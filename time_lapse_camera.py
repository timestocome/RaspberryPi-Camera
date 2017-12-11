
# https://github.com/timestocome


# collect image stills and stitch them into a video
#
# code below collects images
#
# command line tools to stitch images into a video
#
# install tools
# pi@raspberrypi:~ $ sudo apt-get -y install libav-tools
#
# more information:
# https://www.raspberrypi-spy.co.uk/2013/05/creating-timelapse-videos-with-the-raspberry-pi-camera/ 
#
# command to create video from stills
# $ avconv -r 10 -i image_%04d.jpg -r 10 -vcodec libx264 -crf 20 -g 15 timelapse.mp4
#
# play video
# $ omxplayer timelapse.mp4




# take photos at regular time intervals and adjust for light levels
# http://www.reddit.com/r/raspberry_pi/comments/7e51wc/raspberry_pi_daynight_timelapses_with_v2_noir


from picamera import PiCamera
import time
from PIL import Image
import numpy as np
import datetime



width = 1640
height = 1232


min_brightness = 5
max_brightness = 250

target_brightness = 120

min_exposure = 150
max_exposure = 9000000


# 24 hours ~ 24 * 60  1 per minute
# 24 hours * 15 frames/hour 
n_images = 24 * 15

# seconds between images
# seconds per hour ( 60 * 60 ) / images per hour
sleep_time = (60 * 60) // 15


# picamera.readthedocs.io/en/latest/fov.html#theory-of-operation
# framerate = 1second/min exposure time in seconds
# framerate 1/30 ~ 33 fps ->  33 ms shutter speed

# set exposure time
# https://reddit.com/r/raspberry_pi/comments/7e51wc/raspberry_pi/daynight_timelapses_with_v2_noir



with PiCamera() as camera:

    camera.resolution = (width, height)
    camera.framerate = 1 / 9

    for i in range(n_images):

        # increment file name
        filename = 'image_%06d.jpg' % i

        # caputure image
        camera.capture(filename)

        # check brightness of last image
        im = Image.open(filename)
        brightness = np.mean(im)

        # clamp brightness
        brightness = max(min_brightness, min(brightness, max_brightness))
        print('brightness', brightness)
        exposure = camera.exposure_speed
        print('exposure', exposure)

        # calculate new exposure time
        total_light = float(brightness)/float(camera.exposure_speed)
        new_exposure_target = target_brightness // total_light

        # clamp exposure time
        new_exposure_target = max(min_exposure, min(new_exposure_target, max_exposure))

        
        print('new exposure', new_exposure_target)

        # test if something has gone awry
        if abs(exposure - new_exposure_target) > 100000:
            new_exposure_target = exposure
            print('problem with exposure')


        
        # time between images
        time.sleep(sleep_time)
        print('time', datetime.datetime.now())
        
        # set new shutter speed
        camera.shutter_speed = int(new_exposure_target)
    

