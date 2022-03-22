import cv2
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import load_model

df = pd.read_csv('dataset/ArSL_Data_Labels.csv')
label = LabelEncoder()
df['id'] = label.fit_transform(df['Class'])
def get_class(class_id):
        return df.loc[df['id'] == class_id, 'Class'].values[0]


model = load_model('Model/model.h5')

IMAGE_SIZE = 64
CROP_SIZE = 400

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    cv2.rectangle(frame, (0, 0), (CROP_SIZE, CROP_SIZE), (0, 255, 0), 3)
    

    cropped_image = frame[0:CROP_SIZE, 0:CROP_SIZE]
    resized_frame = cv2.resize(cropped_image, (IMAGE_SIZE, IMAGE_SIZE))
    reshaped_frame = (np.array(resized_frame)).reshape((1, IMAGE_SIZE, IMAGE_SIZE, 3))
    frame_for_model = reshaped_frame/255
    
    prediction = np.array(model.predict(frame_for_model))
    predicted_class = get_class(prediction.argmax())

    prediction_probability = prediction[0, prediction.argmax()]
    if prediction_probability > 0.5:
        cv2.putText(frame, '{} - {:.2f}%'.format(predicted_class, prediction_probability * 100), 
                                    (10, 450), 1, 2, (255, 255, 0), 2, cv2.LINE_AA)
    elif prediction_probability > 0.2 and prediction_probability <= 0.5:
        cv2.putText(frame, 'Maybe {}... - {:.2f}%'.format(predicted_class, prediction_probability * 100), 
                                    (10, 450), 1, 2, (0, 255, 255), 2, cv2.LINE_AA)


    cv2.imshow('frame', frame)

    # Press ESC to quit
    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()
