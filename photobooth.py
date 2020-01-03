import gphoto2 as gp
import time
import subprocess
def capture():
    '''
    Method to take a picture using gphoto
    '''
    #capture the image
    try:
        #create the camera object
        camera = gp.Camera()
        camera.init()

        #try to capture the image
        print('Capturing image')
        file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
        print("Saving the image")
        #copy the image from the SD card
        target = "images/" + file_path.name
        camera_file = camera.file_get(
            file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
        camera_file.save(target)
        # subprocess.call(['xdg-open', target])
        camera.exit()

    except:
        print ("Unable to capture")
    #exit the camera object
    
def photo_with_timer(num_photos = 3, count_down = 5):
    print ("\n")
    print ("==========================")
    print ("Welcome to our photobooth!")
    print ("==========================")
    #loop for the number of photos
    for k in range(num_photos):
        print ("\n")
        print ("============")
        print ("Photo", k+1, "of", num_photos)
        print ("============\n")
        # print ("Starting", count_down, "sec timer")

        #start the count_down timer
        for i in range(count_down,0,-1):
            print (i, "seconds!")
            time.sleep(1)
            

        print ("Smile!!!")
        capture()
        


if __name__ == "__main__":
    photo_with_timer()