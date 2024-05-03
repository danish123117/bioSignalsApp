import numpy as np
import json
import ast

def data_to_np(data, key="values"):
    """
    The purpose of this function is to convert single attribute data list values 
    from string dataType to text dataType.
    And then convert it to a transposed np array. This allows for batch processing 
    of multichannel EMG data when extracting features.
    """
   # data = json.loads(data)
    parsed_data = data[key]
    intlist =[ast.literal_eval(string) for string in parsed_data]
   # print(parsed_data)
    converted_data = [[float(num) for num in sublist] for sublist in intlist]
    numpy_arr = np.array(converted_data)
    return numpy_arr
