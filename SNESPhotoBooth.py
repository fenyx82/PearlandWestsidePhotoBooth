from evdev import InputDevice, categorize, ecodes, KeyEvent
import picamera
from time import sleep
import pygame
from pygame.locals import *
import os
from twython import Twython
import time
import sys

RED = ( 255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
#sets up the usb controller
gamepad=InputDevice('/dev/input/event0')
camera = picamera.PiCamera()
camera.resolution = (640, 480)
#camera.brightness = 70
#initializes pygame and pygame font
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
myfontsmall = pygame.font.Font("/usr/share/fonts/truetype/LiberationSans-Regular.ttf", 30)
myfont = pygame.font.Font("/usr/share/fonts/truetype/LiberationSans-Regular.ttf", 144)
infoObject = pygame.display.Info()
#twitter app info
apiKey = ''
apiSecret = ''
accessToken = ''
accessTokenSecret = ''
api = Twython(apiKey, apiSecret, accessToken, accessTokenSecret)
#sets image name.  only one image is saved and it is overwritten every time a picture is taken.
IMG_NAME = "testImage.jpg"

#method to take picture
def takePicture():
        for event in gamepad.read_loop():
                if event.type == ecodes.EV_KEY:
                        keyevent = categorize(event)
                        if keyevent.keystate == KeyEvent.key_down:
                                if keyevent.keycode == 'BTN_TR2':
                                        camera.start_preview(alpha=100)
                                        count = 5
                                        while (count > -1):
                                                screen.fill(BLACK)
                                                titlelabel = myfont.render(str(count), 1, RED)
                                                screen.blit(titlelabel, (530, 240))
                                                pygame.display.update()
                                                sleep(1)
                                                count = count - 1
                                        camera.capture('testImage.jpg')
                                        camera.stop_preview()
                                        screen.fill(BLACK)
                                        imagetw = pygame.image.load(IMG_NAME)
                                        screen.blit(imagetw, (0,0))
                                        tmessage=myfontsmall.render("Press A to upload image to Twitter or X to take picture again.", 1, WHITE)
                                        screen.blit(tmessage, (240, 530))
                                        pygame.display.update()
                                        postTwitter()
                                        return 
                                #escape button to exit program
                                elif keyevent.keycode[1] == 'BTN_Y':
                                        camera.close()
                                        pygame.font.quit()
                                        pygame.quit()
                                        
                                
#method to post to twitter
def postTwitter():
        for event in gamepad.read_loop():
                if event.type == ecodes.EV_KEY:
                        keyevent = categorize(event)
                        if keyevent.keystate == KeyEvent.key_down:
                                if keyevent.keycode[0] == 'BTN_B':
                                        photo = open(IMG_NAME, 'rb')
                                        media_status = api.upload_media(media=photo)
                                        #change message to reflect event photobooth is being used at
                                        tweet_txt = "BCLS at the Houston Maker Faire Day 2!  @MakerFaireHOU"
                                        api.update_status(media_ids=[media_status['media_id']], status=tweet_txt)
                                        return
                                if keyevent.keycode[0] == 'BTN_A':
                                        return

while True:
        screen.fill(BLACK)
        startmessage = myfontsmall.render("Press Start to begin Countdown", 1, WHITE)
        screen.blit(startmessage, (400, 320))
        pygame.display.update()
        takePicture()

                                                     
camera.close()
pygame.font.quit()
pygame.quit()
