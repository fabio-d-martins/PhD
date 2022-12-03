import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors

gamma = 1/2.2
power = 1

img = cv.imread('images/line-chart-inv.png', cv.IMREAD_GRAYSCALE)
aperture = cv.imread('images/pupil-5.png', cv.IMREAD_GRAYSCALE)

aperture = aperture / aperture.sum()

aperture_dft = np.fft.fftshift(np.fft.fft2(aperture))
aperture_psf = np.fft.fft2(aperture_dft)

kernel = np.abs(np.fft.ifftshift(np.fft.ifft2(aperture_dft * aperture_psf)))

img_dft = np.fft.fft2(img)
kernel_dft = np.fft.fft2(kernel)

convolved_img = np.abs(np.fft.ifftshift(np.fft.ifft2(img_dft * kernel_dft)))

plt.imshow(convolved_img, cmap='gray', norm=mcolors.PowerNorm(gamma, 0), interpolation="spline36")
plt.colorbar()
#plt.savefig('plot.png', dpi = 1000)
plt.show()

'''
convolved_img = convolved_img.clip(0, 255).astype(np.uint8)

cv.imshow("Diffraction: Incoherent", convolved_img)
#cv.imwrite("opencv.png", convolved_img)
cv.waitKey(0)
cv.destroyAllWindows()

'''