import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob

# Read in the image, 0 = grayscale
# im = cv2.imread(img_file, 1)
# plt.imshow(im)


# cv2 uses BGR colors
# we can convert to RGB using im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)


# read and convert inmage from BGR to RGB
# fig, axes = plt.subplots(1, 3)
# for flag, ax in zip([cv2.IMREAD_COLOR, cv2.IMREAD_GRAYSCALE, cv2.IMREAD_UNCHANGED], axes):
#     im = cv2.imread(img_file, flag)
#     im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
#     ax.imshow(im)
#     ax.set_title(flag)

# plt.imshow(im)

# hardcoded based on template image
CENTER_COORDS = 600, 550


def find_contours(file_path):
    # Run findContours - Note the RETR_EXTERNAL flag
    # Also, we want to find the best contour possible with CHAIN_APPROX_NONE
    im = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    contours, hierarchy = cv2.findContours(im.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    cv2.drawContours(im, contours, -1, (0, 255, 0), 3)

    # blank = np.zeros_like(im)
    # cv2.drawContours(blank, contours, -1, (0, 255, 0), 3)

    # plt.imshow(blank)

    return contours


def shift_center(contours, center_coords=CENTER_COORDS):
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
    

def plot_on_template(file_path, fill=True, template_path='./resources/template.jpg'):
    tpl = cv2.imread(template_path)
    # tpl = cv2.cvtColor(tpl, cv2.COLOR_BGR2RGB)

    contours = find_contours(file_path)
    contours = shift_center(contours)
    cv2.drawContours(tpl, contours, -1, (181, 145, 98), thickness=2, lineType=cv2.LINE_AA)
    
    if fill:
        # grey = (51, 54, 56)
        silhouette = 142, 100, 46
        cv2.fillPoly(tpl, pts=contours, color=silhouette)
    
    # plt.imshow(tpl)
    return tpl


if __name__ == '__main__':

    # img_files = glob.glob('./resources/img_pokemon_png/*.png')
    img_files = ['./resources/img_pokemon_png/amoonguss.png']
    output_dir = './resources/img_with_template'

    for img_file in img_files:
        tail = img_file.split('/')[-1]

        try:
            result = plot_on_template(img_file)

            tail_jpg = tail[:-3] + 'jpg'
            cv2.imwrite(f'{output_dir}/{tail_jpg}', result)
        
        except Exception as e:
            print(e)
            print(tail)