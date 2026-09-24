import numpy as np
from PIL import Image
P=Image.open('page.png').convert('RGB')
A=np.asarray(P).copy()
def save(name,x0,x1,y0,y1,paint=()):
    C=A[y0:y1,x0:x1].copy()
    for (a,b,c,d,col) in paint:
        C[c-y0:d-y0,a-x0:b-x0]=col
    Image.fromarray(C).save(f'site/img/{name}.webp',quality=92,method=6)
    print(name,x1-x0,y1-y0)
save('hero',1068,3028,70,1173,[(1246,1375,233,280,(0,0,0)),(1246,1375,323,368,(0,0,0))])
save('montage',1156,2940,3328,3710,[(1768,2914,3562,3682,(253,238,182))])
save('sketches',1068,3028,4062,5165,[(1100,1885,4110,4256,(250,250,250))])
save('arrow',1972,2118,6310,6360)
b1=[(1306.0,1576.58),(1609.39,1880.05),(1912.69,2183.42),(2215.97,2486.76),(2519.43,2790.03)]
for i,(l,r) in enumerate(b1): save(f'wallet-{i+1}',round(l),round(r),round(1884.68),round(2486.27))
b3=[(1148.21,1425.8,6279.21),(1444.08,1721.88,6279.21),(1740.33,2017.93,6279.21),(2098.35,2369.19,6284.73),(2387.83,2658.61,6284.74),(2676.98,2947.81,6284.74)]
for i,(l,r,b) in enumerate(b3): save(f'redesign-{i+1}',round(l),round(r),round(5682.29),round(b))
