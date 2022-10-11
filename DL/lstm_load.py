import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd
import numpy as np
from  tensorflow.keras.models import load_model

def lstm():
    predict = load_model("D:/lstm.h5")
    filepath = 'D:/sensorData.csv'
    data = pd.read_csv(filepath)
    # print(data.head())
    feat = data.iloc[:, 1:4]
    date = data.iloc[:, 0]
    input = feat[-12:]
    # input = (input + 25)/70
    input = np.expand_dims(input, axis=0)
    # print(input)
    result = predict.predict(input) * 70 - 25
    result=round(float(result[0][0]),2)
    # print(result)
    if result < 24 :
        return 'Future temperature will be '+str(result)+'℃. The temperature is quite comfortable for the Plant'
    else:
        return 'Future temperature will be '+str(result)+'℃. The temperature will rise up in a short time. Ventilation Needed'

# lstm()