import cv2
import os

path_exp = './exp23/'
path_exp_label = './exp23/labels/'
path_valid_label = './valid_labels/'
label = ['People', ' ' , 'Vehicle', 'Bus', 'Truck',  'Bicycle', 'Motorcycle', 'Traffic Light', 'Traffic Light', 'Traffic Light', 'Traffic Light', 'Traffic Sign', 'Train', 'Cat', ' ', 'Dog']
colors = [(56, 56, 255),(31, 112, 255),(29, 178, 255),(49, 210, 207),(10, 249, 72),(23, 204, 146),(134, 219, 61),(255, 194, 0),(147, 69, 52),(255, 115, 100),(255, 56, 132)]
label_2 = ['People','Vehicle', 'Bus', 'Truck',  'Bicycle', 'Motorcycle', 'Traffic Light','Traffic Sign', 'Train', 'Cat', 'Dog']
frames = []
t = 0
acum_map = 0
num_im = 0
total_true_positive = 0
total_false_positive = 0
number_of_detection = 0
total_false_negative = 0
num_of_detection_exp = 0
for file in os.listdir(path_exp):
    label_used = []
    num_of_detection_exp = 0
    number_of_detection = 0
    total_true_positive = 0
    total_false_positive = 0
    total_false_negative = 0
    false_positive = 0
    false_negative = 0
    if(t < 10):
        t+=1
        precision = []
        mAP = 0
        no_of_classes = 0
        if file.endswith('.png') or file.endswith('.jpg'):
            
            num_im+=1
            label_path = os.path.join(path_exp_label, file.split('.')[0] + '.txt')
            #print(label_path)
            if os.path.exists(label_path):
                print("Exp Label Found")
                #read text file
                with open(label_path, 'r') as l:
                    lines = l.readlines()
                class_list = []
                occurance_list = []
                for line in lines:
                    num_of_detection_exp += 1
                    class_name = line.split(' ')[0]
                    #print(class_name)
                    if class_name not in class_list:
                        occur_dict = {class_name : 1}
                        class_list.append(class_name)
                        occurance_list.append(occur_dict)
                    else:
                        occurance_list[class_list.index(class_name)][class_name] += 1


            original_label_path = os.path.join(path_valid_label, file.split('.')[0] + '.txt')

            if os.path.exists(original_label_path):
                # print("Valid Label Found")
                #read text file
                with open(original_label_path, 'r') as l:
                    lines = l.readlines()
                org_class_list = []
                org_occurance_list = []
                for line in lines:
                    number_of_detection += 1
                    class_name = line.split(' ')[0]
                    #print(class_name)
                    if class_name not in org_class_list:
                        org_occur_dict = {class_name : 1}
                        org_class_list.append(class_name)
                        org_occurance_list.append(org_occur_dict)
                    else:
                        org_occurance_list[org_class_list.index(class_name)][class_name] += 1

                print("File name is:", file)
                print("Occurance", occurance_list)
                print("Original Occurance", org_occurance_list)


            
            prec = {}
            for org_occur in org_occurance_list:
                found = False
                true_negative = 0
                for occur in occurance_list:
                    if org_occur.keys() == occur.keys():
                        found = True
                        #value of org_occur
                        org_occur_value = org_occur.values()
                        #convert org_occur_value to int
                        org_occur_value = list(map(int, org_occur_value))[0]
                        #value of occur
                        occur_value = occur.values()
                        #convert occur_value to int
                        occur_value = list(map(int, occur_value))[0]
                        if(occur_value >= org_occur_value):
                            true_positive = org_occur_value
                            false_positive = occur_value - org_occur_value

                        elif(occur_value < org_occur_value):
                            true_positive = occur_value
                            false_negative = org_occur_value - occur_value

                        

                        #convert org_occur.keys() to int
                        no_of_detection = occur_value
                        org_occur_keys = list(map(int, org_occur.keys()))
                        prec = {org_occur_keys[0] : true_positive/occur_value}
                        precision.append(prec.copy())



                if found == False:
                    
                    org_occur_keys = list(map(int, org_occur.keys()))[0]
                    org_occur_value = org_occur.values()
                    #convert org_occur_value to int
                    org_occur_value = list(map(int, org_occur_value))[0]
                    prec = {org_occur_keys: 0}
                    precision.append(prec.copy())
                    false_negative = org_occur_value

                for occ in occurance_list:
                    if org_occur.keys() == occ.keys():
                        continue
                    else:
                        occur_value = occ.values()
                        #convert occur_value to int
                        occur_value = list(map(int, occur_value))[0]
                        true_negative = true_negative + occur_value
                        

                print("True Negative", true_negative)
                label_name = label[org_occur_keys[0]]
                #print("Label Name:", label_name)
                list_of_values = [no_of_detection,true_positive, true_negative, false_negative, false_positive]
                label_dict = {label_name : list_of_values}
                label_used.append(label_dict.copy())



                total_true_positive += true_positive
                total_false_positive = num_of_detection_exp - total_true_positive
                total_false_negative += false_negative
                #total_true_negative = num_of_detection_exp - total_false_negative

            print("Precision", precision)
            img = cv2.imread(os.path.join(path_exp, file))
            #resize image
            img = cv2.resize(img, (1024, 768))
            #add black border to image
            img = cv2.copyMakeBorder(img, 100, 100, 400, 300, cv2.BORDER_CONSTANT, value=[0, 0, 0])
            print(img.shape)
            
        
            label_prec = []
            for p in precision:
                index = list(p.keys())[0]
                #print(index)
                label_name = label[index]
                #print(label_name)
                dict_prec = {label_name : list(p.values())[0]}
                label_prec.append(dict_prec.copy())
                no_of_classes = no_of_classes + 1
                mAP = mAP + list(map(float, p.values()))[0]
                print(mAP)
            
            mAP = mAP/no_of_classes
            #restirct maP to 2 decimal places
            mAP = round(mAP, 2)
            # print("mAP", mAP)
            print("Label Precision", label_prec)
            acum_map = acum_map + mAP
            # cv2.putText(img, "Number of Detections", (130, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            # cv2.putText(img, "TP", (350, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            # cv2.putText(img, "TN", (400, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            # cv2.putText(img, "FN", (450, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            # cv2.putText(img, "FP", (500, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            cv2.putText(img, "No. of Detections", (50, 670), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            cv2.putText(img, "TP", (200, 670), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            cv2.putText(img, "TN", (230, 670), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            cv2.putText(img, "FN", (260, 670), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            cv2.putText(img, "FP", (290, 670), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            # cv2.imshow("ss",img)
            # cv2.waitKey(0)
            h = 700
            h_c = 500
            cv2.putText(img, "Legend", (1500, h_c-50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            for j in label_2:
                label_name = j
                print(label_name)
                index = label_2.index(label_name)
                color = colors[index]
                #draw rectangle of size 30x30
                cv2.rectangle(img, (1450, h_c), (1470, h_c+20), color, -1)
                #write label name
                cv2.putText(img, label_name, (1500, h_c+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
                h_c += 40


            for ll in label_2:
                #write the label name
                value = ll
                list_of_bool = [True for elem in label_used 
                    if value in elem.keys()]
                
                #index of ll in label_2
                index = label_2.index(ll)
                color = colors[index]
                if list_of_bool:
                    for kh in label_used:
                        if value in kh.keys():
                            cv2.putText(img, ll, (0, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                            cv2.putText(img, str(list(kh.values())[0][0]), (100, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2,)
                            cv2.putText(img, str(list(kh.values())[0][1]), (200, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                            cv2.putText(img, str(list(kh.values())[0][2]), (230, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                            cv2.putText(img, str(list(kh.values())[0][3]), (260, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                            cv2.putText(img, str(list(kh.values())[0][4]), (290, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
                else:
                    cv2.putText(img, ll, (0, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    cv2.putText(img, "NA", (100, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    cv2.putText(img, "NA", (200, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    cv2.putText(img, "NA", (230, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    cv2.putText(img, "NA", (260, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    cv2.putText(img, "NA", (290, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                h=h+20
            cv2.putText(img, "Total Detections", (0, h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            cv2.putText(img, str(num_of_detection_exp), (200, h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            h=0
            for l in label_prec:
                h+=30
                label_name = list(l.keys())[0]
                label_prec = list(l.values())[0]
                #index of label_name in label_2
                index = label_2.index(label_name)
                cv2.putText(img, "AP50 " + str(label_name) + " " + str(round(float(label_prec),2)), (1500, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                color = colors[index]


           

            cv2.putText(img, "Accumulated mAP50", (750, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            cv2.putText(img, str(round((acum_map/num_im),2)), (850, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            #put text in img at left top corner
            cv2.putText(img, "mAP50", (200, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            cv2.putText(img, str(mAP), (225, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            # cv2.putText(img, "Number of Detections", (10, 570), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            # cv2.putText(img, str(number_of_detection), (400, 570), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            # cv2.putText(img, "Total True Positive", (10, 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            # cv2.putText(img, str(total_true_positive), (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            # # cv2.putText(img, "Total True Negative", (10, 630), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            # # cv2.putText(img, str(total_true_negative), (400, 630), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            # cv2.putText(img, "Total False Negative", (10, 660), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            # cv2.putText(img, str(total_false_negative), (400, 660), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            # cv2.putText(img, "Total False Positive", (10, 690), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            # cv2.putText(img, str(total_false_positive), (400, 690), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

            #view image
            # cv2.imshow(file, img)
            # cv2.waitKey(1000)
            # cv2.destroyAllWindows()
            if frames is not None:
                frames.append(img)

            else:
                frames = img


    else:
        break

#create video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('mAP.avi', fourcc, 20.0, img.shape[1::-1])
for frame in frames:
    k = 0
    while k < 20:
        out.write(frame)
        k+=1
out.release()


                    
                
                    



        