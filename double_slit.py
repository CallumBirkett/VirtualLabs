import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.widgets import Slider 

# screen coords when screen is viewed as a 1d array, +/- 5mm
x_values = np.arange(-0.005, 0.005, 0.00001) 

# initial parameters (to be changed by sliders)
slit_width = 100 * (1e-6) # micrometre range
wavelength  = 500 * (1e-9) # nanometre range (500nm is green light)
distance_between_slits = 1 * (1e-3) # millimetre range 
screen_distance = 50 * (1e-2) # centimetre range  


def intensity(a=slit_width, lam=wavelength, d=distance_between_slits, L=screen_distance, x=x_values):

    # small angle approx. screen height over screen distance - see sin(theta) = tan(theta) =approx. 0
    sin_theta = x / L 

    # path difference
    Delta = d * sin_theta

    # phase difference
    phi = (2 * np.pi / lam) * Delta 

    # interference
    interference = np.cos(phi / 2) ** 2

    # diffraction envelope
    alpha = (np.pi * a / lam) * sin_theta 

    # compute sin(alpha) / alpha. Blows up at alpha = 0, but the limit exists there. 
    envelope = np.ones_like(alpha) # initialise a flat shape for the envelope
    nonzero = alpha != 0 # find nozero values of alpha
    envelope[nonzero] = (np.sin(alpha[nonzero])/alpha[nonzero]) ** 2 # shape is followed, defaults to 1 when alpha = 0

    intensity = envelope * interference

    return intensity

print(intensity())
