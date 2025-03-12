import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
pi=3.1415926535
tau=pi*2/5.35
noise = PerlinNoise(octaves=100, seed=1)
xpix, ypix = 100, 100
pic = [[noise([i/1000, j/1000]) for j in range(xpix)] for i in range(ypix)]

plt.imshow(pic, cmap='gray')
plt.show()