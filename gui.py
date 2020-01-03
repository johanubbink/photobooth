import sys
import pygame
import pygame.camera
import time

import photobooth
import printer
import create_photo

import glob
import os

def get_last_photo():
    '''
    Method to get the most recent file in the directory and
    add the file
    '''
    list_of_files = glob.glob('images/*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file


def capture_image(webcam):
    '''
    Captures a single image using and saves it to the directory
    '''
    
    imagen = webcam.get_image()
    # pygame.image.save(imagen,'temp.jpeg')
    photobooth.capture()
    # time.sleep(1)


def print_photo():
    '''
    Send the photo to the printer
    '''
    print ("Sending the photo to the printer")
    create_photo.create_printable(get_last_photo())
    printer.print_photo(get_last_photo())

#Define some important constants

COUNT_DOWN_TIME = 3
DISPLAY_IMAGE_TIME = 1
PRINT_OPTION_TIME = 5
CANCEL_TIME = 1
PRINTING_ANIM_TIME = 2

pygame.init()
pygame.camera.init()

#create fullscreen display 640x480
# screen = pygame.display.set_mode((640,480),0)

infoObject = pygame.display.Info()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

#find, open and start low-res camera
cam_list = pygame.camera.list_cameras()
webcam = pygame.camera.Camera(cam_list[0],(960,540))
webcam.start()

welcome_font = pygame.font.SysFont(None, 100)

font = pygame.font.SysFont(None, 600)
text = font.render("0", True, (128, 0, 0))

#create the one second timer
prev_time = time.time()
time_elapsed = 0
count_down = COUNT_DOWN_TIME

current_state = 0
next_state = 0

while True:
    ###############
    #STATE ACTIONS#
    ###############

    ##################
    #1 :Initial State#
    ##################
    #this state waits for a button press

    if current_state == 0:
        #grab image, scale and blit to screen
        imagen = webcam.get_image()
        imagen = pygame.transform.scale(imagen,(1920,1080))
        screen.blit(imagen,(0,0))

        #do the display
        # text = welcome_font.render("Johan en Marli se Troue", True, (0, 0, 0))
        # screen.blit(text,
        #         (960 - text.get_width() // 2, 540 - text.get_height() // 2))
        text = welcome_font.render("Druk space om te begin", True, (0, 0, 0))
        screen.blit(text,
                (960 - text.get_width() // 2, 540 - text.get_height() // 2))


        next_state = current_state

    #######################
    #Countdown timer state#
    #######################
    #this state create a count down timer to capture image

    elif current_state == 1:
        imagen = webcam.get_image()
        imagen = pygame.transform.scale(imagen,(1920,1080))
        screen.blit(imagen,(0,0))


        if count_down == 0:
            text = font.render("Smile!", True, (128, 0, 0))
            screen.blit(text,
                    (960 - text.get_width() // 2, 540 - text.get_height() // 2))
        else:
            #display the time
            text = font.render(str(count_down), True, (128, 0, 0))
            screen.blit(text,
                        (960 - text.get_width() // 2, 540 - text.get_height() // 2))


    ###############
    #Capture State#
    ###############
    #this state captures the image

    elif current_state == 2:
        capture_image(webcam)

        next_state = 3

    #####################
    #Display image state#
    #####################

    elif current_state == 3:
        latest_file = get_last_photo()
        imagen = pygame.image.load(latest_file)
        imagen = pygame.transform.scale(imagen,(1920,1080))
        screen.blit(imagen,(0,0))

    ################################
    #ask if you want to print state#
    ################################

    elif current_state == 4:
        # imagen = pygame.image.load('temp.jpeg')
        # imagen = pygame.transform.scale(imagen,(1920,1080))
        screen.blit(imagen,(0,0))

        text = welcome_font.render("Druk knoppie om foto te druk", True, (0, 0, 0))
        screen.blit(text,
                (960 - text.get_width() // 2, 400 - text.get_height() // 2))

        text = font.render(str(count_down), True, (128, 0, 0))
        screen.blit(text,
                    (960 - text.get_width() // 2, 800 - text.get_height() // 2))
    

    elif current_state == 5:
        imagen = webcam.get_image()
        imagen = pygame.transform.scale(imagen,(1920,1080))
        screen.blit(imagen,(0,0))

        text = welcome_font.render("Foto gekanseleer...", True, (0, 0, 0))
        screen.blit(text,
                (960 - text.get_width() // 2, 540 - text.get_height() // 2))

    ########################
    #Handle external events#
    ########################

    #handle the timing events

    if time.time() - prev_time > 1:
        prev_time = time.time()

        if current_state ==1:
            count_down += -1
            if count_down < 0:
                next_state = 2

        if current_state == 3:
            count_down += -1
            if count_down < 0:
                next_state = 4

        if current_state == 4:
            count_down += -1
            if count_down < 0:
                next_state = 5

        if current_state == 5:
            count_down += -1
            if count_down < 0:
                next_state = 0

        if current_state == 6:
            count_down += -1
            if count_down < 0:
                next_state = 0
                



    # Handle button events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if current_state == 0:
                    prev_time = time.time()
                    next_state = 1

                if current_state == 4:
                    next_state = 6

                if current_state == 5:
                    next_state = 6

            else:
                webcam.stop()
                pygame.quit()
                sys.exit()

        if event.type == pygame.QUIT:
            webcam.stop()
            pygame.quit()
            sys.exit()


    if current_state == 0 and next_state == 1:
        count_down = COUNT_DOWN_TIME
    
    if current_state == 1 and next_state == 2:
        imagen = webcam.get_image()
        imagen = pygame.transform.scale(imagen,(1920,1080))
        screen.blit(imagen,(0,0))

        text = welcome_font.render("Capturing...", True, (0, 0, 0))
        screen.blit(text,
        (960 - text.get_width() // 2, 540 - text.get_height() // 2))

    if current_state == 2 and next_state == 3:
        count_down = DISPLAY_IMAGE_TIME


    if current_state == 3 and next_state == 4:
        count_down = PRINT_OPTION_TIME

    if current_state == 4 and next_state == 5:    
        count_down = CANCEL_TIME

    if current_state == 5 and next_state == 0:
        count_down = CANCEL_TIME

    if ((current_state == 4 or current_state ==5) and next_state == 6):
        count_down = PRINTING_ANIM_TIME
        screen.blit(imagen,(0,0))

        text = welcome_font.render("Sending photo to printer...", True, (0, 0, 0))
        screen.blit(text,
        (960 - text.get_width() // 2, 540 - text.get_height() // 2))

        #call the printing photo
        print_photo()
        


    #draw all updates to display
    # pygame.display.update()
    pygame.display.flip()


    clock.tick(100)
    current_state = next_state    