import RPi.GPIO as GPIO
import time
import scipy.signal as signal
from pathlib import Path
import numpy as np
import pandas as pd 
import tensorflow as tf
import matplotlib.pyplot as plt

def collect_data(s_pin, sampling_rate, duration, filename = "emg_data.txt"):
    """
    Collects data from the EMG sensor using the GPIO pins from Raspberry Pi 
    and saves it into a file with the name specified in the filename parameter.

    Parameters:
    s_pin (int): Signal pin
    sampling_rate (int): Sampling rate
    duration (int): Duration of data collection
    filename (str): Name of the file to save the data

    Returns:
    None

    """
    signal_pin = s_pin # PCM_CLK

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(signal_pin, GPIO.IN)

    samples = int(sampling_rate * duration)

    with open(filename, "w") as file:
        for i in range(samples):
            # Read the signal from the GPIO pin
            signal = GPIO.input(signal_pin)
            file.write(str(signal))
            file.write("\n")

    GPIO.cleanup()

def clean_data(path, stop):
    """
    Cleans the data by removing the DC offset and converting the data into
    a numpy array.

    Parameters:
    path (str): Path to the file containing the data
    stop (int): Stop time

    Returns:
    None

    """
    data = np.loadtxt(path, dtype=int)
    data = np.abs(np.diff(data))
    num_sample = data.size
    time = np.zeros((num_sample,), int)
    sample_rate = np.reciprocal(np.divide(stop, num_sample))
    return data, sample_rate

def filter_data(data, s_rate):
    """
    Filters the data using a bandpass filter and a lowpass filter.

    Parameters:
    data (numpy array): Data to be filtered
    s_rate (int): Sampling rate

    Returns:
    None

    """
    nyquist_f = s_rate/2
    high = 0.75/nyquist_f
    low = 15/nyquist_f
    b, a = signal.butter(4, [high, low], btype='bandpass')
    emg_filtered = signal.filtfilt(b, a, data, axis=0)
    emg_rectified = np.abs(emg_filtered)
    low_pass = 0.5/nyquist_f
    print(nyquist_f)
    b2, a2 = signal.butter(4, low_pass, btype='lowpass')
    emg_envelop = signal.filtfilt(b2, a2, emg_rectified, axis=0)
    return emg_envelop

def plot_data(data, s_rate):
    """
    Plots the data.

    Parameters:
    data (numpy array): Data to be plotted
    s_rate (int): Sampling rate

    Returns:
    None

    """
    num_sample = data.size
    time = np.zeros((num_sample,), int)
    for i in range(num_sample):
        time[i] = i/s_rate
    plt.plot(time, data)
    plt.show()

def detect_button(state):
    """
    Detects the button press and returns the state of the button.

    Parameters:
    state (int): State of the button

    Returns:
    int: State of the button
    """
    button_pin = 23
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button_pin, GPIO.IN)
    if GPIO.input(button_pin) == 1:
        if state == 0:
            return 1
        else:
            return 0

def predict_emg(data, model):
    """
    Predicts the EMG signal using a pretrained model I build.

    Parameters:
    data (numpy array): Data to be predicted
    model (tensorflow model): Trained emg model (a Deep Neural Network)

    Returns:
    int: 1 if grab, 0 if release
    """
    data = pd.DataFrame(data)
    # I'll do the dataframe processing later
    prediction = model.predict(data)
    if prediction >= 0.5:
        return 1    # grab
    else:
        return 0    # release

def arm_motion(motion):
    """
    Controls the motion of the synthetic arm based on the prediction.
    Using GPIO pins to control the servo motor.
    Maybe using Arduino in the future to control the servo motor.
    
    Parameters:
    motion (int): The predicted state based on the ML model

    Returns:
    None
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    servo = GPIO.PWM(17, 50)
    servo.start(0)
    duty = 2
    if motion == 1:
        print("Grab")
        ### Insert more Arduino/ Raspberry Pi Code for Servo or motor
        while duty <= 12:
            servo.ChangeDutyCycle(duty)
            duty = duty + 1
    else:
        print("Release")
        servo.ChangeDutyCycle(2)
        servo.ChangeDutyCycle(0)


if __name__ == "__main__":
    state = 0
    stoptime = 10
    sample_rate = 100
    duration = 10
    signal_pin = 18
    start = time.time()
    end = time.time()
    filename = "emg_data.txt"
    model = tf.keras.models.load_model("emg_model.h5")
    motion = 0

    i = 0
    while True:
        if end - start > 1/sample_rate:
            start = time.time()
            state = detect_button(state)
            if state == 1:
                collect_data(signal_pin, sample_rate, duration, filename)
                end = time.time()
                data, s_rate = clean_data(filename, stoptime)
                data = filter_data(data, s_rate)
                # plot_data(data, s_rate)
                motion = predict_emg(data, model)
                arm_motion(motion)

            # Create new file for each duration
            i += 1
            filename = f"emg_data{i}.txt"


