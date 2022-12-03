"""
Halation
---
Simulates light intensity decay using the inverse square law.
---
Copyright (c) 2022, Fábio Duarte Martins
"""

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors
import math

# gamma correction for matplotlib's plot
gamma = 1/2.2
# light intensity
power = 1

# read the image as a matrix, single channel, normalize to 1
img = cv.imread('images/line-chart.png', cv.IMREAD_GRAYSCALE) / 255
# create an array for the kernel, same size as image
kernel = np.copy(img)

# calculate the kernel using the inverse square law
# point of emission is at the centre of the kernel
for i, row in enumerate(kernel):
    for j, pixel in enumerate(kernel):
        xDist = 512 - i
        yDist = 512 - j
        dist = abs(math.sqrt((xDist ** 2) + (yDist ** 2)))
        if dist < 1:
            intensity = power
        else:
            intensity = power / dist**2
        kernel[i][j] = intensity

# calculate the Discrete Fourier Transform
# for both images
img_dft = np.fft.fft2(img)
kernel_dft = np.fft.fft2(kernel)

# convolve the image with the kernel
convolved_img = np.absolute(np.abs(np.fft.ifftshift(np.fft.ifft2(img_dft * kernel_dft))))

# plot the full range of light intensity, gamma corrected
plt.imshow(convolved_img, cmap='gray', norm=mcolors.PowerNorm(gamma, 0), interpolation="spline36")
plt.colorbar()
#plt.savefig('plot.png', dpi = 1000)
plt.show()

# clip pixel range from 0 to 255
convolved_img = convolved_img.clip(0, 255).astype(np.uint8)

cv.imshow("Diffraction: Incoherent", convolved_img)
#cv.imwrite("opencv.png", convolved_img)
cv.waitKey(0)
cv.destroyAllWindows()