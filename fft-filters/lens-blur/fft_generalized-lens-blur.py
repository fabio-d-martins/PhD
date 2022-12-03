"""
Lens Blur, Generalized
---
Simulates a lens blur as a section of the converging lens-to-point light cone.
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
# we assume the kernel as a section of the converging light cone
img = cv.imread('images/abcd-inv.png', cv.IMREAD_GRAYSCALE)
kernel = cv.imread('images/apertures/pupil-1.png', cv.IMREAD_GRAYSCALE)

# normalize the kernel
kernel = kernel / kernel.sum()

# calculate the Discrete Fourier Transform
# for both images
img_dft = np.fft.fft2(img)
kernel_dft = np.fft.fft2(kernel) * power

# convolve the image with the kernel
convolved_img = np.abs(np.fft.ifftshift(np.fft.ifft2(img_dft * kernel_dft)))

# plot the full range of light intensity, gamma corrected
plt.imshow(convolved_img, cmap='gray', norm=mcolors.PowerNorm(gamma, 0), interpolation="spline36")
plt.colorbar()
#plt.savefig('plot.png', dpi = 600)
plt.show()

# clip pixel range from 0 to 255
convolved_img = convolved_img.clip(0, 255).astype(np.uint8)

cv.imshow("General Lens Blur", convolved_img)
#cv.imwrite("opencv.png", convolved_img)
cv.waitKey(0)
cv.destroyAllWindows()