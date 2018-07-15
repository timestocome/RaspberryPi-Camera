#!/usr/bin/env python3




# http://github.com/timestocome
# adapted Google Vision Code Demo to save a photo if it detects a human, cat or dog





# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.




"""Object detection library demo.

 - Takes an input image and tries to detect person, dog, or cat.
 - Draws bounding boxes around detected objects.
 - Saves an image with bounding boxes around detected objects.
"""


import io
import sys
from PIL import Image
from PIL import ImageDraw

from aiy.vision.inference import ImageInference
from aiy.vision.models import object_detection



# take and save images
import picamera
import time
import os


    
    



def _crop_center(image):

    width, height = image.size
    size = min(width, height)
    x, y = (width - size) / 2, (height - size) / 2
    
    return image.crop((x, y, x + size, y + size)), (x, y)




def main():
    
    # run forever
    while(True):

        # Google object detection code adapted to use image from camera instead of
        # one entered at command line
        with ImageInference(object_detection.model()) as inference:

            # take a photo to check overwrite last image
            with picamera.PiCamera() as camera:
                h, w = camera.resolution
                camera.capture('test.jpg')

                
            # google code, open image check for objects
            image = Image.open('test.jpg')
        
            image_center, offset = _crop_center(image)
            draw = ImageDraw.Draw(image)
            result = inference.run(image_center)

            
            # draw boxes around any cat, dogs or humans
            count_objects = 0
            for i, obj in enumerate(object_detection.get_objects(result, 0.3, offset)):
        
                print('Object #%d: %s' % (i, str(obj)))
                x, y, width, height = obj.bounding_box
                draw.rectangle((x, y, x + width, y + height), outline='red')

                # if a cat, dog or human in image save it with a timestamp
                count_objects+= 1

                
            # save images with timestmp if cat,dog,human in image
            if count_objects > 0:

                time_string = time.strftime("%m%d-%H%M%S")
                filename = '/home/pi/security_camera/images/' + time_string + '.jpg'
                #print(filename)
                image.save(filename)
            
            # take a 15 second break between photos
            time.sleep(15)




if __name__ == '__main__':
    main()
