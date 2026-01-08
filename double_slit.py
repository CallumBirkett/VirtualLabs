import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.widgets import Slider, Button, CheckButtons

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

    return sin_theta ,Delta, phi, envelope, interference, intensity # return all components

# compute initial interference pattern 
_, Delta, phi, envelope, interference, I = intensity()

# plot intensity
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.40) # sliders will appear at the bottom of the plot 

# plot relative intensity 
(line_I,) = ax.plot(x_values, I, color="red", label="Total Intensity")
ax.set_xlabel("Screen (m)")
ax.set_ylabel("Relative Intensity")
ax.set_title("Young's Double Slit Experiment")
ax.set_ylim(0, 1.05)

# plot the envelope and interference to see that Intensity = envelop * interference - should be toggleable. 
(line_env,) = ax.plot(x_values, envelope, alpha=0.6, label="Envelope (single-slit)")
(line_int,) = ax.plot(x_values, interference, alpha=0.6, label="Interference (two-slit)")
line_env.set_visible(False)
line_int.set_visible(False)
ax.legend(loc="upper right")

# specify slider axes: left, bottom, width, height
wavelength_slider_ax = plt.axes([0.25, 0.3, 0.5, 0.05])
slit_width_slider_ax = plt.axes([0.25, 0.25, 0.5, 0.05])
screen_distance_slider_ax = plt.axes([0.25, 0.2, 0.5, 0.05])
distance_between_slits_slider_ax = plt.axes([0.25, 0.15, 0.5, 0.05])

# create sliders. Normalise values to whole numbers for readability
wavelength_slider = Slider(wavelength_slider_ax, 'Wavelength (nm)', 100, 1000, valinit=wavelength*1e9, valstep=5)
slit_width_slider = Slider(slit_width_slider_ax, 'Slit Width (µm)', 10, 1000, valinit=slit_width*1e6, valstep=5)
distance_between_slits_slider = Slider(distance_between_slits_slider_ax, 'Slit Separation (mm)', .1, 10, valinit=distance_between_slits*1e3,valstep=.05)
screen_distance_slider = Slider(screen_distance_slider_ax, 'Screen Distance (cm)', 10, 100, valinit=screen_distance*1e2, valstep=5)


# reset button axes: left, bottom, width, height
reset_ax = plt.axes([0.02, 0.02, 0.12, 0.06])

# create reset button
reset_button = Button(reset_ax, "Reset")

# toggle buttom axes: left, bottom, width, height
check_ax = plt.axes([0.15, 0.02, 0.12, 0.06])

# create toggle buttons
checks = CheckButtons(check_ax, ["Envelope", "Interference"], [False, False])

# update function to be called when slider is changed.
def update(val):
    lam = wavelength_slider.val * 1e-9
    a = slit_width_slider.val * 1e-6
    d = distance_between_slits_slider.val * 1e-3
    L = screen_distance_slider.val * 1e-2

    # generate new ouputs based on slider inputs
    _, Delta, phi, envelope, interference, I = intensity(a=a, lam=lam, d=d, L=L, x=x_values)

    # update y data for each curve
    line_I.set_ydata(I)
    line_env.set_ydata(envelope)
    line_int.set_ydata(interference)

    # redraw when the event loop is free - asynchronous implementation
    fig.canvas.draw_idle()

# rseet to initial values on button press
def reset(event):
    wavelength_slider.reset()
    slit_width_slider.reset()
    distance_between_slits_slider.reset()
    screen_distance_slider.reset()

# toggle envelope and interference by check box
def toggle(label):
    if label == "Envelope":
        line_env.set_visible(not line_env.get_visible())
    elif label == "Interference":
        line_int.set_visible(not line_int.get_visible())

    fig.canvas.draw_idle()

# call update when slider changed
wavelength_slider.on_changed(update)
slit_width_slider.on_changed(update)
distance_between_slits_slider.on_changed(update)
screen_distance_slider.on_changed(update)

# call reset when button clicked 
reset_button.on_clicked(reset)

# call toggle when checkbox is clicked
checks.on_clicked(toggle)

plt.show()
    

