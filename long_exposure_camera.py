
# https://github.com/timestocome

# take long exposure photos
#
# more information:
# https://www.raspberrypi.org/forums/viewtopic.php?f=43&t=188752


import os
import time
import numpy as np
from PIL import Image



width = 1640
height = 1232

# time between images --- mins between images * seconds per minute = seconds between photos
images_per_hour = 12

# minutes between images (60/images/hour)  * (seconds per min) 
sleep_time = (60 / images_per_hour) * 60

# number of images in 24 hours --- (24 hours * 60 mins/hour * 60 secs/min)/sleep_time in seconds
n_images = int(24 * 60 * 60 / sleep_time) * 2 




# documentation for RaspiCam
# https://www.modmypi.com/blog/raspberry-pi-camera-board-raspistill-command-list

# raspistill
# -vf -hf flip camera
# -o output_file.png
# -n no preview
# -tl timelapse
# -awb off   turn off automatic white balance
# -t sleep_time  time between images
# -sa sharpness -100 100
# -ISO
# -ex off, auto, night, fixedfps
# -ss ? exposure time idk





min_ss = 100
max_ss = 1000000 - 1


ss = 33500 # starting value for first loop average lighting
#ss = max_ss   # late night photos

for i in range(n_images):

    # check brightness of last image
    if i > 0:
        im = np.array(Image.open(file_name))
        r = np.median(im[:,:,0])
        g = np.median(im[:,:,1])
        b = np.median(im[:,:,2])
        avg = (r + b + g) // 3

        # scaled percent to adjust current shutter setting
        ds = (100. - avg) / 500.  
        ss += (ss * ds)
        
        print('trying shutter speed... %d' % (ss))
        if ss < min_ss: ss = 100
        if ss > max_ss: ss = max_ss

        # on NoIR camera green is the best indicator of brightness
        print(' %s g %d r %d, b %d, last shutter speed %f, ds %f' % (file_name, g, r, b, ss, ds))

    
    file_name = "image_%05d.jpg" % i

    # Turning off awb turns images to black and green only
    #command = 'raspistill -n -o %s -awb off -ss %d' % (file_name, ss)
    command = 'raspistill -n -o %s -ss %d' % (file_name, ss)
    
    
    os.system(command)
    time.sleep(sleep_time)

