import os
from tqdm import tqdm

#read text file
def read_text_file(file_path):
    classes = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        class_name = line.split(' ')[0]
        classes.append(class_name)

    return classes

def convert_label_to_yolo(classes, path, save_path, img_height, img_width):
    for text_file in tqdm(os.listdir(path)):
        if text_file.endswith('.txt'):
            text_file_open_path = os.path.join(path, text_file)
            text_file_save_path = os.path.join(save_path, text_file)
            #write file to save_path
            with open(text_file_save_path, 'w') as f:
                #read text_file_open_path
                with open(text_file_open_path, 'r') as l:
                    lines = l.readlines()
                for line in lines:
                    class_number = ""
                    string = line.split(' ')
                    xmin = (round((int(string[1])/img_width), 6))
                    ymin = (round((int(string[2])/img_height),6))
                    xmax = (round((int(string[3])/img_width), 6))
                    ymax = (round((int(string[4])/img_height),6))
                    width = (round((xmax - xmin), 6))
                    height = (round((ymax - ymin), 6))
                    x_center = str(round((xmin + width/2), 6))
                    y_center = str(round((ymin + height/2), 6))
                    width = str(width)
                    height = str(height)

                    class_name = string[0]
                    #print(line)
                    if('bus' in class_name):
                        class_name = 'bus'
                        class_number = "3"

                    if('car' in class_name):
                        class_name = 'car'
                        class_number = "2"

                    if('pedestrian' in class_name):
                        class_name = 'pedestrian'
                        class_number = "0"

                    if('truck' in class_name or 'trailer' in class_name):
                        class_name = 'truck'
                        class_number = "4"

                    if('motorcycle' in class_name):
                        class_name = 'motorcycle'
                        class_number = "6"

                    if('vehicle.bicycle' == class_name):
                        class_name = 'bicycle'
                        class_number = "5"
                    
                    if class_number != "":
                        line_to_write = class_number + ' ' + x_center + ' ' + y_center + ' ' + width + ' ' + height + '\n'
                        f.write(line_to_write)
                    



if __name__ == '__main__':
    file_path = "class_name.txt"
    classes = read_text_file(file_path)
    print(classes)
    output = "./output_test"
    img_height = 900
    img_width = 1600
    save_path = './test_label_yolo_nuimages'
    convert_label_to_yolo(classes, output, save_path,  img_height, img_width)

