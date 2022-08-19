import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
import random
import pickle

# hardcoded based on template image
CENTER_COORDS = 600, 550


def read_img(file_path):
    im = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    return im


def print_img(img):
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(rgb)


def find_contours(im):
    contours, _ = cv2.findContours(im.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    cv2.drawContours(im, contours, -1, (0, 255, 0), 3)

    return contours


def shift_center(contours, center_coords=CENTER_COORDS):
    """
    align the image with the template
    """
    M = cv2.moments(contours[0])
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    
    delta_X = center_coords[0] - cX
    delta_Y = center_coords[1] - cY

    # contours are returned as tuple (numpy_array, )
    coords_array = contours[0]

    coords_array[:, :, 0] = coords_array[:, :, 0] + delta_Y
    coords_array[:, :, 1] = coords_array[:, :, 1] + delta_X

    return contours
    

def plot_on_template(im, fill=True, fill_color = (142, 100, 46), template_path='./resources/template.jpg'):
    tpl = cv2.imread(template_path)
    
    contours = find_contours(im)
    contours = shift_center(contours)
    cv2.drawContours(tpl, contours, -1, fill_color, thickness=2, lineType=cv2.LINE_AA)
    
    if fill:
        cv2.fillPoly(tpl, pts=contours, color=fill_color)
    
    return tpl


if __name__ == '__main__':

    img_files = glob.glob('./resources/img_pokemon_png/*.png')
    img_files = random.sample(img_files, 2)
    output_dir = './resources/img_with_template'

    for img_file in img_files:
        tail = img_file.split('/')[-1]

        try:
            print('reading:', img_files)
            im = read_img(img_file)
            result = plot_on_template(im)

            tail_jpg = tail[:-3] + 'jpg'
            cv2.imwrite(f'{output_dir}/{tail_jpg}', result)
        
        except Exception as e:
            print(e)
            print(tail)