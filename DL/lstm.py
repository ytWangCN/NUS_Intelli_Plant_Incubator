import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd
import numpy as np
from sklearn.preprocessing import  MinMaxScaler
import matplotlib.pyplot as plt

filepath = 'lstm_train.csv'
data = pd.read_csv(filepath)
print(data.head())
feat = data.iloc[:, 1:4]
date = data.iloc[:, 0]

train_num = 5000  # 取前5000组数据用于训练
val_num = 8220  # 取后面的数据用于验证

# 归一化（但是我这里想改成用scaler类函数归一化，这样方便后面反归一化）-25 - 45
# feat_mean = feat[:train_num].mean(axis=0)
# feat_std = feat[:train_num].std(axis=0)
feat = (feat + 25 ) / 70
targets = feat.iloc[:, 0]
feat



def TimeSeries(dataset, start_index, history_size, end_index, step,
               target_size, point_time, true):
    data = []  # 保存特征数据
    labels = []  # 保存特征数据对应的标签值

    start_index = start_index + history_size  # 第一次的取值范围[0:start_index]

    # 如果没有指定滑动窗口取到哪个结束，那就取到最后
    if end_index is None:
        # 数据集最后一块是用来作为标签值的，特征不能取到底
        end_index = len(dataset) - target_size

    # 滑动窗口的起始位置到终止位置每次移动一步
    for i in range(start_index, end_index):

        # 滑窗中的值不全部取出来用，每隔60min取一次
        index = range(i - history_size, i, step)  # 第一次相当于range(0, start_index, 6)

        # 根据索引取出所有的特征数据的指定行
        data.append(dataset.iloc[index])

        # 用这些特征来预测某一个时间点的值还是未来某一时间段的值
        if point_time is True:  # 预测某一个时间点
            # 预测未来哪个时间点的数据，例如[0:20]的特征数据（20取不到），来预测第20个的标签值
            labels.append(true[i + target_size])

        else:  # 预测未来某一时间区间
            # 例如[0:20]的特征数据（20取不到），来预测[20,20+target_size]数据区间的标签值
            labels.append(true[i:i + target_size])

    # 返回划分好了的时间序列特征及其对应的标签值
    return np.array(data), np.array(labels)


history_size = 12
target_size = 0  # 预测未来下一个时间点的气温值
step = 1  # 步长为1取所有的行

# 构造训练集
x_train, y_train = TimeSeries(dataset=feat, start_index=0, history_size=history_size, end_index=train_num,
                              step=step, target_size=target_size, point_time=True, true=targets)

# 构造测试集
x_test, y_test = TimeSeries(dataset=feat, start_index=val_num, history_size=history_size, end_index=13220,
                            step=step, target_size=target_size, point_time=True, true=targets)

# 查看数据集信息
print('x_train_shape:', x_train.shape)
print('y_train_shape:', y_train.shape)

train_ds = tf.data.Dataset.from_tensor_slices((x_train, y_train))
train_ds = train_ds.batch(100).shuffle(10000)  # 随机打乱、每个step处理100组数据

val_ds = tf.data.Dataset.from_tensor_slices((x_test, y_test))
val_ds = val_ds.batch(1)

# 查看数据集信息
sample = next(iter(train_ds))  # 取出一个batch的数据
print('x_train.shape:', sample[0].shape)
print('y_train.shape:', sample[1].shape)
train_ds

inputs_shape = sample[0].shape[1:]
inputs = keras.Input(shape=inputs_shape)
inputs.shape

# LSTM层，设置l2正则化
x = layers.LSTM(units=8, dropout=0.5, return_sequences=True, kernel_regularizer=tf.keras.regularizers.l2(0.01))(inputs)
x = layers.LeakyReLU()(x)
x = layers.LSTM(units=16, dropout=0.5, return_sequences=True, kernel_regularizer=tf.keras.regularizers.l2(0.01))(inputs)
x = layers.LeakyReLU()(x)
x = layers.LSTM(units=32, dropout=0.5, kernel_regularizer=tf.keras.regularizers.l2(0.01))(x)
x = layers.LeakyReLU()(x)
# 全连接层，随即正态分布的权重初始化，l2正则化
x = layers.Dense(64, kernel_initializer='random_normal', kernel_regularizer=tf.keras.regularizers.l2(0.01))(x)
x = layers.Dropout(0.5)(x)
# 输出层返回回归计算后的未来某一时间点的气温值
outputs = layers.Dense(1)(x)

model = keras.Model(inputs, outputs)

model.summary()

model.compile(optimizer=keras.optimizers.Adam(0.001),
              loss=tf.keras.losses.MeanAbsoluteError())

epochs = 15

history = model.fit(train_ds, epochs=epochs, validation_data=val_ds)

model.evaluate(val_ds)
model.save('D:/lstm.h5')
x_predict = x_test[:200]  # 用测试集的前200组特征数据来预测
y_true = y_test[:200]  # 每组特征对应的标签值

y_predict = model.predict(x_predict)
# 这里要反归一化，我还没做


y_predict_result=y_predict * 70 -25
print(y_predict_result)
