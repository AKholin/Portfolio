import math
import pickle
import sys
import time
import winsound
from os import listdir, mkdir
from os.path import isfile, isdir, join, exists

from PIL import Image, ImageFont, ImageDraw

start_work = time.time()
# ==============================================

# ----------------------------------------------
#            ***  DIRECTORY  ***
check_dir = 'C:/Python/Tasks/Task/Rename/Field_check'
# ==============================================

# ----------------------------------------------
#               ***  FUNCTIONS  ***
def seconds_to_m_s(seconds):
    minutes = math.floor(seconds // 60)
    seconds = math.ceil(seconds % 60)
    return minutes, seconds

def num_class_to_word(nclass):
    if nclass == 0:
        wclass = 'M1A2'
    elif nclass == 1:
        wclass = 'TYP98'
    elif nclass == 2:
        wclass = 'T90'
    elif nclass == 3:
        wclass = 'LAV25'
    elif nclass == 4:
        wclass = 'WZ551'
    elif nclass == 5:
        wclass = 'BTR90'
    elif nclass == 6:
        wclass = 'M6'
    elif nclass == 7:
        wclass = 'TYP95'
    elif nclass == 8:
        wclass = 'TUNG'
    elif nclass == 9:
        wclass = 'HMWV'
    elif nclass == 10:
        wclass = 'NANJ'
    elif nclass == 11:
        wclass = 'VODNK'
    elif nclass == 12:
        wclass = 'FAAV'
    elif nclass == 13:
        wclass = 'PARAT'
    elif nclass == 14:
        wclass = 'AH1Z'
    elif nclass == 15:
        wclass = 'Z10'
    elif nclass == 16:
        wclass = 'HAVOC'
    elif nclass == 17:
        wclass = 'UH60'
    elif nclass == 18:
        wclass = 'Z8'
    elif nclass == 19:
        wclass = 'MI17'
    elif nclass == 20:
        wclass = 'BOAT'
    else:
        wclass = 'UNKNW'
    return wclass

def highlight_boxes(image, boxes):
    colors = what_color_objects()

    for box in range(len(boxes)):
        color = next(colors)
        min_x, max_x, min_y, max_y = boxes[box][1]

        draw = ImageDraw.Draw(image)
        draw.rectangle(((min_y, min_x), (max_y, max_x)), fill=None, outline=color)
        font = ImageFont.truetype("calibri.ttf", 30)
        text = num_class_to_word(boxes[box][0])

        if 334 - max_x > 22:
            draw.text((min_y, max_x), text, fill=color, font=font, align="right") #   “left”, “center” or “right”.
        elif min_x - 26 > 0:
            draw.text((min_y, min_x - 26), text, fill=color, font=font, align="right")  # “left”, “center” or “right”.

def what_color_objects():
    color_ind = 0

    # colors_objects = ((255, 128, 0), (0, 128, 255), (0, 255, 0), (255, 0, 128), (255, 255, 0), (0, 255, 255), (255, 0, 255), (0, 255, 128))
    colors_objects = ((255, 128, 0), (0, 255, 0), (255, 0, 128), (0, 128, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255), (0, 255, 128))

    while True:
        color = colors_objects[color_ind]
        color_ind += 1
        if color_ind == len(colors_objects):
            color_ind = 0
        yield color

def predicted_left_time(total_imgs, current_img, start_time):
    pass_imgs = current_img + 1
    left_imgs = total_imgs - pass_imgs
    if left_imgs != 0:
        now_time = time.time()
        one_img_seconds = (now_time - start_time) / pass_imgs
        left_seconds = one_img_seconds * left_imgs
        left_time = seconds_to_m_s(left_seconds)
        print('Images left:', left_imgs)
        print("Predicted left time {0} minutes {1} seconds".format(left_time[0], left_time[1]))
# ==============================================

# ----------------------------------------------
#    ***  OPEN and PREPARE DATA, IMAGES  ***
file = open(join(check_dir, '!_field_labels.p'), 'rb')
labels_dict = pickle.load(file)
file.close()

folder_list = [dir for dir in listdir(check_dir) if isdir(join(check_dir, dir))]

if 'ZV_QUANTITY' in folder_list:
    index = folder_list.index('ZV_QUANTITY')
    del folder_list[index]

if '!_Allready' in folder_list:
    index = folder_list.index('!_Allready')
    del folder_list[index]

start = time.time()
# ==============================================

# ----------------------------------------------
#          ***  CHECK IMAGES  ***
for name_dir in folder_list:
    current_dir = join(check_dir, name_dir)

    # current_out_dir = join(current_dir, '{}_out'.format(name_dir))
    #
    # if exists(current_out_dir) == False:
    #     mkdir(current_out_dir)

    folder_images_list = [f for f in listdir(current_dir) if isfile(join(current_dir, f))]
    # folder_images_list = folder_images_list[1:]
    print('{}: {}'.format(name_dir, len(folder_images_list)))

    for img_ind in range(len(folder_images_list)):
        img_name = folder_images_list[img_ind]
        print('\n{0}/{1} Image name: {2}'.format(img_ind + 1, len(folder_images_list), img_name))

        if img_name not in labels_dict:
            print("Image name isn't in data dict")
            sys.exit()

        img = Image.open(join(current_dir, img_name))

        if img.size != (454, 334):
            print('Image have wrong size')
            sys.exit()

        objects = labels_dict[img_name]
        print('Objects =', len(objects), objects)

        highlight_boxes(img, objects)

        # save out image
        img.save(join(current_dir, img_name)) # current_out_dir
        if (img_ind + 1) % 5 == 0:
            predicted_left_time(len(folder_images_list), img_ind, start)

# ==============================================

# //////////////////////////////////////////////
end_work = time.time()
winsound.Beep(432, 700)
winsound.Beep(432, 300)
winsound.Beep(432, 300)
work_time = seconds_to_m_s(end_work - start_work)
print("\nAll work took {} minutes {} seconds".format(work_time[0], work_time[1]))