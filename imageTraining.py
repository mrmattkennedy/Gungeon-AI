import numpy as np
from PIL import ImageGrab
import cv2
import urllib.request
from time import sleep
import os
import shutil

def grab_negatives_from_game():
    sleep(3)
    for i in range(100, 2000):
        ss = np.array(ImageGrab.grab())
        ss = cv2.cvtColor(ss, cv2.COLOR_BGR2GRAY)
        resized_ss = cv2.resize(ss, (100, 100))
        cv2.imwrite("negative_images_grayscale/" + str(i) + ".jpg", resized_ss)
        sleep(0.1)

def store_raw_images():
    neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00523513'   
    neg_image_urls = urllib.request.urlopen(neg_images_link).read().decode()
    pic_num = 1
    
    if not os.path.exists('negative_from_web'):
        os.makedirs('negative_from_web')
        
    for i in neg_image_urls.split('\n'):
        try:
            print(i)
            urllib.request.urlretrieve(i, "negative_from_web/"+str(pic_num)+".jpg")
            img = cv2.imread("negative_from_web/"+str(pic_num)+".jpg",cv2.IMREAD_GRAYSCALE)
            # should be larger than samples / pos pic (so we can place our image on it)
            resized_image = cv2.resize(img, (100, 100))
            cv2.imwrite("negative_from_web/"+str(pic_num)+".jpg",resized_image)
            pic_num += 1
            
        except Exception as e:
            print(str(e))

def find_uglies():
    match = False
    for file_type in ['negative_from_web']:
        for img in os.listdir(file_type):
            for ugly in os.listdir('uglies'):
                try:
                    current_image_path = str(file_type)+'/'+str(img)
                    ugly = cv2.imread('uglies/'+str(ugly))
                    question = cv2.imread(current_image_path)
                    if ugly.shape == question.shape and not(np.bitwise_xor(ugly,question).any()):
                        print('That is one ugly pic! Deleting!')
                        print(current_image_path)
                        os.remove(current_image_path)
                except Exception as e:
                    print(str(e))

def compile_negatives():
    current_image = 0
    destination = "temp2"
    for folder in ['negative_images']:
        for img in os.listdir(folder):
            new_name = 'temp/'+str(current_image)+".jpg"
            os.rename(folder+'/'+img, new_name)
            shutil.move(new_name, destination)
            current_image = current_image+1
            
                    

def reshape_positive():
    pos = cv2.imread("positive_images/1.png")
    resized_image = cv2.resize(pos, (50, 50))
    cv2.imwrite("positive_images/positive_1.jpg", resized_image)
    
def create_pos_n_neg():
    for file_type in ['negative_images', 'positive_images']:

        for img in os.listdir(file_type):
            if file_type == 'negative_images':
                line = 'neg/'+img+'\n'
                with open('bg.txt', 'a') as f:
                    f.write(line)

            elif file_type == 'positive_images':
                line = file_type+'/'+img+' 1 0 0 50 50\n'
                with open('info.dat', 'a') as f:
                    f.write(line)

#reshape_positive()
#grab_negatives()
create_pos_n_neg()
#store_raw_images()
#find_uglies()
#compile_negatives()
