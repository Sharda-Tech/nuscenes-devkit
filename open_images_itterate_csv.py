import pandas as pd

class_df = pd.read_csv('classes.csv')

print(class_df.head())

#find class_id when class is 'Train'
y = class_df[class_df['Tortoise'] == 'Cat']

#convert y to list
y = y.values.tolist()

print(y[0][0])

class_id = y[0][0]

detection_df = pd.read_csv('detections_train.csv')
print(detection_df.head())

#count number of occurance of labelName class_id
counting = detection_df[detection_df['LabelName'] == class_id].count()
print(counting)