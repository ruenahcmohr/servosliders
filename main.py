

from servoArray import *
import tkinter as tk


servos = ServoControllerSSC8("/dev/ttyUSB0")

#servos.set_position(0, 255)
#servos.set_position(1, 513)
#servos.set_position(2, 1025)
#servos.set_position(3, 2049)
#servos.set_position(4, 4097)
#servos.set_position(5, 8193)
#servos.set_position(6, 16385)
#servos.set_position(7, 32769)

#results = servos.build_command()

#for value in results:
#    print(f"0x{value:02X} ", end="")
#print("")


def update_value(slider_number, value):
    # Update the label text with the new value of the slider
    labels[slider_number].config(text=f"CH {slider_number + 1}: {value:05d}")
    servos.set_position(slider_number, value)

# Create the main window
root = tk.Tk()
root.title("Servo controller")

# List to hold slider and label widgets
sliders = []
labels = []

# Create 8 sliders and labels
for i in range(8):
    # Create the vertical slider
    slider = tk.Scale(root, from_=48000, to=0, orient="vertical", length=300)
    slider.set(24000)
    slider.grid(row=0, column=i, padx=10, pady=5)
    
    # Create the label that will show the slider's value
    label = tk.Label(root, text=f"CH {i + 1}: 24000")
    label.grid(row=1, column=i, padx=10, pady=5)
    
    # Store the slider and label
    sliders.append(slider)
    labels.append(label)
    
    # Bind the update function to the slider
    slider.bind("<Motion>", lambda event, slider_number=i: update_value(slider_number, sliders[slider_number].get()))

servos.start_stream()

# Run the Tkinter event loop
root.mainloop()
