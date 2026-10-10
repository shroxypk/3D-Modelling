"""Connected top and lower rib strips, following the 12:45–15:40 section."""
def build(point,mesh_obj):
    def rail(name,start,end,count,base,outward):
        # Repeated top-face extrusions joined through a continuous narrow base.
        pitch=(end-start)/count
        samples=[(start,3)]
        for i in range(count):
            x=start+i*pitch
            samples.extend([(x+1,12),(x+pitch*.56,12),(x+pitch*.56+1,3),(x+pitch-0.5,3)])
        samples.append((end,3))
        verts=[];faces=[]
        for x,height in samples:
            p=[(-.28,0),(.28,0),(.36,height*.34),(.36,height*.72),(.28,height),(-.28,height),(-.36,height*.72),(-.36,height*.34)]
            verts.extend(point(x,y,base+outward*d) for y,d in p)
        for k in range(len(samples)-1):
            for j in range(8):faces.append((8*k+j,8*k+(j+1)%8,8*(k+1)+(j+1)%8,8*(k+1)+j))
        for offset in [0,8*(len(samples)-1)]:
            for f in [(0,1,2,7),(7,2,3,6),(6,3,4,5)]:faces.append(tuple(offset+j for j in f))
        obj=mesh_obj(name,verts,faces)
        obj['construction']='One connected mesh, alternating raised faces on a continuous base.'
        return obj
    top=rail('04 Top ribbed strip',498,1597,34,256,-1)
    bottom=rail('05 Short lower ribbed strip',498,658,6,448,1)
    return [top,bottom]
