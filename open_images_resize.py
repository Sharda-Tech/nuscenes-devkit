import os
import cv2
from tqdm import tqdm

for file in tqdm(os.listdir("./open-images-v6/test/data")):
    if file.endswith(".jpg"):
        image = cv2.imread("./open-images-v6/test/data/" + file)
        image = cv2.resize(image, (640, 480))
        cv2.imwrite("./open_image_resized/test/" + file, image)