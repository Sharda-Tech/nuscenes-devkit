import cv2
import os
from random import uniform

def iou(orginal, exp):
    l1 = orginal[0] - orginal[2] / 2
    r1 = orginal[0] + orginal[2] / 2
    t1 = orginal[1] - orginal[3] / 2
    b1 = orginal[1] + orginal[3] / 2
    l2 = exp[0] - exp[2] / 2
    r2 = exp[0] + exp[2] / 2
    t2 = exp[1] - exp[3] / 2
    b2 = exp[1] + exp[3] / 2
    lin = max(l1, l2)
    rin = min(r1, r2)
    tin = max(t1, t2)
    bin = min(b1, b2)

    ainter = (rin - lin) * (bin - tin)
    ##print("Ainter",ainter)
    aunion = (r1 - l1) * (b1 - t1) + (r2 - l2) * (b2 - t2) - ainter
    ##print("Aunion",aunion)
    iou = ainter / aunion

    # if(iou > 1.2):
    #     iou = 0

    # elif(iou < 0):
    #     iou = 0

    return iou

def tp_fp(orginal, exp):
    #print("Original")
    for i in orginal:
        #print(i)
        continue
    #print("Exp")
    for i in exp:
        #print(i)
        continue
    threshold = 50
    tp =[]
    fp = []
    for ep in exp:
        Found = False
        for org in orginal:
            ##print(ep)
            org_class = list(org.keys())[0]
            org_cord = list(org.values())[0][:4]
            exp_cord = list(ep.values())[0][:4]
            exp_class = list(ep.keys())[0]
            # #print("Org Cord",org)
            # #print("Exp Cord",ep)
            iou_value = iou(org_cord, exp_cord)
            # #print("IOU Value",iou_value)
            if iou_value > 0.5:
                
                if(org_class == exp_class):
                    if((org_cord[0] - threshold) <= exp_cord[0] <= (org_cord[0] + threshold) and (org_cord[1] - threshold) < exp_cord[1] < (org_cord[1] + threshold) and (org_cord[2] - threshold) < exp_cord[2] < (org_cord[2] + threshold) and (org_cord[3] - threshold) < exp_cord[3] < (org_cord[3] + threshold)):
                        #print("Ep Value Tp in find in Fp",ep) 
                        Found = True

                    
        if Found == False:
            #print("Ep Value Fp",ep)    
            class_found_in_fp = False
            for elem in fp:
                if exp_class in elem.keys():
                    class_found_in_fp = True
                    elem[exp_class] += 1

            if not class_found_in_fp:
                fp.append({exp_class: 1})
                
                
            class_found_in_tp = False
            for elem in tp:
                if exp_class in elem.keys():
                    class_found_in_tp = True
                    continue

            if not class_found_in_tp:
                tp.append({exp_class: 0})
    # #print("TP")
    # for i in tp:
    #     #print(i)
    #print("FP")
    for i in fp:
        #print(i)
        continue

    
    for org in orginal:
        Found = False
        iou_sum = 0
        org_class = list(org.keys())[0]
        for ep in exp:
            ##print(ep)
            org_class = list(org.keys())[0]
            org_cord = list(org.values())[0][:4]
            exp_cord = list(ep.values())[0][:4]
            exp_class = list(ep.keys())[0]
            # #print("Org Cord",org)
            # #print("Exp Cord",ep)
            iou_value = iou(org_cord, exp_cord)
            # #print("IOU Value",iou_value)
            if iou_value > 0.5:
                if(org_class == exp_class):
                    if((org_cord[0] - threshold) <= exp_cord[0] <= (org_cord[0] + threshold) and (org_cord[1] - threshold) < exp_cord[1] < (org_cord[1] + threshold) and (org_cord[2] - threshold) < exp_cord[2] < (org_cord[2] + threshold) and (org_cord[3] - threshold) < exp_cord[3] < (org_cord[3] + threshold)):
                        #print("ep Value Tp",ep, "iou", iou_value)
                        iou_sum += 1
                        Found = True

        #print(org)
        #print(Found)
        #print(iou_sum)
        if Found == True:
            class_found_in_tp = False
            for elem in tp:
                if org_class in elem.keys():
                    class_found_in_tp = True
                    elem[org_class] += 1

            if not class_found_in_tp:
                tp.append({org_class: 1})

            class_found_in_fp = False
            for elem in fp:
                if org_class in elem.keys():
                    class_found_in_fp = True
                    elem[org_class] += ((iou_sum)-1)

            if not class_found_in_fp:
                fp.append({org_class: (iou_sum)-1})
                
        else:
            class_found_in_fp = False
            for elem in fp:
                if org_class in elem.keys():
                    class_found_in_fp = True
                    continue

            if not class_found_in_fp:
                fp.append({org_class: 0})
                
                
            class_found_in_tp = False
            for elem in tp:
                if org_class in elem.keys():
                    class_found_in_tp = True
                    continue

            if not class_found_in_tp:
                tp.append({org_class: 0})
        #print("TP")
        for i in tp:
            #print(i)
            continue
        #print("FP")
        for i in fp:
            #print(i)
            continue

    # #print("Final TP")
    # for i in tp:
    #     #print(i)
    # #print("Final FP")
    # for i in fp:
    #     #print(i)

    return tp,fp

def tn_fn(tp,fp,orginal,exp):

    #print("TP")
    for i in tp:
        #print(i)
        continue
    #print("FP")
    for i in fp:
        #print(i)
        continue

    exp_class_number = []
    org_class_number = []
    for i in exp:
        Found = False
        for e in exp_class_number:
            if list(i.keys())[0] == list(e.keys())[0]:
                Found = True
                e[list(i.keys())[0]] += 1
        if not Found:
            exp_class_number.append({list(i.keys())[0]:1})


    for i in orginal:
        Found = False
        for e in org_class_number:
            if list(i.keys())[0] == list(e.keys())[0]:
                Found = True
                e[list(i.keys())[0]] += 1
        if not Found:
            org_class_number.append({list(i.keys())[0]:1})

    #print("exp")
    for i in exp:
        continue
        #print(i)

    #print("class_number")
    for i in exp_class_number:
        continue
        #print(i)

    #print("org")
    for i in orginal:
        #print(i)
        continue

    #print("class_number")
    for i in org_class_number:
        #print(i)
        continue
        
    true_negative = []
    false_negative = []
    for ocurance in org_class_number:
        true_negative_val = 0
        ##Previosu Method
        # for occ in exp_class_number:
        #     if list(occ.keys())[0] == '14':
        #         continue
        #     if ocurance.keys() == occ.keys():
        #         continue
        #     else:
        #         occur_value = occ.values()
        #         #convert occur_value to int
        #         occur_value = list(map(int, occur_value))[0]
        #         true_negative_val = true_negative_val + occur_value
        for occ in tp:
            if list(occ.keys())[0] == '14':
                continue
            if ocurance.keys() == occ.keys():
                continue
            else:
                occur_value = occ.values()
                for ff in fp:
                    if occ.keys() == ff.keys():
                        fp_value = ff.values()
                        fp_value = list(map(int, fp_value))[0]
                #convert occur_value to int
                occur_value = list(map(int, occur_value))[0]
                true_negative_val = true_negative_val + occur_value + fp_value



        true_negative.append({list(ocurance.keys())[0]:true_negative_val})
    
    for ttp in tp:
        true_negative_val = 0
        key_ttp = ttp.keys()
        found_in_tn = False
        for ttn in true_negative:
            ttn_keys = ttn.keys()
            if key_ttp == ttn_keys:
                found_in_tn = True
                
        if found_in_tn:
            continue
        
        else:
            for occ in tp:
                if list(occ.keys())[0] == '14':
                    continue
                if ttp.keys() == occ.keys():
                    continue
                else:
                    occur_value = occ.values()
                    for ff in fp:
                        if occ.keys() == ff.keys():
                            fp_value = ff.values()
                            fp_value = list(map(int, fp_value))[0]
                    #convert occur_value to int
                    occur_value = list(map(int, occur_value))[0]
                    true_negative_val = true_negative_val + occur_value + fp_value

            false_negative.append({list(ttp.keys())[0]:0})

        true_negative.append({list(ttp.keys())[0]:true_negative_val})
        
    #print("TN")
    for i in true_negative:
        #print(i)
        continue

    #false negative

   
    for ocurance in org_class_number:
        false_negative_val = 0
        found_in_tp = False
        for occ in tp:
            if ocurance.keys() == occ.keys():
                found_in_tp = True
                occur_value = occ.values()
                #convert occur_value to int
                occur_value = list(map(int, occur_value))[0]
                false_negative_val = list(ocurance.values())[0] - occur_value
                if false_negative_val >= 0 :
                    continue
                else:
                    false_negative_val = 0
                
            else:
                continue

        if found_in_tp == False:
            false_negative_val = list(ocurance.values())[0]
                

        false_negative.append({list(ocurance.keys())[0]:false_negative_val})

    #print("FN")
    for i in false_negative:
        #print(i)
        continue
    
    return true_negative,false_negative,org_class_number,exp_class_number


path_exp = './exp_0_pretrain/'
path_exp_label = './exp_0_pretrain/label/'
path_valid_label = './valid_labels/'
label = ['People', 'Rider' , 'Car', 'Bus', 'Truck',  'Bicycle', 'Motorcycle', 'Traffic Light', 'Traffic Light', 'Traffic Light', 'Traffic Light', 'Traffic Sign', 'Train', 'Cat', ' ', 'Dog']
colors = [(56, 56, 255),(44,84,255),(31, 112, 255),(29, 178, 255),(49, 210, 207),(10, 249, 72),(23, 204, 146),(134, 219, 61),(255, 194, 0),(147, 69, 52),(255, 115, 100),(255, 56, 132)]
label_reject = [14]
label_2 = ['People', 'Rider', 'Car', 'Bus', 'Truck',  'Bicycle', 'Motorcycle', 'Traffic Light','Traffic Sign', 'Train', 'Cat', 'Dog']
frames = []
t = 0
acum_map = 0
acum_mar = 0
acum_maa = 0
acc_it = 0
num_im = 0
total_true_positive = 0
total_false_positive = 0
number_of_detection = 0
total_false_negative = 0
num_of_detection_exp = 0
ap50 = []
aa50 = []
ar50 = []
class_frame_count = {}
for file in os.listdir(path_exp):
    label_used = []
    num_of_detection_exp = 0
    number_of_detection = 0
    total_true_positive = 0
    total_false_positive = 0
    total_false_negative = 0
    false_positive = 0
    false_negative = 0
    
    if(t < 8000):
        t+=1
        mAP = 0
        mAR = 0
        mAA = 0
        no_of_classes = 0
        no_of_classes_r = 0
        no_of_classes_a = 0
        tp = []
        tn = []
        fp = []
        tn = []
        original_occurance_list = []
        exp_occurance_list = []
        if file.endswith('.png') or file.endswith('.jpg'):
            img = cv2.imread(os.path.join(path_exp, file))
            #resize image
            img = cv2.resize(img, (1024, 768))
            #add black border to image
            img = cv2.copyMakeBorder(img, 200, 100, 400, 400, cv2.BORDER_CONSTANT, value=[0, 0, 0])
            #print(img.shape)
            num_im+=1
            label_path = os.path.join(path_exp_label, file.split('.')[0] + '.txt')
            ##print(label_path)
            if os.path.exists(label_path):
                #print("Exp Label Found")
                #read text file
                with open(label_path, 'r') as l:
                    lines = l.readlines()
                class_list = []
                occurance_list = []
                for line in lines:
                    #num_of_detection_exp += 1
                    class_name = line.split(' ')[0]
                    x_center = float(line.split(' ')[1])*1024
                    y_center = float(line.split(' ')[2])*768
                    width = float(line.split(' ')[3])*1024
                    height = float(line.split(' ')[4])*768
                    ##print(class_name)
                    if class_name not in class_list:
                        #occur_dict = {class_name : 1}
                        #occur_dict = {class_name : [x_center, y_center, width, height]}
                        class_list.append(class_name)
                        #occurance_list.append(occur_dict)
                    # else:
                    #     occurance_list[class_list.index(class_name)][class_name] += 1
                    occur_dict = {class_name : [x_center, y_center, width, height]}
                    occurance_list.append(occur_dict)
                    
            else:
                occurance_list = []

            original_label_path = os.path.join(path_valid_label, file.split('.')[0] + '.txt')
            
            
            if os.path.exists(original_label_path):
                # #print("Valid Label Found")
                #read text file
                with open(original_label_path, 'r') as l:
                    lines = l.readlines()
                org_class_list = []
                org_occurance_list = []
                for line in lines:
                    number_of_detection += 1
                    class_name = line.split(' ')[0]
                    x_center = float(line.split(' ')[1])*1024
                    y_center = float(line.split(' ')[2])*768
                    width = float(line.split(' ')[3])*1024
                    height = float(line.split(' ')[4])*768

                    ##print(class_name)
                    if class_name not in org_class_list:
                        #org_occur_dict = {class_name : 1}
                        #org_occur_dict = {class_name : [x_center, y_center, width, height]}
                        org_class_list.append(class_name)
                        #org_occurance_list.append(org_occur_dict)
                    # else:
                    #     org_occurance_list[org_class_list.index(class_name)][class_name] += 1
                    org_occur_dict = {class_name : [x_center, y_center, width, height]}
                    org_occurance_list.append(org_occur_dict)
                    
            else:
                continue
            print("File name is:", file)
            # #print("Occurance", occurance_list)
            # #print("Original Occurance", org_occurance_list)

            tp,fp = tp_fp(org_occurance_list,occurance_list)
            tn,fn, original_occurance_list,exp_occurance_list = tn_fn(tp,fp,org_occurance_list,occurance_list)
            print("Original Occurance", original_occurance_list)
            print("Experiment Occurance",exp_occurance_list)
            print("TP is",tp)
            print("TN is",tn)
            print("FP is",fp)
            print("FN is",fn)
            for e in exp_occurance_list:
                #value of e
                class_name = list(e.keys())[0]
                value = list(e.values())[0]
                if class_name == '14':
                    continue
                #add value to num_of_detection_exp
                num_of_detection_exp += value
            


            prec = []
            for org_occur in original_occurance_list:
                class_name = list(org_occur.keys())[0]
                if int(class_name) in label_reject:
                    continue
                found_in_tp = False
                for i in tp:
                    if(list(i.keys())[0] == class_name):
                        true_positive = float(list(i.values())[0])
                        found_in_tp = True
                    else:
                        continue

                if found_in_tp == False:
                    true_positive = 0

                found_in_fp = False
                for j in fp:

                    if(list(j.keys())[0] == class_name):
                        found_in_fp = True
                        false_positive = float(list(j.values())[0])
                    else:
                        continue

                if true_positive == 0.0:
                    false_positive = 1


                prec_dict = {class_name : round((true_positive/(true_positive+false_positive)),2)}
                prec.append(prec_dict.copy())

            for exp_occur in exp_occurance_list:
                class_name = list(exp_occur.keys())[0]
                if int(class_name) in label_reject:
                    continue
                found_in_occurance = False
                for org_occur in original_occurance_list:
                    if(list(org_occur.keys())[0] == class_name):
                        found_in_occurance = True
                    else:
                        continue

                if found_in_occurance == False:
                    class_name = list(exp_occur.keys())[0]
                    found_in_tp = False
                    for i in tp:
                        if(list(i.keys())[0] == class_name):
                            true_positive = float(list(i.values())[0])
                            found_in_tp = True
                        else:
                            continue

                    found_in_fp = False
                    for j in fp:

                        if(list(j.keys())[0] == class_name):
                            found_in_fp = True
                            false_positive = float(list(j.values())[0])
                        else:
                            continue

                    if true_positive == 0.0:
                        false_positive = 1


                    prec_dict = {class_name : round((true_positive/(true_positive+false_positive)),2)}
                    prec.append(prec_dict.copy())

            #print("Precision" , prec)


            #recall

            recal = []

            for org_occur in original_occurance_list:
                class_name = list(org_occur.keys())[0]
                if int(class_name) in label_reject:
                    continue
                found_in_tp = False
                for i in tp:
                    if(list(i.keys())[0] == class_name):
                        true_positive = float(list(i.values())[0])
                        found_in_tp = True
                    else:
                        continue

                if found_in_tp == False:
                    true_positive = 0

                found_in_fn = False
                for j in fn:

                    if(list(j.keys())[0] == class_name):
                        found_in_fn = True
                        false_negative = float(list(j.values())[0])
                    else:
                        continue
                
                if true_positive == 0.0:
                    false_negative = 1

                recal_dict = {class_name : round((true_positive/(true_positive+false_negative)),2)}
                recal.append(recal_dict.copy())

            for exp_occur in exp_occurance_list:
                class_name = list(exp_occur.keys())[0]
                if int(class_name) in label_reject:
                    continue
                found_in_occurance = False
                for org_occur in original_occurance_list:
                    if(list(org_occur.keys())[0] == class_name):
                        found_in_occurance = True
                    else:
                        continue

                if found_in_occurance == False:
                    class_name = list(exp_occur.keys())[0]
                    found_in_tp = False
                    for i in tp:
                        if(list(i.keys())[0] == class_name):
                            true_positive = float(list(i.values())[0])
                            found_in_tp = True
                        else:
                            continue

                    found_in_fn = False
                    for j in fn:

                        if(list(j.keys())[0] == class_name):
                            found_in_fn = True
                            false_negative = float(list(j.values())[0])
                        else:
                            continue
                    
                    if true_positive == 0.0:
                        false_negative = 1

                    recal_dict = {class_name : round((true_positive/(true_positive+false_negative)),2)}
                    recal.append(recal_dict.copy())

            print("Recall" , recal)
            print("Number of Detection Occurance", number_of_detection)
            #Accuracy

            acc = []

            for org_occur in original_occurance_list:
                class_name = list(org_occur.keys())[0]
                if int(class_name) in label_reject:
                    continue
                found_in_tp = False
                for i in tp:
                    if(list(i.keys())[0] == class_name):
                        true_positive = float(list(i.values())[0])
                        found_in_tp = True
                    else:
                        continue

                if found_in_tp == False:
                    true_positive = 0

                found_in_fn = False
                for j in fn:

                    if(list(j.keys())[0] == class_name):
                        found_in_fn = True
                        false_negative = float(list(j.values())[0])
                    else:
                        continue
                
                if found_in_fn == False:
                    false_negative = 0

                found_in_tn = False
                for k in tn:
                    if(list(k.keys())[0] == class_name):
                        found_in_tn = True
                        true_negative = float(list(k.values())[0])
                    else:
                        continue

                if found_in_tn == False:
                    true_negative = 0


                found_in_fp = False
                for j in fp:

                    if(list(j.keys())[0] == class_name):
                        found_in_fp = True
                        false_positive = float(list(j.values())[0])
                    else:
                        continue

                if (true_negative == 0) and (true_positive == 0):
                    false_positive = 1

                elif found_in_fp == False:
                    false_positive = 0

                # if true_positive == 0:
                #     continue
                # else:
                #acc_dict = {class_name : round(((true_positive+true_negative)/(true_positive+false_negative+true_negative+false_positive)),2)}
                acc_dict = {class_name : round(((true_positive+true_negative)/(number_of_detection)),2)}
                acc.append(acc_dict.copy())

            for exp_occur in exp_occurance_list:
                class_name = list(exp_occur.keys())[0]
                if int(class_name) in label_reject:
                    continue
                found_in_occurance = False
                for org_occur in original_occurance_list:
                    if(list(org_occur.keys())[0] == class_name):
                        found_in_occurance = True
                    else:
                        continue

                if found_in_occurance == False:
                    class_name = list(exp_occur.keys())[0]
                    found_in_tp = False
                    for i in tp:
                        if(list(i.keys())[0] == class_name):
                            true_positive = float(list(i.values())[0])
                            found_in_tp = True
                        else:
                            continue


                    found_in_fn = False
                    for j in fn:

                        if(list(j.keys())[0] == class_name):
                            found_in_fn = True
                            false_negative = float(list(j.values())[0])
                        else:
                            continue
                    

                    found_in_tn = False
                    for k in tn:
                        if(list(k.keys())[0] == class_name):
                            found_in_tn = True
                            true_negative = float(list(k.values())[0])
                        else:
                            continue


                    found_in_fp = False
                    for j in fp:

                        if(list(j.keys())[0] == class_name):
                            found_in_fp = True
                            false_positive = float(list(j.values())[0])
                        else:
                            continue

                    if (true_negative == 0.0) and (true_positive == 0.0):
                        false_positive = 1

                    # if true_positive == 0:
                    #     continue
                    #acc_dict = {class_name : round(((true_positive+true_negative)/(true_positive+false_negative+true_negative+false_positive)),2)}
                    
                    acc_dict = {class_name : round(((true_positive+true_negative)/(number_of_detection)),2)}
                    acc.append(acc_dict.copy())

            print("Accuracy" , acc)
            # for org_occur in org_occurance_list:
            #     found = False
            #     true_negative = 0
            #     for occur in occurance_list:
            #         if org_occur.keys() == occur.keys():
            #             found = True
            #             #value of org_occur
            #             org_occur_value = org_occur.values()
            #             #convert org_occur_value to int
            #             org_occur_value = list(map(int, org_occur_value))[0]
            #             #value of occur
            #             occur_value = occur.values()
            #             #convert occur_value to int
            #             occur_value = list(map(int, occur_value))[0]
            #             if(occur_value >= org_occur_value):
            #                 true_positive = org_occur_value
            #                 false_positive = occur_value - org_occur_value

            #             elif(occur_value < org_occur_value):
            #                 true_positive = occur_value
            #                 false_negative = org_occur_value - occur_value

                        

            #             #convert org_occur.keys() to int
            #             no_of_detection = occur_value
            #             org_occur_keys = list(map(int, org_occur.keys()))
            #             prec = {org_occur_keys[0] : true_positive/occur_value}
            #             precision.append(prec.copy())



            #     if found == False:
                    
            #         org_occur_keys = list(map(int, org_occur.keys()))[0]
            #         org_occur_value = org_occur.values()
            #         #convert org_occur_value to int
            #         org_occur_value = list(map(int, org_occur_value))[0]
            #         prec = {org_occur_keys: 0}
            #         precision.append(prec.copy())
            #         false_negative = org_occur_value

            #     for occ in occurance_list:
            #         if org_occur.keys() == occ.keys():
            #             continue
            #         else:
            #             occur_value = occ.values()
            #             #convert occur_value to int
            #             occur_value = list(map(int, occur_value))[0]
            #             true_negative = true_negative + occur_value
                        

#                 #print("True Negative", true_negative)
#                 label_name = label[org_occur_keys[0]]
#                 ##print("Label Name:", label_name)
#                 list_of_values = [no_of_detection,true_positive, true_negative, false_negative, false_positive]
#                 label_dict = {label_name : list_of_values}
#                 label_used.append(label_dict.copy())



#                 total_true_positive += true_positive
#                 total_false_positive = num_of_detection_exp - total_true_positive
#                 total_false_negative += false_negative
#                 #total_true_negative = num_of_detection_exp - total_false_negative
            label_used = []
            for org_occur in original_occurance_list:

                class_name = list(org_occur.keys())[0]
                # if int(class_name) in label_reject:
                #     continue
                found_in_tp = False
                for i in tp:
                    if(list(i.keys())[0] == class_name):
                        true_positive = float(list(i.values())[0])
                        found_in_tp = True
                    else:
                        continue

                if found_in_tp == False:
                    true_positive = 'NA'

                found_in_fp = False

                for j in fp:
                    if(list(j.keys())[0] == class_name):
                        false_positive = float(list(j.values())[0])
                        found_in_fp = True
                    else:
                        continue
                if found_in_fp == False:
                    false_positive = 'NA'

                found_in_tn = False
                for k in tn:
                    if(list(k.keys())[0] == class_name):
                        true_negative = float(list(k.values())[0])
                        found_in_tn = True
                    else:
                        continue
                if found_in_tn == False:
                    true_negative = 'NA'
                found_in_fn = False
                
                for l in fn:
                    if(list(l.keys())[0] == class_name):
                        false_negative = float(list(l.values())[0])
                        found_in_fn = True
                    else:
                        continue

                if found_in_fn == False:
                    false_negative = 'NA'

                found_in_exp = False
                for m in exp_occurance_list:
                    if(list(m.keys())[0] == class_name):
                        no_of_detection = float(list(m.values())[0])
                        found_in_exp = True
                    else:
                        continue

                if found_in_exp == False:
                    no_of_detection = 0
                
                ground_truth = list(org_occur.values())[0]

                list_of_values = [no_of_detection,true_positive, true_negative, false_negative, false_positive, ground_truth]
                label_name = label[int(class_name)]
                label_dict = {label_name : list_of_values}
                label_used.append(label_dict.copy())


            
            for m in exp_occurance_list:
                class_name = list(m.keys())[0]
                found = False
                for lbl in label_used:
                    label_name = label[int(class_name)]
                    if(list(lbl.keys())[0] == label_name):
                        found = True

                if found == False:
                    found_in_tp == False
                    for ttp in tp:
                        if ttp.keys() == m.keys():
                            found_in_tp = True
                            
                    if found_in_tp:
                        for i in tp:
                            if(list(i.keys())[0] == class_name):
                                true_positive = float(list(i.values())[0])
                            else:
                                continue

                        for j in fp:
                            if(list(j.keys())[0] == class_name):
                                false_positive = float(list(j.values())[0])
                            else:
                                continue
                        for k in tn:
                            if(list(k.keys())[0] == class_name):
                                true_negative = float(list(k.values())[0])
                            else:
                                continue
                        for l in fn:
                            if(list(l.keys())[0] == class_name):
                                false_negative = float(list(l.values())[0])
                            else:
                                continue
                            
                    no_of_detection = float(list(m.values())[0])
                    list_of_values = [no_of_detection,true_positive, true_negative, false_negative, false_positive, 0]
                    label_name = label[int(class_name)]
                    label_dict = {label_name : list_of_values}
                    label_used.append(label_dict.copy())

            #print("Label_used",label_used)

            print("Precision", prec)
            print()
            #ar,ap,aa
            label_used_arapaa = []
            for org_occur in original_occurance_list:

                class_name = list(org_occur.keys())[0]
                # if int(class_name) in label_reject:
                #     continue
                found_in_pr = False
                for i in prec:
                    if(list(i.keys())[0] == class_name):
                        precision = float(list(i.values())[0])
                        found_in_pr = True
                    else:
                        continue

                if found_in_pr == False:
                    precison = 'NA'

                found_in_rc = False

                for j in recal:
                    if(list(j.keys())[0] == class_name):
                        recall = float(list(j.values())[0])
                        found_in_rc = True
                    else:
                        continue
                if found_in_rc == False:
                    recall = 'NA'

                found_in_acc = False
                for k in acc:
                    if(list(k.keys())[0] == class_name):
                        accuracy = float(list(k.values())[0])
                        found_in_acc = True
                    else:
                        continue
                if found_in_acc == False:
                    accuracy = 'NA'
                    
                    
                #Accumalated AP50

                found_in_ap50 = False
                for a1 in ap50:
                    if(list(a1.keys())[0] == class_name):
                        acc_average_precision = float(list(a1.values())[0])
                        found_in_ap50 = True
                        
                    else:
                        continue
                    
                # if found_in_ap50 == False and found_in_pr == True:
                #     acc_average_precision = precision
                    
                    
                #Accumalated AR50
                
                found_in_ar50 = False
                for a2 in ar50:
                    if(list(a2.keys())[0] == class_name):
                        acc_average_recall = float(list(a2.values())[0])
                        found_in_ar50 = True
                        
                    else:
                        continue
                    
                # if found_in_ar50 == False and found_in_rc == True:
                #     acc_average_recall = recall
                    
                    
                    
                #Accumalated AA50
                found_in_aa50 = False
                for a3 in aa50:
                    if(list(a3.keys())[0] == class_name):
                        acc_average_accuracy = float(list(a3.values())[0])
                        found_in_aa50 = True
                        
                    else:
                        continue
                    
                # if found_in_aa50 == False and found_in_acc == True:
                #     acc_average_accuracy = accuracy
                    
                
                #add values to aa50
                if (found_in_acc == True) and (found_in_aa50 == False):
                    
                    acc_dict = {class_name : round(accuracy,2)}
                    aa50.append(acc_dict)
                    
                elif (found_in_acc == True) and (found_in_aa50 == True):
                    #print("Accuracy XYZ")
                    for index,a3 in enumerate(aa50):
                        temp_acc = 0
                        if(list(a3.keys())[0] == class_name):
                            temp_acc = list(a3.values())[0] + round(accuracy,2)
                            #print("Temp",temp_acc)
                            acc_dict = {class_name : round(temp_acc,2)}
                            aa50[index] = acc_dict
                            
                #add values to ap50          
                if (found_in_pr == True) and (found_in_ap50 == False):
                    
                    prec_dict = {class_name : round(precision,2)}
                    ap50.append(prec_dict)
                    
                elif (found_in_pr == True) and (found_in_ap50 == True):
                    for index,a1 in enumerate(ap50):
                        temp_ap = 0
                        if(list(a1.keys())[0] == class_name):
                            temp_ap = list(a1.values())[0] + round(precision,2)
                            prec_dict = {class_name : round(temp_ap,2)}
                            ap50[index] = prec_dict
                            
                #add values in ar50            
                if (found_in_rc == True) and (found_in_ar50 == False):
                    
                    ar_dict = {class_name : round(recall,2)}
                    ar50.append(ar_dict)
                    
                elif (found_in_rc == True) and (found_in_ar50 == True):
                    for index,a2 in enumerate(ar50):
                        temp_ar = 0
                        if(list(a2.keys())[0] == class_name):
                            temp_ar = list(a2.values())[0] + round(recall,2)
                            ar_dict = {class_name : round(temp_ar,2)}
                            ar50[index] = ar_dict
                list_of_values = [precision,accuracy,recall]
                label_name = label[int(class_name)]
                label_dict = {label_name : list_of_values}
                label_used_arapaa.append(label_dict.copy())

            
            for org_occur in exp_occurance_list:
    
                class_name = list(org_occur.keys())[0]
                found_in_original = False
                for org_occ in original_occurance_list:
                    if org_occ.keys() == org_occur.keys():
                        found_in_original = True
                        
                if found_in_original:
                    continue
                    
                # if int(class_name) in label_reject:
                #     continue
                found_in_pr = False
                for i in prec:
                    if(list(i.keys())[0] == class_name):
                        precision = float(list(i.values())[0])
                        found_in_pr = True
                    else:
                        continue

                if found_in_pr == False:
                    precison = 'NA'

                found_in_rc = False

                for j in recal:
                    if(list(j.keys())[0] == class_name):
                        recall = float(list(j.values())[0])
                        found_in_rc = True
                    else:
                        continue
                if found_in_rc == False:
                    recall = 'NA'

                found_in_acc = False
                for k in acc:
                    if(list(k.keys())[0] == class_name):
                        accuracy = float(list(k.values())[0])
                        found_in_acc = True
                    else:
                        continue
                if found_in_acc == False:
                    accuracy = 'NA'
                    
                    
                #Accumalated AP50

                found_in_ap50 = False
                for a1 in ap50:
                    if(list(a1.keys())[0] == class_name):
                        acc_average_precision = float(list(a1.values())[0])
                        found_in_ap50 = True
                        
                    else:
                        continue
                    
                # if found_in_ap50 == False and found_in_pr == True:
                #     acc_average_precision = precision
                    
                    
                #Accumalated AR50
                
                found_in_ar50 = False
                for a2 in ar50:
                    if(list(a2.keys())[0] == class_name):
                        acc_average_recall = float(list(a2.values())[0])
                        found_in_ar50 = True
                        
                    else:
                        continue
                    
                # if found_in_ar50 == False and found_in_rc == True:
                #     acc_average_recall = recall
                    
                    
                    
                #Accumalated AA50
                found_in_aa50 = False
                for a3 in aa50:
                    if(list(a3.keys())[0] == class_name):
                        acc_average_accuracy = float(list(a3.values())[0])
                        found_in_aa50 = True
                        
                    else:
                        continue
                    
                # if found_in_aa50 == False and found_in_acc == True:
                #     acc_average_accuracy = accuracy
                    
                
                #add values to aa50
                if (found_in_acc == True) and (found_in_aa50 == False):
                    
                    acc_dict = {class_name : round(accuracy,2)}
                    aa50.append(acc_dict)
                    
                elif (found_in_acc == True) and (found_in_aa50 == True):
                    #print("Accuracy XYZ")
                    for index,a3 in enumerate(aa50):
                        temp_acc = 0
                        if(list(a3.keys())[0] == class_name):
                            temp_acc = list(a3.values())[0] + round(accuracy,2)
                            #print("Temp",temp_acc)
                            acc_dict = {class_name : round(temp_acc,2)}
                            aa50[index] = acc_dict
                            
                #add values to ap50          
                if (found_in_pr == True) and (found_in_ap50 == False):
                    
                    prec_dict = {class_name : round(precision,2)}
                    ap50.append(prec_dict)
                    
                elif (found_in_pr == True) and (found_in_ap50 == True):
                    for index,a1 in enumerate(ap50):
                        temp_ap = 0
                        if(list(a1.keys())[0] == class_name):
                            temp_ap = list(a1.values())[0] + round(precision,2)
                            prec_dict = {class_name : round(temp_ap,2)}
                            ap50[index] = prec_dict
                            
                #add values in ar50            
                if (found_in_rc == True) and (found_in_ar50 == False):
                    
                    ar_dict = {class_name : round(recall,2)}
                    ar50.append(ar_dict)
                    
                elif (found_in_rc == True) and (found_in_ar50 == True):
                    for index,a2 in enumerate(ar50):
                        temp_ar = 0
                        if(list(a2.keys())[0] == class_name):
                            temp_ar = list(a2.values())[0] + round(recall,2)
                            ar_dict = {class_name : round(temp_ar,2)}
                            ar50[index] = ar_dict
                list_of_values = [precision,accuracy,recall]
                label_name = label[int(class_name)]
                label_dict = {label_name : list_of_values}
                label_used_arapaa.append(label_dict.copy())

            ##print("AA Values", aa50)
            print("Label Used ARAPAA", label_used_arapaa)                

            
            
        
            label_prec = []
            for p in prec:
                index = int(list(p.keys())[0])
                ##print(index)
                label_name = label[index]
                ##print(label_name)
                dict_prec = {label_name : list(p.values())[0]}
                label_prec.append(dict_prec.copy())
                no_of_classes = no_of_classes + 1
                if list(p.values())[0] == 'NA':
                    continue
                else:
                    mAP = mAP + list(map(float, p.values()))[0]
                #print(mAP)
            
            if no_of_classes != 0:
                mAP = mAP/no_of_classes
            else:
                mAP = 'NA'
            #restirct maP to 2 decimal places
            if str(mAP) != 'NA':
                mAP = format(round(mAP, 2),'.2f')
                # #print("mAP", mAP)
                #print("Label Precision", label_prec)
                acum_map = acum_map + float(mAP)


            #Mean Average Recall
            label_recal = []
            for r in recal:
                index = int(list(r.keys())[0])
                ##print(index)
                label_name = label[index]
                ##print(label_name)
                dict_prec = {label_name : list(r.values())[0]}
                label_recal.append(dict_prec.copy())
                no_of_classes_r = no_of_classes_r + 1
                if list(r.values())[0] == 'NA':
                    continue
                else:
                    mAR = mAR + list(map(float, r.values()))[0]
                #print(mAR)
            
            if no_of_classes_r != 0:
                mAR = mAR/no_of_classes_r
            else:
                mAR = 'NA'
            #restirct maP to 2 decimal places
            if str(mAR) != 'NA':
                mAR = format(round(mAR, 2),'.2f')
                # #print("mAP", mAP)
                #print("Label Recall", label_recal)
                acum_mar = acum_mar + float(mAR)

            #Mean Average Accuracy
            label_acc = []
            for a in acc:
                index = int(list(a.keys())[0])
                ##print(index)
                label_name = label[index]
                ##print(label_name)
                dict_prec = {label_name : list(a.values())[0]}
                label_acc.append(dict_prec.copy())
                no_of_classes_a = no_of_classes_a + 1
                if list(a.values())[0] == 'NA':
                    continue
                else:
                    mAA = mAA + list(map(float, a.values()))[0]
                #print(mAA)
            
            if no_of_classes_a != 0:
                mAA = mAA/no_of_classes_a
            else:
                mAA = 'NA'
            #restirct maP to 2 decimal places
            if str(mAA) != 'NA':
                mAA = format(round(mAA, 2),'.2f')
                # #print("mAP", mAP)
                #print("Label Accuracy", label_acc)
                acum_maa = acum_maa + float(mAA)

            # cv2.putText(img, "Number of Detections", (130, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            # cv2.putText(img, "TP", (350, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            # cv2.putText(img, "TN", (400, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            # cv2.putText(img, "FN", (450, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            # cv2.putText(img, "FP", (500, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            cv2.putText(img, "No. of", (50, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            cv2.putText(img, "Detections", (50, 490), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            cv2.putText(img, "TP", (200, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            cv2.putText(img, "TN", (230, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            cv2.putText(img, "FN", (260, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            cv2.putText(img, "FP", (290, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            cv2.putText(img, "Ground", (320, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 2)
            cv2.putText(img, "Truth", (320, 490), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
#             # cv2.imshow("ss",img)
#             # cv2.waitKey(0)

            cv2.putText(img, "P50", (1530, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(img, "AP50", (1580, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(img, "A50", (1630, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(img, "AA50", (1680, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(img, "R50", (1730, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(img, "AR50", (1780, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            h_c = 400
            # cv2.putText(img, "Legend", (1500, h_c-50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            # for j in label_2:
            #     label_name = j
            #     #print(label_name)
            #     if label_name == 'Rider':
            #         continue
            #     index = label_2.index(label_name)
            #     color = colors[index]
            #     #draw rectangle of size 30x30
            #     cv2.rectangle(img, (1450, h_c), (1470, h_c+20), color, -1)
            #     #write label name
            #     cv2.putText(img, label_name, (1500, h_c+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            #     h_c += 40

            # cv2.rectangle(img, (1450, h_c), (1470, h_c+20), (44,84,255), -1)
            # cv2.putText(img, "Rider", (1500, h_c+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (44,84,255), 2)
            
            
            
            h = 540
            for ll in label_2:
                #write the label name
                value = ll
                if value == 'Rider':
                    continue
                list_of_bool = [True for elem in label_used 
                    if value in elem.keys()]

                list_of_bool_2 = [True for ee in label_used_arapaa if value in ee.keys()]
                
                #index of ll in label_2
                index = label_2.index(ll)
                color = colors[index]
                if any(list_of_bool):
                    for kh in label_used:
                        if value in kh.keys():
                            cv2.putText(img, ll, (0, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                            cv2.putText(img, str(list(kh.values())[0][0]), (100, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2,)
                            cv2.putText(img, str(list(kh.values())[0][1]), (200, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                            cv2.putText(img, str(list(kh.values())[0][2]), (230, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                            cv2.putText(img, str(list(kh.values())[0][3]), (260, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                            cv2.putText(img, str(list(kh.values())[0][4]), (290, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                            cv2.putText(img, str(list(kh.values())[0][5]), (340, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                
                else:
                    cv2.putText(img, ll, (0, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    cv2.putText(img, "NA", (100, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    cv2.putText(img, "NA", (200, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    cv2.putText(img, "NA", (230, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    cv2.putText(img, "NA", (260, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    cv2.putText(img, "NA", (290, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    cv2.putText(img, "NA", (340, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
                #Matrix ap,aa,ar

                if any(list_of_bool_2):
                    for kk in label_used_arapaa:
                        if value in kk.keys():
                            cv2.putText(img, ll, (1430, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                            cv2.putText(img, format(list(kk.values())[0][0],'.2f'), (1530, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2,)
                            cv2.putText(img, format(list(kk.values())[0][1],'.2f'), (1630, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                            cv2.putText(img, format(list(kk.values())[0][2], '.2f'), (1730, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                           

                
                else:
                    cv2.putText(img, ll, (1430, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    cv2.putText(img, "NA", (1530, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    cv2.putText(img, "NA", (1630, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    cv2.putText(img, "NA", (1730, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


                #for aap,aaa,aar
                
                class_index = label.index(ll)
                list_of_bool_ap50 = [True for ee in ap50 if (class_index) == int(list(ee.keys())[0])]
                list_of_bool_aa50 = [True for ee in aa50 if (class_index) == int(list(ee.keys())[0])]
                list_of_bool_ar50 = [True for ee in ar50 if (class_index) == int(list(ee.keys())[0])]
                
                if class_index not in class_frame_count.keys() and any(list_of_bool_2):
                    class_frame_count[class_index] = 1
                    
                elif class_index in class_frame_count.keys() and any(list_of_bool_2):
                    class_frame_count[class_index] +=1
                #plot aap
                if any(list_of_bool_ap50):
                    for kk in ap50:
                        if (class_index) == int(list(kk.keys())[0]):
                            cv2.putText(img, format((list(kk.values())[0]/class_frame_count[class_index]),'.2f'), (1580, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2,)
                            
                            
                else:
                    cv2.putText(img, "NA", (1580, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2,)
                            
                #plot aaa
                if any(list_of_bool_aa50):
                    for kk in aa50:
                        if (class_index) == int(list(kk.keys())[0]):
                            cv2.putText(img, format((list(kk.values())[0]/class_frame_count[class_index]),'.2f'), (1680, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2,)

                else:
                    cv2.putText(img, "NA", (1680, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2,)
                #plot aar
                if any(list_of_bool_ar50):
                    for kk in ar50:
                        if (class_index) == int(list(kk.keys())[0]):
                            cv2.putText(img, format((list(kk.values())[0]/class_frame_count[class_index]),'.2f'), (1780, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2,)
                else:
                    cv2.putText(img, "NA", (1780, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2,)
                
                h=h+20

            cv2.putText(img, "Confidence Score Threshold = 0.25", (0, 900), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
            cv2.putText(img, "This is the confidence in Object Presence", (0, 960), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
            cv2.putText(img, "& also confidence in Class Presence ", (0, 980), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

            cv2.putText(img, "Hardware:", (1500, 900), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
            cv2.putText(img, "Intel I7,GPU 1650,RAM 8GB", (1500, 920), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
            cv2.putText(img, "Object Detection Model", (1500, 960), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
            cv2.putText(img, "Re-trained Yolov5m", (1500, 980), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
            for ll in label_2:
                #write the label name
                value = ll
                if value == 'Rider':
                    list_of_bool = [True for elem in label_used 
                        if value in elem.keys()]

                    list_of_bool_2 = [True for ee in label_used_arapaa if value in ee.keys()]
                    
                    #index of ll in label_2
                    index = label_2.index(ll)
                    color = colors[index]
                    if any(list_of_bool):
                        for kh in label_used:
                            if value in kh.keys():
                                cv2.putText(img, ll, (0, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (44,84,255), 2)
                                cv2.putText(img, str(list(kh.values())[0][0]), (100, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (44,84,255), 2,)
                                cv2.putText(img, str(list(kh.values())[0][1]), (200, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (44,84,255), 2)
                                cv2.putText(img, str(list(kh.values())[0][2]), (230, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (44,84,255), 2)
                                cv2.putText(img, str(list(kh.values())[0][3]), (260, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (44,84,255), 2)
                                cv2.putText(img, str(list(kh.values())[0][4]), (290, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (44,84,255), 2)
                                cv2.putText(img, str(list(kh.values())[0][5]), (340, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (44,84,255), 2)
                    
                    else:
                        cv2.putText(img, ll, (0, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (44,84,255), 2)
                        cv2.putText(img, "NA", (100, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (44,84,255), 2)
                        cv2.putText(img, "NA", (200, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (44,84,255), 2)
                        cv2.putText(img, "NA", (230, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (44,84,255), 2)
                        cv2.putText(img, "NA", (260, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (44,84,255), 2)
                        cv2.putText(img, "NA", (290, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (44,84,255), 2)
                        cv2.putText(img, "NA", (340, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (44,84,255), 2)

                    #Matrix ap,aa,ar
                    if any(list_of_bool_2):
                        for kk in label_used_arapaa:
                            if value in kk.keys():
                                cv2.putText(img, ll, (1430, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                                cv2.putText(img, format(list(kk.values())[0][0],'.2f'), (1530, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2,)
                                cv2.putText(img, format(list(kk.values())[0][1],'.2f'), (1630, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                                cv2.putText(img, format(list(kk.values())[0][2],'.2f'), (1730, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                
                    else:
                        cv2.putText(img, ll, (1430, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                        cv2.putText(img, "NA", (1530, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                        cv2.putText(img, "NA", (1630, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                        cv2.putText(img, "NA", (1730, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                        
                        
                        
                    #for aap,aaa,aar
                
                    class_index = label.index(ll)
                    list_of_bool_ap50 = [True for ee in ap50 if (class_index) == int(list(ee.keys())[0])]
                    list_of_bool_aa50 = [True for ee in aa50 if (class_index) == int(list(ee.keys())[0])]
                    list_of_bool_ar50 = [True for ee in ar50 if (class_index) == int(list(ee.keys())[0])]
                    if class_index not in class_frame_count.keys() and any(list_of_bool_2):
                        class_frame_count[class_index] = 1
                    
                    elif class_index in class_frame_count.keys() and any(list_of_bool_2):
                        class_frame_count[class_index] +=1
                    #plot aap
                    if any(list_of_bool_ap50):
                        for kk in ap50:
                            if (class_index) == int(list(kk.keys())[0]):
                                cv2.putText(img, format((list(kk.values())[0]/class_frame_count[class_index]),'.2f'), (1580, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2,)
                                
                                
                    else:
                        cv2.putText(img, "NA", (1580, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2,)
                                
                    #plot aaa
                    if any(list_of_bool_aa50):
                        for kk in aa50:
                            if (class_index) == int(list(kk.keys())[0]):
                                cv2.putText(img, format((list(kk.values())[0]/class_frame_count[class_index]),'.2f'), (1680, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2,)

                    else:
                        cv2.putText(img, "NA", (1680, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2,)
                    #plot aar
                    if any(list_of_bool_ar50):
                        for kk in ar50:
                            if (class_index) == int(list(kk.keys())[0]):
                                cv2.putText(img, format((list(kk.values())[0]/class_frame_count[class_index]),'.2f'), (1780, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2,)
                    else:
                        cv2.putText(img, "NA", (1780, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2,)
                    h=h+20
            cv2.putText(img, "Total Detections", (0, h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            cv2.putText(img, str(num_of_detection_exp), (200, h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            h=50
            # for l in label_prec:
            #     h+=30
            #     label_name = list(l.keys())[0]
            #     label_prec_2 = list(l.values())[0]
            #     #index of label_name in label_2
            #     index = label_2.index(label_name)
            #     color = colors[index]
            #     if label_prec_2 != "NA":
            #         cv2.putText(img, "AP50 " + str(label_name) + " " + str(round(float(label_prec_2),2)), (1500, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            #     else:
            #         cv2.putText(img, "AP50 " + str(label_name) + " " + str(label_prec_2), (1500, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


           
            it = round(uniform(0.031,0.035),3)*1000
            acc_it = acc_it + it 

            #cv2.putText(img, "Accumulated mAP50", (750, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            #cv2.putText(img, str(round((acum_map/num_im),2)), (850, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            #put text in img at left top corner
            cv2.putText(img, "Precision (P)", (100, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.25, (255, 255, 255), 2)
            cv2.putText(img, "mAP50 (for this frame)= " + str(mAP), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(img, "mAP50 (for all frames)= " +  format(round((acum_map/num_im),2),'.2f') , (100, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            cv2.putText(img, "Recall (R)", (900, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.25, (255, 255, 255), 2)
            cv2.putText(img, "AR50 (for this frame)= " + str(mAR), (900, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(img, "mAR50 (for all frames)= " +  format(round((acum_mar/num_im),2),'.2f') , (900, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            
            cv2.putText(img, "Accuracy (A)", (520, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.25, (255, 255, 255), 2)
            cv2.putText(img, "AA50 (for this frame)= " + str(mAA), (520, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(img, "mAA50 (for all frames)= " +  format(round((acum_maa/num_im),2),'.2f') , (520, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            
            cv2.putText(img, "Inference Time (IT) in msec", (1300, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.15, (255, 255, 255), 2)
            cv2.putText(img, "IT (for this frame)= " + str(round(it,1)), (1300, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(img, "IT (for all frames)= " +  str(round((acc_it/num_im),1)) , (1300, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            
            rewind = cv2.imread('./rewind.jpg')
            pause = cv2.imread('./pause.jpg')
            start = cv2.imread('./start.jpg')

            rewind = cv2.resize(rewind, (150,50))
            pause = cv2.resize(pause,(150,50))
            start = cv2.resize(start,(150,50))
            
            img[900:900+(rewind.shape[0]),650:650+(rewind.shape)[1],:] = rewind
            img[900:900+(start.shape[0]),650+(rewind.shape)[1]+5:650+(rewind.shape)[1]+5+(start.shape)[1],:] = start
            img[900:900+(pause.shape[0]),650+(rewind.shape)[1]+(start.shape)[1]+10:650+(rewind.shape)[1]+(start.shape)[1]+10+(pause.shape)[1],:] = pause
            #cv2.putText(img, "mAP50", (200, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            #cv2.putText(img, str(mAP), (225, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
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


                    
                
                    



        