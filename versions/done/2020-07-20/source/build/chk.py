from PIL import Image; import numpy as np
A=np.asarray(Image.open('raw/raw_9.png').convert('RGB')).astype(np.float32)
B=np.asarray(Image.open('raw/raw_6.png').convert('RGB')).astype(np.float32)
d=1910;n=2304-d
D=np.abs(A[d:,1068:3028]-B[:n,1068:3028]).mean(2)
r=D.mean(1); c=D.mean(0)
for y in range(0,n,20): print(y+d, round(float(r[y]),2), end=' | ')
print()
print([ (x+1068, round(float(c[x]),1)) for x in range(0,1960,98)])
