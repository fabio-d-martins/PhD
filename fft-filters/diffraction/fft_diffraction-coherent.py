"""
Diffraction, Coherent Light
---
"""

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors

gamma = 1/2.2
power = .15

img = cv.imread('images/line-chart-inv.png')
kernel = cv.imread('images/apertures/pupil-5.png')

img = cv.cvtColor(img, cv.COLOR_BGR2GRAY) / 255
kernel = cv.cvtColor(kernel, cv.COLOR_BGR2GRAY)

kernel = kernel / kernel.sum()

k_dft = np.fft.fft2(kernel)
k_dft = np.fft.fftshift(k_dft)
k_magnitude = np.abs(k_dft) * power

img_dft = np.fft.fft2(img)
kernel_dft = np.fft.fft2(k_magnitude)

convolved_img = np.abs(np.fft.ifftshift(np.fft.ifft2(img_dft * kernel_dft)))

plt.imshow(convolved_img, cmap='gray', norm=mcolors.PowerNorm(gamma, 0), interpolation="spline36")
plt.colorbar()
#plt.savefig('plot.png', dpi = 1000)
plt.show()

convolved_img = convolved_img.clip(0, 255).astype(np.uint8)

cv.imshow("Diffraction: Incoherent", convolved_img)
#cv.imwrite("opencv.png", convolved_img)
cv.waitKey(0)
cv.destroyAllWindows()