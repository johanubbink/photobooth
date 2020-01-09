from PIL import Image

def create_printable(filename,foldername):
    image1 = Image.open(filename)
    MARGIN = 15

    #join the photos and create printable

    #open up the template image
    background = Image.open(foldername + "/template.png")
    grid_x, grid_y =  background.size

    #resize the captured image to fit
    image_height = grid_x//4*3
    image_smaller = image1.resize((grid_x,image_height))

    #crop the dimensions of the photo
    #calculate how much the photo should be cropped
    desired_height = grid_y//2 - MARGIN*2
    crop = image_height - desired_height
    image_cropped = image_smaller.crop((0,crop//2,grid_y,image_height - crop//2))

    background.paste(image_cropped, (0, MARGIN))
    background.paste(image_cropped, (0, grid_y//2 + MARGIN))

    # logo = Image.open('logo.png')
    # background.paste(logo, (MARGIN, MARGIN*2))
    background.save('out.png')