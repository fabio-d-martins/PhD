"""
Diffraction, Incoherent Light
---
Given an aperture, simulates a diffracted image.
---
Copyright (c) 2022, Fábio Duarte Martins
"""

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors

# gamma correction for matplotlib's plot
gamma = 1/2.2
# light intensity
power = 1

# read the images as matrices, single channel
img = cv.imread('images/spoke.png', cv.IMREAD_GRAYSCALE)
kernel = cv.imread('images/apertures/pupil-10.png', cv.IMREAD_GRAYSCALE)

k_dft = np.fft.fft2(kernel)
k_dft = np.fft.fftshift(k_dft)
k_magnitude = np.abs(k_dft * np.conj(k_dft))

k_magnitude = (k_magnitude / k_magnitude.sum()) * power 

img_dft = np.fft.fft2(img)
kernel_dft = np.fft.fft2(k_magnitude)

convolved_img = np.abs(np.fft.ifftshift(np.fft.ifft2(img_dft * kernel_dft)))

plt.imshow(convolved_img, cmap='gray', norm=mcolors.PowerNorm(gamma, 0), interpolation="spline36")
plt.colorbar()
plt.savefig('plot.png', dpi = 1000)
plt.show()

convolved_img = convolved_img.clip(0, 255).astype(np.uint8)

cv.imshow("Diffraction: Incoherent", convolved_img)
cv.imwrite("opencv.png", convolved_img)
cv.waitKey(0)
cv.destroyAllWindows()