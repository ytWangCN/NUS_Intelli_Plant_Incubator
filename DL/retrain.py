import numpy as np
from tensorflow.keras.optimizers import Adam
from cv2 import cv2
from tensorflow.keras.preprocessing.image import img_to_array
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.applications import InceptionV3
import os
import tensorflow as tf
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.models import Sequential
import albumentations

norm_size = 224
datapath = 'data/train'
EPOCHS = 50
INIT_LR = 3e-4
labelList = []
dicClass = {0:'apple_healthy' ,1 :'apple_scab_general', 2:'apple_scab_serious', 3:'apple_frogeve_spot',4: 'cedar_apple_rust_general', 5:'cedar_apple_rust_serious', 6:'cherry_heealthy',
            7:'cherry_powdery_mildew_general',8: 'cherry_powdery_mildew_serious', 9:'corn_healthy', 10:'cercospora_zearmaydis_tehon_and_daniels_general',11: 'cercospora_zearmaydis_tehon_and_daniels_serious',
            12:'puccinia_polvsora_general', 13:'puccinia_polvsora_serious',14:'corn_curvularia_leaf_spot_fungus_general',
            15:'corn_curvularia_leaf_spot_fungus_serious' ,16 :'maize_dwarf_mosaic_virus' ,  17:'grape_healthy', 18:'grape_black_rot_fungus_general',
            19:'grape_black_rot_fungus_serios', 20:'grape_black_measles_fungus_general', 21:'grape_blacj_measles_fungus_serious', 22:'grape_leaf_blight_fungus_general',23: 'grape_leaf_blight_fungus_serious',
            24:'citrus_healthy',25: 'citrus_greeninig_june_general', 26:'citrus_greening_june_serious', 27:'peach_healthy', 28:'peach_bacterial_general',29:'peach_bacterial_serious',
            30:'pepper_healthy',31:'pepper_scab_1',32:'pepper_scab_2', 33:'potato_healthy',34: 'potato_early_blight_fungus_1',35: 'potato_early_blight_fungus_2', 36:'potato_late_blight_fungus_1', 37:'potato_late_blight_fungus_2',
            38:'strawberry_0', 39:'strawberry_scorch_1',40: 'strawberry_scorch_2',41: 'tomato_0',42: 'tomato_powdery_mildgew_1', 43:'tomato_powdery_mildgew_2',44: 'tomato_early_1', 45:'tomato_early_2',46: 'tomato_late_1',
            47:'tomato_late_2',48:'tomato_leaf_1', 49:'tomato_leaf_2', 50:'tomato_spot_1',51:'tomato_spot_2', 52:'tomato_sep_1',53:'tomato_sep_2',54:'tomato_spider_1',
            55:'tomato_spider_2',56:'tomato_ylcv_1',57:'tomato_yclv_2',58:'tomato_tomv'}
classnum = 59
batch_size = 64
np.random.seed(42)
print(dicClass[0])
def loadImageData():
    imageList = []
    listClasses = os.listdir(datapath)  # 类别文件夹
    print(listClasses)
    for class_name in listClasses:
        label_id = dicClass[int(class_name)]
        class_path = os.path.join(datapath, class_name)
        image_names = os.listdir(class_path)
        for image_name in image_names:
            image_full_path = os.path.join(class_path, image_name)
            labelList.append(int(class_name))
            imageList.append(image_full_path)
    return imageList


print("loading data...")
imageArr = loadImageData()
labelList = np.array(labelList)
print("Successfully Complete")

trainX, valX, trainY, valY = train_test_split(imageArr, labelList, test_size=0.2, random_state=42)

train_transform = albumentations.Compose([
        albumentations.OneOf([
            albumentations.RandomGamma(gamma_limit=(60, 120), p=0.9),
            albumentations.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.9),
            albumentations.CLAHE(clip_limit=4.0, tile_grid_size=(4, 4), p=0.9),
        ]),
        albumentations.HorizontalFlip(p=0.5),
        albumentations.ShiftScaleRotate(shift_limit=0.2, scale_limit=0.2, rotate_limit=20,
                                        interpolation=cv2.INTER_LINEAR, border_mode=cv2.BORDER_CONSTANT, p=1),
        albumentations.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), max_pixel_value=255.0, p=1.0)
    ])
val_transform = albumentations.Compose([
        albumentations.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), max_pixel_value=255.0, p=1.0)
    ])


def generator(file_pathList,labels,batch_size,train_action=False):
    L = len(file_pathList)
    while True:
        input_labels = []
        input_samples = []
        for row in range(0, batch_size):
            temp = np.random.randint(0, L)
            X = file_pathList[temp]
            Y = labels[temp]
            image = cv2.imdecode(np.fromfile(X, dtype=np.uint8), -1)
            if image.shape[2] > 3:
                image = image[:, :, :3]
            if train_action:
                image=train_transform(image=image)['image']
            else:
                image = val_transform(image=image)['image']
            image = cv2.resize(image, (norm_size, norm_size), interpolation=cv2.INTER_LANCZOS4)
            image = img_to_array(image)
            input_samples.append(image)
            input_labels.append(Y)
        batch_x = np.asarray(input_samples)
        batch_y = np.asarray(input_labels)
        yield (batch_x, batch_y)

checkpointer=tf.keras.callbacks.ModelCheckpoint(filepath='D:/plantDisease.h5', monitor='val_accuracy', verbose=1, save_best_only=True, save_weights_only=False, mode='max')
reduce=tf.keras.callbacks.ReduceLROnPlateau(monitor='val_accuracy', factor=0.5, patience=10, verbose=1, min_lr=1e-6)

model = Sequential()
model.add(InceptionV3(include_top=False, pooling='avg', weights='imagenet'))
model.add(Dense(classnum, activation='softmax'))
optimizer = Adam(learning_rate=INIT_LR)
model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
history = model.fit(generator(trainX,trainY,batch_size,train_action=True),
                              steps_per_epoch=len(trainX) / batch_size,
                              validation_data=generator(valX,valY,batch_size,train_action=False),
                              epochs=EPOCHS,
                              validation_steps=len(valX) / batch_size,
                              callbacks=[checkpointer, reduce])
model.save('D:/my_model.h5')
print(history)
