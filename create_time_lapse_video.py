
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
# where I learned
# https://www.raspberrypi-spy.co.uk/2013/05/creating-timelapse-videos-with-the-raspberry-pi-camera/ 
#
# command to create video from stills
# $ avconv -r 10 -i image_%04d.jpg -r 10 -vcodec libx264 -crf 20 -g 15 timelapse.mp4
#
# play video
# $ omxplayer timelapse.mp4



# kept this as simple as possible
# a lot cooler things can be done to adjust for night images or adding filters


from picamera import PiCamera
import time
import numpy as np




# init camera
camera = PiCamera()
camera.vflip = True
camera.resolution = (1024, 768)
time.sleep(0.5)



# max images to collect - just a few to test things
n_images = 80

for i in range(n_images):

    print('loop', i)
    
    # test light  ( 0-100 )
    print('light reading ', camera.brightness)
    time.sleep(1)

    # file name with timestamp
    #ts = str(camera.timestamp)
    #filename = 'image_' + ts + '.jpg'

    # or just increment file name each loop
    filename = 'image_%04d.jpg' % i

    # save image
    camera.capture(filename)
   
    # number of seconds between images
    time.sleep(3)
        



    
