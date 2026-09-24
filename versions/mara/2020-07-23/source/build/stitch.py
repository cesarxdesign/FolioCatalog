import numpy as np
from PIL import Image
S='source/screenshots/'
fs=['1-2024-07-07-19.30.47.png','2-2024-07-07-19.30.50.png','3-2024-07-07-19.30.52.png','4-2024-07-07-19.30.59.png']
A=[np.asarray(Image.open(S+f).convert('RGB')) for f in fs]
off=[0,2056,4137,5579]
H=off[-1]+2304
P=np.zeros((H,4096,3),np.uint8)
cuts=[0]+[ (off[i+1]+off[i]+2304)//2 for i in range(3)]+[H]
for i in range(4):
    P[cuts[i]:cuts[i+1]]=A[i][cuts[i]-off[i]:cuts[i+1]-off[i]]
print(cuts)
P=P[96:]
Image.fromarray(P).save('page.png')
print(P.shape)
