import glob
import os
from PIL import Image
def get_last_photo():
    '''
    Method to get the most recent file in the directory and
    add the file
    '''
    list_of_files = glob.glob('images/*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def crop_sensor(file_name):
    '''
    Method to crop the image to more closely resemble the webcam
    '''
    
    SIZE_PERCENT = 0.75
    
    image1 = Image.open(file_name)
    grid_x, grid_y =  image1.size
    
    desired_height = int(grid_y*SIZE_PERCENT)
    desired_width = int(grid_x*SIZE_PERCENT)
    
    crop_y = grid_y - desired_height
    crop_x = grid_x - desired_width
    
    
    image_cropped = image1.crop((crop_x//2,crop_y//2,grid_x - crop_x//2,grid_y - crop_y//2))
    image_cropped.save(file_name)


latest = get_last_photo()
print (latest)

crop_sensor(latest)