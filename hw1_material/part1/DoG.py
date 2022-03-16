from itertools import count
from mimetypes import init
from xml.dom.domreg import well_known_implementations
from xmlrpc.client import boolean
from cv2 import threshold
import numpy as np
import cv2 as cv


class Difference_of_Gaussian(object):
    def __init__(self, threshold):
        self.threshold = threshold
        self.sigma = 2**(1/4)
        self.num_octaves = 2
        self.num_DoG_images_per_octave = 4
        self.num_guassian_images_per_octave = self.num_DoG_images_per_octave + 1
    
    def get3d(up,mid,lower,row,col):
        newup = up[row-1:row+1,col-1:col+1]
        newmid = mid[row-1:row+1,col-1:col+1]
        newlower = lower[row-1:row+1,col-1:col+1]
        my3d = np.array([newup,newmid,newlower])
        return my3d
        
    def extremeoccur(Doglist,index):
        map = Doglist[index]
        upper = Doglist[index + 1]
        lower = Doglist[index - 1]
        rows,cols  = np.shape(map)
        recordextr = []
        for row in (1,rows-2):
            for col in (1,cols-2):
                if(map[row,col] >threshold):
                    threeD = Difference_of_Gaussian.get3d(upper,map,lower,row,col)
                    if ((np.max(threeD) == map[row,col]) | (np.min(threeD) == map[row,col])):
                        extrbuf = [row,col]
                        recordextr.append(extrbuf)
        recordarray = np.array(recordextr)
        return recordarray

    def get_keypoints(self, image):
        ### TODO ####
        # Step 1: Filter images with different sigma values (5 images per octave, 2 octave in total)
        # - Function: cv2.GaussianBlur (kernel = (0, 0), sigma = self.sigma**___)
        count = 0
       
        gaussian_images = []
    
      
        while count<self.num_guassian_images_per_octave:
            if count==0:
                gaussian_images.append(image)
                count = count +1
            else:
                gimage = cv.GaussianBlur(gaussian_images[count-1],ksize=(0,0),sigmaX=self.sigma**(count),sigmaY= 0)
                gaussian_images.append(gimage)
                count = count +1
        count = 0
        while count<self.num_guassian_images_per_octave:
            if count == 0:
                a = gaussian_images[-1]
                gimage = cv.resize(gaussian_images[-1],fx=0.5,fy=0.5, interpolation=cv.INTER_NEAREST)
                gaussian_images.append(gimage)
                count = count + 1
            else:
                gimage = cv.GaussianBlur(gaussian_images[count + self.num_DoG_images_per_octave],ksize=(0,0),sigmaX=self.sigma**(count),sigmaY= 0)
                gaussian_images.append(gimage)
                count = count + 1



        # Step 2: Subtract 2 neighbor images to get DoG images (4 images per octave, 2 octave in total)
        # - Function: cv2.subtract(second_image, first_image)
        
        dog_images = []
        for i in range(0, self.num_DoG_images_per_octave):
            dog_images.append(cv.subtract(gaussian_images[i+1]-gaussian_images[i]))
        for i in range(self.num_guassian_images_per_octave,self.num_guassian_images_per_octave+self.num_DoG_images_per_octave):
             dog_images.append(cv.subtract(gaussian_images[i+1]-gaussian_images[i]))
            

        # Step 3: Thresholding the value and Find local extremum (local maximun and local minimum)
        #         Keep local extremum as a keypoint
        first_octaveextr = []
        second_octaveextr = []
        for i in range(1,self.num_DoG_images_per_octave-1):
            extrbuffer = self.extremeoccur(dog_images,i)
            first_octaveextr.append(extrbuffer)
        for i in range(self.num_DoG_images_per_octave+1,self.num_DoG_images_per_octave*2 - 1):
            extrbuffer = self.extremeoccur(dog_images,i)*2
            second_octaveextr.append(extrbuffer)
        final_extr = first_octaveextr + second_octaveextr


        # Step 4: Delete duplicate keypoints
        # - Function: np.unique
        length =0
        for i in final_extr:
            length = length + i.shape[0] #for resize to an lenght*2 array
        initkey = np.array(final_extr)
        initkey.resize(length,2)
        keypoints = np.unique(initkey,axis=0)
        




        # sort 2d-point by y, then by x
        keypoints = keypoints[np.lexsort((keypoints[:,1],keypoints[:,0]))] 
        return keypoints
