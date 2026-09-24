from PIL import Image; import numpy as np
order=[9,6,3,5,1,11]; offs=[0,1910,2105,1957,1694,1201]
starts=np.cumsum(offs)  # in raw_9 coordinates
imgs=[np.asarray(Image.open(f'raw/raw_{i}.png').convert('RGB')) for i in order]
H=starts[-1]+2304
page=np.zeros((H,4096,3),np.uint8)
for k,a in enumerate(imgs):
    s=starts[k]
    lo = 0 if k==0 else (2304 - (starts[k]-starts[k-1]))//2  # middle of overlap with previous
    page[s+lo:s+2304]=a[lo:]
page=page[96:]
Image.fromarray(page).save('page.png')
print(page.shape, [int(s)-96 for s in starts])
# sharpness of sketch overlap
for k,(a,s) in enumerate(zip(imgs[:2],starts[:2])):
    reg=a[1910-s:2304-s,1068:3028].astype(float).mean(2)
    print(order[k], np.abs(np.diff(reg,axis=1)).mean())
