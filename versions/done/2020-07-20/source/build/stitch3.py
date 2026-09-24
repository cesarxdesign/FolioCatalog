from PIL import Image; import numpy as np
order=[9,6,3,5,1,11]; offs=[0,1910,2105,1957,1694,1201]
starts=np.cumsum(offs)
imgs=[np.asarray(Image.open(f'raw/raw_{i}.png').convert('RGB')) for i in order]
H=starts[-1]+2304
page=np.zeros((H,4096,3),np.uint8)
page[0:2304]=imgs[0]
seams=[]
for k in range(1,6):
    A,B=imgs[k-1],imgs[k]; d=offs[k]; n=2304-d
    e=np.abs(A[d:,1068:3028].astype(int)-B[:n,1068:3028].astype(int)).mean((1,2))
    es=np.convolve(e,np.ones(9)/9,'same')
    lo=20; j=lo+int(np.argmin(es[lo:n-20]))
    s=starts[k]
    page[s+j:s+2304]=B[j:]
    seams.append((int(s+j-96), round(float(es[j]),3)))
page=page[96:]
Image.fromarray(page).save('page.png')
print(seams)
