import numpy as np

def data_to_np(data, key="values"):
    """
    The purpose of this function is to convert single attribute data list values 
    from string dataType to text dataType.
    And then convert it to a transposed np array. This allows for batch processing 
    of multichannel EMG data when extracting features.
    """
    parsed_data = data[key]
    converted_data = [[float(num) for num in sublist] for sublist in parsed_data]
    numpy_arr = np.array(converted_data).T
    return numpy_arr

