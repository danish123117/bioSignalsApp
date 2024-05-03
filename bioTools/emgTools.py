from scipy import signal
import numpy as np

def data_filter(data, sampling_frequency, band_lower, band_upper,notch_filter=True,removed_frequency=50,notch_quality=30, axis =1 ):
    """
    This function performs a combined band pass filtering and notch filter
    data : is an N column input numpy array where each column represents an EMG data channel
    band_lower and band_upper: are the lower and upper limits of band pass filter
    notch_filter:  is a boolean which can be used to switch off the notch filter it is by default True
    removed_frequency: is the frequency removed by the notch filter by default it is set to 50hz AC frequency
    notch_quality : is the quality of notch filteration set to 30 by default.
    """
    if axis == 1: 
        data = data.T
    Niquist_frequency = sampling_frequency/2
    nor_band_lo = band_lower/Niquist_frequency
    nor_band_hi = band_upper/Niquist_frequency
    nor_del_freq = removed_frequency/Niquist_frequency
    sos_band = signal.iirfilter(4, [ nor_band_lo, nor_band_hi],btype='band', ftype='butter', output = "sos")
    if notch_filter==True:
        b, a = signal.iirnotch(nor_del_freq, notch_quality, sampling_frequency)
        filtered_band = np.array(signal.sosfiltfilt(sos_band , data))
        filtered = signal.lfilter(b, a, filtered_band)
    else: 
        filtered = np.array(signal.sosfiltfilt(sos_band , data))
    return filtered

def out_stft(data, sampling_frequency, axis =1): 
    """
    Performs feature extraction on EMG data 
    Input: 
    Filtered signal:  as N column numpy array where each column represents an EMG data channel. 
    sampling_frequency
    Output:  
    N element lists containing median frequency , mean frequency, 
    mean power frequency and zero crossing rate   
    """
    if axis !=1: 
        data = data.T
    num_samples, num_channels = data.shape
    durations = np.full(num_channels, num_samples / sampling_frequency)
    diffs = np.diff(np.sign(data), axis=0)
    zero_crossings = np.sum(diffs != 0, axis=0)
    frequency_zeroCrossing = zero_crossings / durations
    frequency_domain = np.fft.fft(data, axis=0)
    magnitude_spectrum = np.abs(frequency_domain)
    sampling_rate = 1 / sampling_frequency
    frequency_bins = np.fft.fftfreq(num_channels, d=sampling_rate)
    positive_frequencies = frequency_bins[:num_channels//2]
    frequency_mean = np.sum(magnitude_spectrum[:num_channels//2] * positive_frequencies[:, np.newaxis], axis=0) / np.sum(magnitude_spectrum[:num_channels//2], axis=0)
    frequency_meanPower = np.sqrt(np.sum(magnitude_spectrum[:num_channels//2] * positive_frequencies[:, np.newaxis]**2, axis=0) / np.sum(magnitude_spectrum[:num_channels//2], axis=0))
    cumulative_power = np.cumsum(magnitude_spectrum[:num_channels//2], axis=0)
    half_power = np.sum(magnitude_spectrum[:num_channels//2], axis=0) / 2
    median_indices = np.argmax(cumulative_power > half_power, axis=0)
    frequency_median = positive_frequencies[median_indices]
    
    return frequency_median , frequency_mean , frequency_meanPower, frequency_zeroCrossing

def stress_out(frequency_median, frequency_mean, frequency_meanPower, frequency_zeroCrossing, parms):
    """
    The stress out function normalises the mean, median, mean power, and zero crossing frequency by the baseline values
    The baseline values are taken from a param.json file and it is person specific
    """
    # Convert parms dictionary to NumPy arrays
    p_med = np.array([parms["medianFrequency"]["ch" + str(i+1)] for i in range(len(frequency_median))])
    p_mean = np.array([parms["meanFrequency"]["ch" + str(i+1)] for i in range(len(frequency_mean))])
    p_pow = np.array([parms["meanPowerFrequency"]["ch" + str(i+1)] for i in range(len(frequency_meanPower))])
    p_zero = np.array([parms["zeroCrossingFrequency"]["ch" + str(i+1)] for i in range(len(frequency_zeroCrossing))])
    # Calculate normalized values using vectorized operations 
    frequency_median_norm = p_med / frequency_median# test the correctness
    frequency_mean_norm = p_mean / frequency_mean
    frequency_meanPower_norm = p_pow / frequency_meanPower
    frequency_zeroCrossing_norm = p_zero / frequency_zeroCrossing
    
    return frequency_median_norm, frequency_mean_norm, frequency_meanPower_norm, frequency_zeroCrossing_norm