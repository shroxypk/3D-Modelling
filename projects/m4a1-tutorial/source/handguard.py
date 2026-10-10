"""Tutorial 03:30–10:30 forms rebuilt as one continuous handguard surface."""
import bpy, math

def build(point, mesh_obj):
    # Common station layout follows the front/rear underside cut-ups demonstrated in the video.
    stations=[(498,450),(662,450),(672,436),(685,426),(703,420),
              (1315,420),(1338,424),(1357,436),(1374,450),(1597,450)]
    verts=[]; faces=[]; ids={}
    def depth(x):
        # Continuous transitions into the wider end blocks; the front ribbed section is integral.
        if x<617:
            for a,b in [(500,514),(531,545),(562,576),(593,607)]:
                if a<=x<=b: return .89
                if a-2<x<a:return .72+(.17*(x-a+2)/2)
                if b<x<b+2:return .89-(.17*(x-b)/2)
            return .72
        if x<665:return .89
        if x<690:return .89-(x-665)/25*.17
        if x<1494:return .72
        if x<1510:return .72+(x-1494)/16*.17
        if x<1550:return .89
        if x<1570:return .89-(x-1550)/20*.09
        return .80
    def v(x,py,offset=0):
        co=point(x,depth(x)+offset,py); key=tuple(round(c,7) for c in co)
        if key not in ids: ids[key]=len(verts); verts.append(co)
        return ids[key]
    top,bottom=307,375; cy=(top+bottom)/2
    def rect(a,b):
        cx=(a+b)/2; dx=(b-a)/2; dy=(bottom-top)/2
        result=[(cx+dx,cy),(cx+dx,cy-dy/2),(cx+dx,cy-dy),(cx+dx/2,cy-dy),
                (cx,cy-dy),(cx-dx/2,cy-dy),(cx-dx,cy-dy),(cx-dx,cy-dy/2),
                (cx-dx,cy),(cx-dx,cy+dy/2),(cx-dx,cy+dy),(cx-dx/2,cy+dy),
                (cx,cy+dy),(cx+dx/2,cy+dy),(cx+dx,cy+dy),(cx+dx,cy+dy/2)]
        # Shared stations capture the rear underside relief without terminating extra loops.
        if a==1230:
            for index,x in [(3,1338),(4,1315),(5,1260),(11,1260),(12,1315),(13,1338)]:result[index]=(x,result[index][1])
        if a==1357:
            for index in [5,11]:result[index]=(1374,result[index][1])
        return result
    def rounded(cx,hy,hx,r):
        k=math.sqrt(.5); cy=344
        return [(cx+hx,cy),(cx+hx,cy-hy+r),(cx+hx-r+r*k,cy-hy+r-r*k),(cx+hx-r,cy-hy),
                (cx,cy-hy),(cx-hx+r,cy-hy),(cx-hx+r-r*k,cy-hy+r-r*k),(cx-hx,cy-hy+r),
                (cx-hx,cy),(cx-hx,cy+hy-r),(cx-hx+r-r*k,cy+hy-r+r*k),(cx-hx+r,cy+hy),
                (cx,cy+hy),(cx+hx-r,cy+hy),(cx+hx-r+r*k,cy+hy-r+r*k),(cx+hx,cy+hy-r)]
    def bridge(a,b):
        faces.extend((a[i],a[(i+1)%len(a)],b[(i+1)%len(a)],b[i]) for i in range(len(a)))
    def solidcell(a,b):
        g=[[v(a+(b-a)*i,top+(bottom-top)*j/4) for j in range(5)] for i in range(2)]
        for i in range(1):
            for j in range(4):faces.append((g[i][j],g[i+1][j],g[i+1][j+1],g[i][j+1]))
    front=[498,500,514,516,529,531,545,547,560,562,576,578,591,593,607,609,617,662,665,672,685,690,703,713]
    for a,b in zip(front,front[1:]):solidcell(a,b)
    bounds=[713,850,976,1103.5,1230,1357,1494]
    holes=[(733,840),(860,966),(986,1094),(1113,1220),(1240,1347),(1367,1474)]
    for (a,b),(h0,h1) in zip(zip(bounds,bounds[1:]),holes):
        outer=[v(x,y) for x,y in rect(a,b)]
        lip=[v(x,y) for x,y in rounded((h0+h1)/2,15,(h1-h0)/2+1,9)]
        hole=[v(x,y,-.014) for x,y in rounded((h0+h1)/2,14,(h1-h0)/2,8)]
        bridge(outer,lip);bridge(lip,hole)
    for a,b in zip([1494,1502,1510,1550,1560,1570],[1502,1510,1550,1560,1570,1597]):solidcell(a,b)
    # Grow the upper and lower shoulders directly from the side-strip boundary edges.
    # This shares vertices throughout, rather than joining closed overlapping objects.
    counts={}
    for face in faces:
        for a,b in zip(face,face[1:]+face[:1]):
            e=tuple(sorted((a,b)));counts[e]=counts.get(e,0)+1
    def vertex(co):
        key=tuple(round(c,7) for c in co)
        if key not in ids:ids[key]=len(verts);verts.append(co)
        return ids[key]
    def low(x):
        for (a,h0),(b,h1) in zip(stations,stations[1:]):
            if a-1e-6<=x<=b+1e-6:return h0+(h1-h0)*(x-a)/(b-a)
        return stations[-1][1]
    def lower_rows(x):
        height=low(x)
        # Cut the underside relief through a planar shoulder, rather than
        # twisting each quad by pinning its lower edge to a fixed width.
        width=.64-(height-9-375)*(.33/66)
        return [(375,.64),(height-9,width),(height,width),(height,0)]
    for (a,b),count in counts.items():
        if count!=1:continue
        va,vb=verts[a],verts[b]
        ya,yb=345-va[2]*100,345-vb[2]*100
        if abs(ya-yb)>1e-5 or not (abs(ya-top)<1e-5 or abs(ya-bottom)<1e-5):continue
        xa,xb=va[0]*100+850,vb[0]*100+850
        upper=abs(ya-top)<1e-5
        rowsa=[(307,.64),(267,.31),(255,.31),(255,0)] if upper else lower_rows(xa)
        rowsb=[(307,.64),(267,.31),(255,.31),(255,0)] if upper else lower_rows(xb)
        for (pa,wa),(pb,wb) in zip(rowsa,rowsb):
            aa=vertex(point(xa,wa,pa));bb=vertex(point(xb,wb,pb))
            faces.append((a,b,bb,aa));a,b=aa,bb
    shell=mesh_obj('02 Handguard | continuous shell and slotted sides',verts,faces)
    mir=shell.modifiers.new('Width symmetry | welded center','MIRROR');mir.use_axis=(False,True,False);mir.use_clip=True;mir.merge_threshold=.00001
    so=shell.modifiers.new('One wall thickness | includes slot walls','SOLIDIFY');so.thickness=.055;so.offset=-1;so.use_even_offset=False;so.thickness_clamp=.8
    shell['tutorial_stage']='03:30–10:30 forms; continuous topology adaptation of the tutorial intermediate objects'
    shell['construction']='Shared side/shoulder vertices, one connected base surface, one thickness operation.'
    return shell
