import os
from tqdm import tqdm
import shutil

def copyfile(src, dst):
    try:
        shutil.copy2(src, dst)
    except OSError as e:
        print('Error: %s' % e)

def image_extractor(directory_path, num_of_instances, save_path):
    class_instances = {'people': 0, 'vehicle': 0, 'bus': 0, 'truck': 0, 'motorcycle': 0, 'bicycle': 0, 'dog': 0, 'cat' : 0, 'train' : 0, 'trees' : 0, 'traffic_light' : 0, 'traffic_sign' : 0}
    class_prev_instance = {'prev_person' : 0, 'prev_vehicle' : 0, 'prev_bus' : 0, 'prev_truck' : 0, 'prev_motorcycle' : 0, 'prev_bicycle' : 0, 'prev_dog' : 0, 'prev_cat' : 0, 'prev_train' : 0, 'prev_trees' : 0, 'prev_traffic_light' : 0, 'prev_traffic_sign' : 0}
    class_images = {'people' : 0, 'vehicle' : 0, 'bus' : 0, 'truck' : 0, 'motorcycle' : 0, 'bicycle' : 0, 'dog' : 0, 'cat' : 0, 'train' : 0, 'trees' : 0, 'traffic_light' : 0, 'traffic_sign' : 0}
    number_of_instances = 30000 
    for file in tqdm(os.listdir(directory_path)):
        copy = False
        if file.endswith('.txt'):
            #read text file
            with open(os.path.join(directory_path, file), 'r') as l:
                lines = l.readlines()

            #write to a text file
            with open(os.path.join(save_path, file), 'w') as f:
            
                for line in lines:
                    string = line.split(' ')
                    class_number  = string[0]
                    if class_number == '0':
                        #class_instances['people'] += 1
                        if(class_instances['people'] <= number_of_instances):
                            class_instances['people'] += 1
                            #write line to file
                            line_to_write = line
                            f.write(line_to_write)

                    if class_number == '2':
                        #class_instances['vehicle'] += 1
                        if(class_instances['vehicle'] <= number_of_instances):
                            class_instances['vehicle'] += 1
                            #write line to file
                            line_to_write = line
                            f.write(line_to_write)

                    if class_number == '3':
                        #class_instances['bus'] += 1
                        if(class_instances['bus'] <= number_of_instances):
                            class_instances['bus'] += 1
                            #write line to file
                            line_to_write = line
                            f.write(line_to_write)


                    if class_number == '4':

                        if(class_instances['truck'] <= number_of_instances):
                            class_instances['truck'] += 1
                            #write line to file
                            line_to_write = line
                            f.write(line_to_write)


                    if class_number == '6':

                        if(class_instances['motorcycle'] <= number_of_instances):
                            class_instances['motorcycle'] += 1
                            #write line to file
                            line_to_write = line
                            f.write(line_to_write)


                    if class_number == '5':

                        if(class_instances['bicycle'] <= number_of_instances):
                            class_instances['bicycle'] += 1
                            #write line to file
                            line_to_write = line
                            f.write(line_to_write)


                    if class_number == '15':

                        if(class_instances['dog'] <= number_of_instances):
                            class_instances['dog'] += 1
                            #write line to file
                            line_to_write = line
                            f.write(line_to_write)

                    if class_number == '13':

                        if(class_instances['cat'] <= number_of_instances):
                            class_instances['cat'] += 1
                            #write line to file
                            line_to_write = line
                            f.write(line_to_write)


                    if class_number == '12':

                        if(class_instances['train'] <= number_of_instances):
                            class_instances['train'] += 1
                            #write line to file
                            line_to_write = line
                            f.write(line_to_write)


                    if class_number == '14':
                            
                        if(class_instances['trees'] <= number_of_instances):
                            class_instances['trees'] += 1
                            #write line to file
                            line_to_write = line
                            f.write(line_to_write)

                    if class_number == '7' or class_number == '8' or class_number == '9' or class_number == '10' :
                            
                        if(class_instances['traffic_light'] <= 40000):
                            class_instances['traffic_light'] += 1
                            #write line to file
                            line_to_write = line
                            f.write(line_to_write)


                    if class_number == '11' :    
                        if(class_instances['traffic_sign'] <= 40000):
                            class_instances['traffic_sign'] += 1
                            #write line to file
                            line_to_write = line
                            f.write(line_to_write)

            if(class_instances['people'] - class_prev_instance['prev_person'] > 0):
                class_images['people'] += 1
                class_prev_instance['prev_person'] = class_instances['people']
                copy = True


            if(class_instances['vehicle'] - class_prev_instance['prev_vehicle'] > 0):
                class_images['vehicle'] += 1
                class_prev_instance['prev_vehicle'] = class_instances['vehicle']
                copy = True

            if(class_instances['bus'] - class_prev_instance['prev_bus'] > 0):
                class_images['bus'] += 1
                class_prev_instance['prev_bus'] = class_instances['bus']
                copy = True

            if(class_instances['truck'] - class_prev_instance['prev_truck'] > 0):
                class_images['truck'] += 1
                class_prev_instance['prev_truck'] = class_instances['truck']
                copy = True

            if(class_instances['motorcycle'] - class_prev_instance['prev_motorcycle'] > 0):
                class_images['motorcycle'] += 1
                class_prev_instance['prev_motorcycle'] = class_instances['motorcycle']
                copy = True

            if(class_instances['bicycle'] - class_prev_instance['prev_bicycle'] > 0):
                class_images['bicycle'] += 1
                class_prev_instance['prev_bicycle'] = class_instances['bicycle']
                copy = True

            if(class_instances['dog'] - class_prev_instance['prev_dog'] > 0):
                class_images['dog'] += 1
                class_prev_instance['prev_dog'] = class_instances['dog']
                copy = True

            if(class_instances['cat'] - class_prev_instance['prev_cat'] > 0):
                class_images['cat'] += 1
                class_prev_instance['prev_cat'] = class_instances['cat']
                copy = True

            if(class_instances['train'] - class_prev_instance['prev_train'] > 0):
                class_images['train'] += 1
                class_prev_instance['prev_train'] = class_instances['train']
                copy = True

            if(class_instances['trees'] - class_prev_instance['prev_trees'] > 0):
                class_images['trees'] += 1
                class_prev_instance['prev_trees'] = class_instances['trees']
                copy = True

            if(class_instances['traffic_light'] - class_prev_instance['prev_traffic_light'] > 0):
                class_images['traffic_light'] += 1
                class_prev_instance['prev_traffic_light'] = class_instances['traffic_light']
                copy = True

            if(class_instances['traffic_sign'] - class_prev_instance['prev_traffic_sign'] > 0):
                class_images['traffic_sign'] += 1
                class_prev_instance['prev_traffic_sign'] = class_instances['traffic_sign']
                copy = True

            

            if(copy == True):
                #copy image to save path
                copyfile(os.path.join(directory_path, file.split('.')[0] + '.jpg'), os.path.join(save_path, file.split('.')[0] + '.jpg'))
                copy = False


    print(class_instances)
    print(class_images)



if __name__ == '__main__':
    directory_path = './open_image_resized/train/'
    save_path = './Final Dataset 2/train_motor/'
    image_extractor(directory_path, 20000, save_path)
                

