import pandas as pd
import os.path

# TODO: Modify with the name of the folder containing the images
IMAGE_DIR = "F:/Truck Tipper Tractor Data/open-images-v7/validation/data/"

# Classes tor train (TODO: Modify the names with the desired labels)
# WARNING: first letter should be UPPER case
#trainable_classes = ["Cat", "Dog", "Tree", "Train", "Motorcycle"]
trainable_classes = ["Truck"]
#trainable_classes = ["/m/04_sv"]
annotation_files = ["F:/Truck Tipper Tractor Data/open-images-v7/validation/labels/detections.csv"]


def SaveBoundingBoxToFile(image_id, label, x_min, x_max, y_min, y_max):

    #print("Saving bounding box to file")
    # Check that the image exist:
    # if os.path.isfile(IMAGE_DIR + image_id + '.jpg'):
        
    #     pass

    # else:
    if(trainable_codes.index(label) == 0):
        label_id = 1
        #Truck
        # If the label file exist, append the new bounding box
    if os.path.isfile(IMAGE_DIR + image_id + '.txt'):
        with open(IMAGE_DIR + image_id+".txt", 'a') as f:
            f.write(' '.join([str(label_id),
                                str(round((x_max+x_min)/2, 6)),
                                str(round((y_max+y_min)/2, 6)),
                                str(round(x_max-x_min, 6)),
                                str(round(y_max-y_min, 6))])+'\n')
    else:
        print("Creating file: " + IMAGE_DIR + image_id + '.txt')
        with open(IMAGE_DIR+image_id+".txt", 'w') as f:
            f.write(' '.join([str(label_id),
                                str(round((x_max+x_min)/2, 6)),
                                str(round((y_max+y_min)/2, 6)),
                                str(round(x_max-x_min, 6)),
                                str(round(y_max-y_min, 6))])+'\n')


if __name__ == '__main__':

    # Get the codes for the trainable classes
    class_descriptions = pd.read_csv(
        "F:/Truck Tipper Tractor Data/open-images-v7/validation/metadata/classes.csv", header=None)
    class_descriptions.to_csv("F:/Truck Tipper Tractor Data/open-images-v7/validation/metadata/classes_i.csv",
                              header=["Class id", "Class Name"], index=False)
    file2 = pd.read_csv("F:/Truck Tipper Tractor Data/open-images-v7/validation/metadata/classes_i.csv")
    trainable_codes = [code for code,
                       name in file2.values if name in trainable_classes]
    print(trainable_codes)
    print(file2.where(file2['Class id'].isin(trainable_codes)).dropna())
    # trainable_codes = [code for code,name in class_descriptions.values] # For ALL CLASSES
    for filename in annotation_files:

        # Read the train da
        filename = "F:/Truck Tipper Tractor Data/open-images-v7/validation/labels/detections.csv"
        df = pd.read_csv(filename)
        print("Dataset Loaded")

        # print(df)
        # Keep only the data for our training labels
        # Comment this line for ALL CLASSES
        df = df.loc[df['LabelName'].isin(trainable_codes)]
        print(df)
        # Save the bounding box data to the files
        df.apply(lambda x: SaveBoundingBoxToFile(x['ImageID'], x['LabelName'], x['XMin'], x['XMax'], x['YMin'], x['YMax']), axis=1)
