"""Carry existing divisions through planar quadrilateral patches."""
import bmesh

def weld_seams(bm):
    for edge in list(bm.edges):
        a,b=edge.verts;ab=b.co-a.co;ll=ab.length_squared
        if ll<1e-12:continue
        hits=[]
        for vert in list(bm.verts):
            if vert in edge.verts:continue
            t=(vert.co-a.co).dot(ab)/ll
            if 1e-5<t<1-1e-5 and (vert.co-a.co-t*ab).length<1e-5:hits.append((t,vert.co.copy()))
        for t,co in sorted(hits,reverse=True):
            fraction=(co-a.co).length/(edge.other_vert(a).co-a.co).length
            _,nv=bmesh.utils.edge_split(edge,a,fraction);nv.co=co
            edge=next(e for e in a.link_edges if nv in e.verts)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-5)

def repair(bm):
    for iteration in range(12):
        weld_seams(bm);changes=0
        for f in list(bm.faces):
            if len(f.verts)<=4:continue
            pts=[v.co.copy() for v in f.verts];n=len(pts)
            corners=[i for i in range(n) if (pts[i]-pts[i-1]).cross(pts[(i+1)%n]-pts[i]).length>1e-5]
            if len(corners)!=4:continue
            cp=[pts[i] for i in corners];cuts=[]
            for k in range(4):
                start=corners[k];end=corners[(k+1)%4]
                if end<=start:end+=n
                edge=cp[(k+1)%4]-cp[k];ll=edge.length_squared
                cuts.append([round((pts[i%n]-cp[k]).dot(edge)/ll,5) for i in range(start,end+1)])
            us=sorted(set(cuts[0]+[round(1-t,5) for t in cuts[2]]))
            vs=sorted(set(cuts[1]+[round(1-t,5) for t in cuts[3]]))
            if len(us)*len(vs)>80:continue
            bm.faces.remove(f);grid=[]
            for v in vs:
                row=[]
                for u in us:
                    row.append(bm.verts.new((1-v)*((1-u)*cp[0]+u*cp[1])+v*((1-u)*cp[3]+u*cp[2])))
                grid.append(row)
            for j in range(len(vs)-1):
                for i in range(len(us)-1):bm.faces.new((grid[j][i],grid[j][i+1],grid[j+1][i+1],grid[j+1][i]))
            changes+=1
        bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-5)
        if not changes:break
    weld_seams(bm)
