import os
import matplotlib.pyplot as plt
from tqdm import tqdm

class_name = []
class_number = []
for file in tqdm(os.listdir('./output_val')):
    if file.endswith('.txt'):
        #read lines
        text_file_path = os.path.join('./output_val', file)
        with open(text_file_path, 'r') as f:
            lines = f.readlines()
            #iterate through each line
            for line in lines:
                #split line
                line_split = line.split(' ')
                #get the first word
                word = line_split[0]
                if(word not in class_name):
                    class_name.append(word)
                    class_number.append(1)
                else:
                    class_number[class_name.index(word)] += 1


#save class_name and class_number to a file
with open('class_name_nuimages_val.txt', 'w') as f:
    for i in range(len(class_name)):
        f.write(class_name[i] + ' ' + str(class_number[i]) + '\n')

     

plt.bar(class_name, class_number)
plt.xlabel('Class')
plt.ylabel('Number of images')
plt.title('Number of images per class')
plt.show()
#save the data
plt.savefig('class_number.png')






