from PIL import Image
from tqdm import tqdm
from PIL import ImageFile
import os
ImageFile.LOAD_TRUNCATED_IMAGES = True
#resize the image to a smaller size
for file in tqdm(os.listdir('./output')):

    if file.endswith('.png'):
        img = Image.open('./output/' + file)
        img = img.resize((640, 480))
        img.save('./output/' + file)


    