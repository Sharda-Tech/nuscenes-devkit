import os
import tqdm
path = './Final Dataset/train/'
number = 0
image_number = 0
print(path)
for file in tqdm.tqdm(os.listdir(path)):
    if '.txt' in file:
        #find file size
        file_size = os.path.getsize(os.path.join(path, file))
        if file_size == 0:
            number+=1


    else:
        image_number+=1


print(number)
print(image_number)