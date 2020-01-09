import sys
import pygame
import pygame.camera
import time

import photobooth
import printer
import create_photo


import gphoto2 as gp
import RPi.GPIO as GPIO

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
    time.sleep(1)


def print_photo():
    '''
    Send the photo to the printer
    '''
    print ("Sending the photo to the printer")
    create_photo.create_printable(get_last_photo())
    printer.print_photo(get_last_photo())

print (os.path.realpath(__file__))

#Define the button press setup
BUTTON_PIN = 18
DEBOUNCE_TIME = 4

debounce_counter = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Define some important constantsen,preview_size)
COUNT_DOWN_TIME = 3
DISPLAY_IMAGE_TIME = 1
PRINT_OPTION_TIME = 10
CANCEL_TIME = 1
PRINTING_ANIM_TIME = 2

button_flag = False

pygame.init()
pygame.camera.init()

#create fullscreen display 640x480
# screen = pygame.display.set_mode((640,480),0)
pygame.mouse.set_visible(False) #hide the mouse cursor
infoObject = pygame.display.Info()

#screen = pygame.display.set_mode((infoObject.current_w,infoObject.current_h), pygame.FULLSCREEN)
screen = pygame.display.set_mode((infoObject.current_w,infoObject.current_h), pygame.FULLSCREEN)
clock = pygame.time.Clock()
x_size, y_size = screen.get_size()
MIDDEL_X = x_size/2
MIDDEL_Y = y_size/2

preview_size= (x_size, x_size//16*9)
preview_y = (y_size - x_size//16*9)//2


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
        screen.fill([0,0,0])
        imagen = webcam.get_image()
        imagen = pygame.transform.scale(imagen,preview_size)
        imagen = pygame.transform.flip(imagen,True,False)
        screen.blit(imagen,(0,preview_y))

        #do the display
        # text = welcome_font.render("Johan en Marli se Troue", True, (0, 0, 0))
        # screen.blit(text,
        #         (960 - text.get_width() // 2, 540 - text.get_height() // 2))
        text = welcome_font.render("Press button to start!", True, (128, 0, 0))
        screen.blit(text,
                (MIDDEL_X - text.get_width() // 2, MIDDEL_Y - text.get_height() // 2))


        next_state = current_state

    #######################
    #Countdown timer state#
    #######################
    #this state create a count down timer to capture image

    elif current_state == 1:
        imagen = webcam.get_image()
        imagen = pygame.transform.scale(imagen,preview_size)
        imagen = pygame.transform.flip(imagen,True,False)
        screen.blit(imagen,(0,preview_y))


        if count_down == 0:
            text = font.render("Smile!", True, (128, 0, 0))
            screen.blit(text,
                    (MIDDEL_X - text.get_width() // 2, MIDDEL_Y - text.get_height() // 2))
        else:
            #display the time
            text = font.render(str(count_down), True, (128, 0, 0))
            screen.blit(text,
                        (MIDDEL_X - text.get_width() // 2, MIDDEL_Y - text.get_height() // 2))


    ###############
    #Capture State#
    ###############
    #this state captures the image

    elif current_state == 2:
        file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
        screen.fill([255,255,255])
        text = welcome_font.render("processing...", True, (0, 0, 0))
        screen.blit(text,
        (MIDDEL_X - text.get_width() // 2, MIDDEL_Y - text.get_height() // 2))


        next_state = 2_5

    elif current_state == 2_5:
        
        
        target = "images/" + file_path.name
        camera_file = camera.file_get(
            file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
        print (target)
        camera_file.save(target)
        # subprocess.call(['xdg-open', target])
        camera.exit()
        next_state = 3

    #####################
    #Display image state#
    #####################

    elif current_state == 3:
        latest_file = get_last_photo()
        imagen = pygame.image.load(latest_file)
        imagen = pygame.transform.scale(imagen,(y_size//3 *4,y_size))
        screen.fill([0,0,0])
        pos =  (x_size - y_size//3 *4)/2
        screen.blit(imagen,(pos,0))

    ################################
    #ask if you want to print state#
    ################################

    elif current_state == 4:
        # imagen = pygame.image.load('temp.jpeg')
        # imagen = pygame.transform.scale(imagen,(1920,1080))
        pos =  (x_size - y_size//3 *4)/2
        screen.blit(imagen,(pos,0))

        text = welcome_font.render("Press button to print photo!", True, (128, 0, 0))
        screen.blit(text,
                (MIDDEL_X - text.get_width() // 2, MIDDEL_Y - 200 - text.get_height() // 2))

        text = font.render(str(count_down), True, (128, 0, 0))
        screen.blit(text,
                    (MIDDEL_X - text.get_width() // 2, MIDDEL_Y + 200 - text.get_height() // 2))
    

    elif current_state == 5:
        screen.fill([0,0,0])
        imagen = webcam.get_image()
        imagen = pygame.transform.scale(imagen,preview_size)
        imagen = pygame.transform.flip(imagen,True,False)
        screen.blit(imagen,(0,preview_y))

        text = welcome_font.render("Printing cancelled...", True, (128, 0, 0))
        screen.blit(text,
                (MIDDEL_X - text.get_width() // 2, MIDDEL_Y - text.get_height() // 2))

    elif current_state == 6:
        #call the printing photo
        print_photo()
    ########################
    #Handle external events#
    ########################

    #handle the timing events

    if time.time() - prev_time > 1:
        prev_time = time.time()

        if current_state ==1:
            count_down += -1
            if count_down < 1:
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
        
        #handle the button press
        if button_flag:
            button_flag = False
            
            if current_state == 0:
                prev_time = time.time()
                next_state = 1
            if current_state == 4:
                next_state = 6
            if current_state == 5:
                next_state = 6            
            
            
            
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
        # imagen = webcam.get_image()
        # imagen = pygame.transform.scale(imagen,(1920,1080))
        # screen.blit(imagen,(0,0))
        white = [255, 255, 255]
        screen.fill(white)
        #create the camera object
        
        
        camera = gp.Camera()
        camera.init()
        text = font.render("Smile!", True, (0, 0, 0))
        screen.blit(text,
        (MIDDEL_X - text.get_width() // 2, MIDDEL_Y - text.get_height() // 2))

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
        pos =  (x_size - y_size//3 *4)/2
        screen.blit(imagen,(pos,0))

        text = welcome_font.render("Sending photo to printer...", True, (128, 0, 0))
        screen.blit(text,
        (MIDDEL_X - text.get_width() // 2, MIDDEL_Y - text.get_height() // 2))

        
        


    #draw all updates to display
    # pygame.display.update()
    pygame.display.flip()

    
    
    
    #do the button debouncing
    for k in range(5):
        the_time = time.time()
        while time.time() - the_time > 0.1:
            #do nothin
            x = 1
            
        input_state = GPIO.input(18)
        if input_state == False:
            debounce_counter += 1
        else:
            debounce_counter = 0
            
        if debounce_counter > DEBOUNCE_TIME:
            button_flag = True
        
    clock.tick(50)
    current_state = next_state
        
        