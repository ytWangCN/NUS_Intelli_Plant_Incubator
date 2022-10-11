from cv2 import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from  tensorflow.keras.models import load_model
import time
import os
import albumentations


def PredictResult(data_path):
    norm_size=224
    imagelist=[]
    emotion_labels ={0:'apple_healthy' ,1 :'apple_scab_general', 2:'apple_scab_serious', 3:'apple_frogeve_spot',4: 'cedar_apple_rust_general', 5:'cedar_apple_rust_serious', 6:'cherry_heealthy',
                7:'cherry_powdery_mildew_general',8: 'cherry_powdery_mildew_serious', 9:'corn_healthy', 10:'cercospora_zearmaydis_tehon_and_daniels_general',11: 'cercospora_zearmaydis_tehon_and_daniels_serious',
                12:'puccinia_polvsora_general', 13:'puccinia_polvsora_serious',14:'corn_curvularia_leaf_spot_fungus_general',
                15:'corn_curvularia_leaf_spot_fungus_serious' ,16 :'maize_dwarf_mosaic_virus' ,  17:'grape_healthy', 18:'grape_black_rot_fungus_general',
                19:'grape_black_rot_fungus_serios', 20:'grape_black_measles_fungus_general', 21:'grape_blacj_measles_fungus_serious', 22:'grape_leaf_blight_fungus_general',23: 'grape_leaf_blight_fungus_serious',
                24:'tomato_healthy0',25: 'citrus_greeninig_june_general', 26:'citrus_greening_june_serious', 27:'peach_healthy', 28:'peach_bacterial_general',29:'peach_bacterial_serious',
                30:'pepper_healthy',31:'pepper_scab_1',32:'pepper_scab_2', 33:'potato_healthy',34: 'potato_early_blight_fungus_1',35: 'potato_early_blight_fungus_2', 36:'potato_late_blight_fungus_1', 37:'potato_late_blight_fungus_2',
                38:'strawberry_0', 39:'strawberry_scorch_1',40: 'strawberry_scorch_2',41: 'tomato_0',42: 'tomato_powdery_mildgew_1', 43:'tomato_powdery_mildgew_2',44: 'tomato_early_1', 45:'tomato_early_2',46: 'tomato_late_1',
                47:'tomato_late_2',48:'tomato_leaf_1', 49:'tomato_leaf_2', 50:'tomato_spot_1',51:'tomato_spot_2', 52:'tomato_sep_1',53:'tomato_sep_2',54:'tomato_spider_1',
                55:'tomato_spider_2',56:'tomato_ylcv_1',57:'tomato_yclv_2',58:'tomato_tomv'}

    val_transform = albumentations.Compose([
            albumentations.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), max_pixel_value=255.0, p=1.0)
        ])
    emotion_classifier=load_model("D:/plantDisease.h5")

    image = cv2.imdecode(np.fromfile(data_path, dtype=np.uint8), -1)
    image = val_transform(image=image)['image']
    image = cv2.resize(image, (norm_size, norm_size), interpolation=cv2.INTER_LANCZOS4)
    image = img_to_array(image)
    imagelist.append(image)
    imageList = np.array(imagelist, dtype="float")

    pre=np.argmax(emotion_classifier.predict(imageList))
    emotion = emotion_labels[pre]

    print(emotion)
    return emotion
#