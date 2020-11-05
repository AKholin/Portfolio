from tkinter import *
from PIL import Image, ImageTk
import numpy as np
from os import listdir, mkdir
from os.path import isfile, isdir, join, exists
import time
import math
import pickle
import sys

start = time.time()
# ----------------------------------------------
root = Tk()
root.title('Mark objects')
# ==============================================

# ----------------------------------------------
#            ***  DIRECTORY  ***
pack_dir = 'C:/Python/Projects/Task/Pack_big'
work_folder = 'Group_456'
current_dir = join(pack_dir, work_folder)
new_objs_dir = '/Python/Tasks/Task/Objects/00_All'
objects_dir = '/Python/Tasks/Task/Objects'
# ==============================================

# ----------------------------------------------
#               ***  GLOBAL  ***
current_box = 0
objects_img = []
img_name = 0
total_objects = 0
pass_objects = 0
start_mark = 0
update_time = 0
current_in_dict = 0

img_ind = 0
sub_img_ind = 0
last_ind = 0
# ==============================================

# ----------------------------------------------
#               ***  FUNCTIONS  ***
def seconds_to_m_s(seconds):
    minutes = math.floor(seconds // 60)
    seconds = math.ceil(seconds % 60)
    return minutes, seconds

def seconds_to_h_m_s(all_seconds):
    hour = math.floor(all_seconds // 3600)
    minutes = math.floor(all_seconds % 3600 // 60)
    seconds = math.ceil(all_seconds % 3600 % 60)
    return hour, minutes, seconds

def calculated_finish_time(quantity):
    start_time = time.localtime()
    print('Start work at {0}:{1}:{2}'.format(start_time.tm_hour, start_time.tm_min, start_time.tm_sec))
    start_seconds = start_time.tm_hour * 3600 + start_time.tm_min * 60 + start_time.tm_sec
    spent_seconds = 4 * quantity
    spent_time = seconds_to_h_m_s(spent_seconds)
    print("Calculated spent time {0} hours {1} minutes {2} seconds".format(spent_time[0], spent_time[1], spent_time[2]))
    finish_time = seconds_to_h_m_s(spent_seconds + start_seconds)
    print("Calculated finish time at {0}:{1}:{2}".format(finish_time[0], finish_time[1], finish_time[2]))

def spent_left_time(total_objs, pass_objs, start_time):
    left_objs = total_objs - pass_objs
    now_time = time.time()
    spent_time = now_time - start_time
    one_obj_seconds = spent_time / pass_objs
    spent_time = seconds_to_m_s(now_time - start_time)
    left_time = seconds_to_m_s(one_obj_seconds * left_objs)
    return spent_time, left_time

def next_name_dict(current):
    name = current.split('.')
    name = name[0].split('_')
    ind = int(name[-1]) + 1
    if ind < 10:
        next = '00' + str(ind)
    elif ind < 100:
        next = '0' + str(ind)
    else:
        next = str(ind)
    return next

def next_name_new(directory):
    dir_folder_lst = [dir for dir in listdir(directory) if isdir(join(directory, dir))]
    last_name = dir_folder_lst[-1].split('_')
    ind = int(last_name[1]) + 1
    if ind < 10:
        next_name = last_name[0] + '_00' + str(ind)
    elif ind < 100:
        next_name = last_name[0] + '_0' + str(ind)
    else:
        next_name = last_name[0] + '_' + str(ind)

    mkdir(join(directory, next_name))
    return next_name

def num_class_to_word(nclass):
    if nclass == 0:
        wclass = '00_M1A2'
    elif nclass == 1:
        wclass = '01_TYPE98'
    elif nclass == 2:
        wclass = '02_T90'
    elif nclass == 3:
        wclass = '03_LAV25'
    elif nclass == 4:
        wclass = '04_WZ551'
    elif nclass == 5:
        wclass = '05_BTR90'
    elif nclass == 6:
        wclass = '06_M6BRADLY'
    elif nclass == 7:
        wclass = '07_TYPE95'
    elif nclass == 8:
        wclass = '08_TUNGUSKA'
    elif nclass == 9:
        wclass = '09_HMMWV'
    elif nclass == 10:
        wclass = '10_NANJING'
    elif nclass == 11:
        wclass = '11_VODNIK'
    elif nclass == 12:
        wclass = '12_FAAV'
    elif nclass == 13:
        wclass = '13_PARATR'
    elif nclass == 14:
        wclass = '14_AH1Z'
    elif nclass == 15:
        wclass = '15_Z10'
    elif nclass == 16:
        wclass = '16_HAVOC'
    elif nclass == 17:
        wclass = '17_UH60'
    elif nclass == 18:
        wclass = '18_Z8'
    elif nclass == 19:
        wclass = '19_MI17'
    elif nclass == 20:
        wclass = '20_BOAT'
    elif nclass == '?':
        wclass = 'UNKNOW'
    else:
        wclass = 200
        print('Somthing went wrong')
    return wclass

def what_color_objects():
    color_ind = 0

    colors_objects = ((255, 128, 0), (0, 128, 255), (0, 255, 0), (255, 0, 128),
                  (255, 255, 0), (0, 255, 255), (255, 0, 255), (0, 255, 128))
    while True:
        color = colors_objects[color_ind]
        color_ind += 1
        if color_ind == len(colors_objects):
            color_ind = 0
        yield color

def highlight_all_boxes(imray, boxes):
    colors = what_color_objects()

    for box in boxes:
        box_color = next(colors)
        min_x, max_x, min_y, max_y = box
        for sq in range(min_x, max_x + 1):
            imray[sq][min_y] = box_color
            imray[sq][max_y] = box_color

        for sq in range(min_y, max_y):
            imray[min_x][sq] = box_color
            imray[max_x][sq] = box_color

def highlight_current_object(imray, box):
    small_x = 21
    small_y = 23

    min_x, max_x, min_y, max_y = box

    if max_x - min_x >= small_x and max_y - min_y >= small_y:
        box_color = (255, 128, 0)  # orange
    else:
        box_color = (255, 0, 255)  # magenta

    for sq in range(min_x, max_x + 1):
        imray[sq][min_y] = box_color
        imray[sq][max_y] = box_color

    for sq in range(min_y, max_y):
        imray[min_x][sq] = box_color
        imray[max_x][sq] = box_color

def save_dict():
    if img_ind < (len(folder_files)-1):
        labels_dict['last'] = folder_files[img_ind]
    else:
        if 'last' in labels_dict:
            del labels_dict['last']

    # if 'last' in labels_dict:
    #     del labels_dict['last']

    file = open(join(objects_dir, '!_Labels_{}.p'.format(next_dict_name)), 'wb')
    pickle.dump(labels_dict, file)
    file.close()
    print('Data saved')
    close_window()

def close_window():
    root.destroy()

def assign_class(nclass):
    global img_ind
    global sub_img_ind
    global img_name
    global color_img
    global coordinates
    global current_box
    global objects_img
    global start_mark

    global info_text
    global button_prev
    global button_next

    global frame_info_folder
    global frame_info_img_ind
    global frame_info_img_name
    global frame_info_sub_img_ind
    global frame_info_in_dict
    global frame_info_pass_time
    global frame_info_objs_left
    global frame_info_pred_time

    global info_text_folder
    global info_img_ind
    global info_img_name
    global info_sub_img_ind
    global info_in_dict
    global info_pass_time
    global info_objs_left
    global info_pred_time

    if img_ind >= len(folder_files):
        save_dict()

    if img_ind == 0 and sub_img_ind == 0 or img_ind == last_ind:
        start_mark = time.time()
        info_text.grid_forget()
        # ----------------------------------------------
        frame_info_folder = LabelFrame(frame_info, padx=5, pady=5)
        frame_info_folder.grid(row=0, column=0)
        # ----------------------------------------------
        frame_info_img_ind = LabelFrame(frame_info, padx=5, pady=5)
        frame_info_img_ind.grid(row=0, column=1)
        # ----------------------------------------------
        frame_info_img_name = LabelFrame(frame_info, padx=5, pady=5)
        frame_info_img_name.grid(row=0, column=2)
        # ----------------------------------------------
        frame_info_sub_img_ind = LabelFrame(frame_info, padx=5, pady=5)
        frame_info_sub_img_ind.grid(row=0, column=3)
        # ----------------------------------------------
        frame_info_in_dict = LabelFrame(frame_info, padx=5, pady=5)
        frame_info_in_dict.grid(row=0, column=4)
        # ----------------------------------------------
        frame_info_pass_time = LabelFrame(frame_info, padx=5, pady=5)
        frame_info_pass_time.grid(row=0, column=5)
        # ----------------------------------------------
        frame_info_objs_left = LabelFrame(frame_info, padx=5, pady=5)
        frame_info_objs_left.grid(row=0, column=6)
        # ----------------------------------------------
        frame_info_pred_time = LabelFrame(frame_info, padx=5, pady=5)
        frame_info_pred_time.grid(row=0, column=7)

    if sub_img_ind != 0:
        if nclass != '?':
            object = [nclass, current_box]
            objects_img.append(object)

        sub_img_ind += 1

        if sub_img_ind <= len(coordinates):
            current_box = coordinates[sub_img_ind - 1]
            update_object()

        if sub_img_ind > len(coordinates):
            sub_img_ind = 0
            img_ind += 1

            if img_ind == (len(folder_files) - 1):
                button_next = Button(frame_service, text=' >> ', padx=30, pady=14, state=DISABLED)
            else:
                button_next = Button(frame_service, text=' >> ', padx=30, pady=14, command=lambda: next_prev_image(1))

            button_next.config(font=("Calibri", 14))
            button_next.grid(row=0, column=6, sticky="we")

            labels_dict[img_name] = objects_img
            name_to_move = what_folder_move(objects_img)

            # if name_to_move == '':
            #     name_to_move = 'ZW_DELETED'

            move_dict[img_name] = name_to_move
            objects_img = []

            if img_ind == len(folder_files):
                save_dict()

    if sub_img_ind == 0 and img_ind < len(folder_files):
        img_name = folder_files[img_ind]

        name_in_dict(img_name)

        # ++++++++++++++++++++++++++++++++++++++++++++++
        info_text_folder.pack_forget()
        info_text_folder = Label(frame_info_folder, text=str(work_folder), padx=10)
        info_text_folder.config(font=("Calibri", 14))
        info_text_folder.pack()
        # ----------------------------------------------
        info_img_ind.pack_forget()
        info_img_ind = Label(frame_info_img_ind, text='Img: {0}/{1}'.format(img_ind + 1, len(folder_files)), padx=10)
        info_img_ind.config(font=("Calibri", 14))
        info_img_ind.pack()
        # ----------------------------------------------
        info_img_name.pack_forget()
        info_img_name = Label(frame_info_img_name, text=img_name, padx=10)
        info_img_name.config(font=("Calibri", 14))
        info_img_name.pack()
        # ----------------------------------------------
        # info_in_dict.pack_forget()
        # info_in_dict = Label(frame_info_in_dict, text='In dict [{}]'.format(in_dict[sub_img_ind]), padx=10)
        # info_in_dict.config(font=("Calibri", 14))
        # info_in_dict.pack()
        # ======================================

        coordinates = coordinates_dict[img_name]
        current_box = coordinates[sub_img_ind]

        color_img.grid_forget()
        color_img = Label(frame_img, image=ready_images[img_ind][sub_img_ind], padx=5, pady=5)
        color_img.grid(row=0, column=0)

        sub_img_ind += 1
        update_object()

        if img_ind == 0:
            button_prev = Button(frame_service, text=' << ', padx=30, pady=14, state=DISABLED)
        else:
            button_prev = Button(frame_service, text=' << ', padx=30, pady=14, command=lambda: next_prev_image(-1))

        button_prev.config(font=("Calibri", 14))
        button_prev.grid(row=0, column=3, sticky="we")

def update_object():
    global info_sub_img_ind
    global wb_img
    global pass_objects
    global info_objs_left
    global info_pass_time
    global info_pred_time
    global info_in_dict
    global update_time

    info_sub_img_ind.pack_forget()
    info_sub_img_ind = Label(frame_info_sub_img_ind, text='Objects: {0}/{1}'.format(sub_img_ind, len(ready_images[img_ind]) - 1), padx=10)
    info_sub_img_ind.config(font=("Calibri", 14))
    info_sub_img_ind.pack()

    wb_img.grid_forget()
    wb_img = Label(frame_img, image=ready_images[img_ind][sub_img_ind], padx=5, pady=5)
    wb_img.grid(row=0, column=1)

    info_in_dict.pack_forget()
    info_in_dict = Label(frame_info_in_dict, text='In dict [{}]'.format(current_in_dict[sub_img_ind-1]), padx=10)
    info_in_dict.config(font=("Calibri", 14))
    info_in_dict.pack()

    pass_objects += 1
    info_objs_left.pack_forget()
    info_objs_left = Label(frame_info_objs_left, text='Objs left: {0}/{1}'.format(total_objects - pass_objects, total_objects), padx=10)
    info_objs_left.config(font=("Calibri", 14))
    info_objs_left.pack()

    if pass_objects > 1:
        update_time = spent_left_time(total_objects, pass_objects, start_mark)

        info_pass_time.pack_forget()
        info_pass_time = Label(frame_info_pass_time, text='{0}:{1}'.format(update_time[0][0], update_time[0][1]), padx=10)
        info_pass_time.config(font=("Calibri", 14))
        info_pass_time.pack()

        info_pred_time.pack_forget()
        info_pred_time = Label(frame_info_pred_time, text='{0}:{1}'.format(update_time[1][0], update_time[1][1]), padx=10)
        info_pred_time.config(font=("Calibri", 14))
        info_pred_time.pack()

def name_in_dict(name):
    global current_in_dict

    current_in_dict = []

    if name in labels_dict:
        coordinates = coordinates_dict[name]
        objects = labels_dict[name]
        i_obj = 0
        for points in coordinates:
            if i_obj < len(objects):
                nclass, box_obj = objects[i_obj]

                if points == box_obj:
                    current_in_dict.append(num_class_to_word(nclass))
                    i_obj += 1
                else:
                    current_in_dict.append('No')
            else:
                current_in_dict.append('No')
    else:
        for n in range(len(coordinates_dict[name])):
            current_in_dict.append('No')

def show_img():
    coordinates = coordinates_dict[img_name]
    img_open = Image.open(join(current_dir, img_name))
    rgb_img = img_open.convert('RGB')
    rgb_array = np.array(rgb_img)
    highlight_all_boxes(rgb_array, coordinates)
    color_img_pil = Image.fromarray(rgb_array, 'RGB')
    color_img_pil.show()

def next_prev_image(act):
    global img_ind
    global sub_img_ind
    global button_prev
    global button_next

    img_ind = img_ind + act
    sub_img_ind = 0

    if img_ind == 0:
        button_prev = Button(frame_service, text=' << ', padx=30, pady=14, state=DISABLED)
    else:
        button_prev = Button(frame_service, text=' << ', padx=30, pady=14, command=lambda: next_prev_image(-1))

    if img_ind == (len(folder_files)-1):
        button_next = Button(frame_service, text=' >> ', padx=30, pady=14, state=DISABLED)
    else:
        button_next = Button(frame_service, text=' >> ', padx=30, pady=14, command=lambda: next_prev_image(1))

    button_prev.config(font=("Calibri", 14))
    button_prev.grid(row=0, column=3, sticky="we")

    button_next.config(font=("Calibri", 14))
    button_next.grid(row=0, column=6, sticky="we")

    assign_class('?')

def delete_image():
    if img_name in labels_dict:
        del labels_dict[img_name]

    move_to_folder('ZW_DELETED')

def what_paint():
    if img_name in change_dict:
        buffer = change_dict[img_name]
        buffer.append(current_box)
        change_dict[img_name] = buffer
    else:
        buffer = []
        buffer.append(current_box)
        change_dict[img_name] = buffer

    assign_class('?')

def paint_object(imray, box):
    min_x, max_x, min_y, max_y = box

    w_n = imray[min_x, min_y]
    w_s = imray[max_x, min_y]
    e_n = imray[min_x, max_y]
    e_s = imray[max_x, max_y]

    r = sum([w_n[0], w_s[0], e_n[0], e_s[0]]) // 4
    g = sum([w_n[1], w_s[1], e_n[1], e_s[1]]) // 4
    b = sum([w_n[2], w_s[2], e_n[2], e_s[2]]) // 4

    box_color = (r, g, b)

    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            imray[x, y] = box_color

def move_to_folder(folder):
    move_dict[img_name] = folder
    if img_ind < len(folder_files):
        next_prev_image(1)

def name_folder_move(objects):
    name_list = []
    for nclass, box in objects:
        name_list.append(num_class_to_word(nclass))

    name_list = list(set(name_list))
    name_list.sort()
    sep = '_'
    folder_name = sep.join(name_list)
    return folder_name

def what_folder_move(objects):
    if objects != []:
        if len(objects) > 1:
            objects = sorted(objects, key=lambda coord: (coord[1][1] - coord[1][0]) * (coord[1][3] - coord[1][2]), reverse=True)
            return '{}_g'.format(num_class_to_word(objects[0][0]))
        else:
            return '{}_s'.format(num_class_to_word(objects[0][0]))
    else:
        return 'ZW_DELETED'


# ==============================================

# ----------------------------------------------
#       ***  OPEN and PREPARE DATA  ***
folder_files = [f for f in listdir(current_dir) if isfile(join(current_dir, f))]

if '!' not in folder_files[0]:
    print('There are no data dictionary in this folder')
    sys.exit()

file = open(join(current_dir, folder_files[0]), 'rb')
coordinates_dict = pickle.load(file)
file.close()

dictionaries = [f for f in listdir(objects_dir) if isfile(join(objects_dir, f))]
current_dict_name = dictionaries[-1]
next_dict_name = next_name_dict(current_dict_name)

file = open(join(objects_dir, current_dict_name), 'rb')
labels_dict = pickle.load(file)
file.close()

while '!' in folder_files[0]:
    folder_files = folder_files[1:]

change_dict = {}
move_dict = {}
# ==============================================

# ----------------------------------------------
#      ***  OPEN and PREPARE IMAGES  ***
ready_images = []

for img_name in folder_files:
    one_image_sub_imgs = []
    coordinates = coordinates_dict[img_name]

    img_open = Image.open(join(current_dir, img_name))
    rgb_img = img_open.convert('RGB')
    rgb_array = np.array(rgb_img)
    highlight_all_boxes(rgb_array, coordinates)
    color_img_pil = Image.fromarray(rgb_array, 'RGB')
    color_img = ImageTk.PhotoImage(color_img_pil)
    one_image_sub_imgs.append(color_img)

    # rgb to white black
    wb = rgb_img.convert('L')  # convert rgb to white black to remove color
    wb_rgb = wb.convert('RGB')  # convert back to rgb without color
    wb_rgb_array = np.array(wb_rgb)  # convert to numpy array

    for box in coordinates:
        cur_wb_array = np.copy(wb_rgb_array)
        highlight_current_object(cur_wb_array, box)
        wb_img_pil = Image.fromarray(cur_wb_array, 'RGB')
        wb_img = ImageTk.PhotoImage(wb_img_pil)
        one_image_sub_imgs.append(wb_img)

    total_objects = total_objects + len(one_image_sub_imgs) - 1
    ready_images.append(one_image_sub_imgs)

print('Total images', len(folder_files))
print('Total objects', total_objects)

calculated_finish_time(total_objects)
# ==============================================

# ----------------------------------------------
#           ***  LOAD LAST IMAGE  ***
if 'last' in labels_dict:
    last = labels_dict['last']
    if last in folder_files:
        for last_ind in range(len(folder_files)):
            if folder_files[last_ind] == last:
                img_ind = last_ind
                break
# ==============================================

# ----------------------------------------------
#           ***  IMAGES FRAME  ***
frame_img = LabelFrame(root, padx=5, pady=5)
frame_img.pack(padx=10, pady=10)

start_color_img = ImageTk.PhotoImage(Image.open('C:/Python/Projects/Task/Stock/start_color_img.jpg'))
start_wb_img = ImageTk.PhotoImage(Image.open('C:/Python/Projects/Task/Stock/start_wb_img.jpg'))
# ++++++++++++++++++++++++++++++++++++++++++++++
color_img = Label(frame_img, image=start_color_img, padx=5, pady=5)
color_img.grid(row=0, column=0)
# ++++++++++++++++++++++++++++++++++++++++++++++
wb_img = Label(frame_img, image=start_wb_img, padx=5, pady=5)
wb_img.grid(row=0, column=1)
# ==============================================

# ----------------------------------------------
#           ***  INFO FRAME  ***
frame_info = LabelFrame(root, padx=5, pady=5)
frame_info.pack(padx=10, pady=10)
# ++++++++++++++++++++++++++++++++++++++++++++++
frame_info_folder = LabelFrame(frame_info, padx=5, pady=5)
frame_info_folder.grid(row=0, column=0)

info_text_folder = Label(frame_info_folder, text='folder', padx=10)
info_text_folder.config(font=("Courier", 14))
info_text_folder.pack()
# ----------------------------------------------
frame_info_img_ind = LabelFrame(frame_info, padx=5, pady=5)
frame_info_img_ind.grid(row=0, column=1)

info_img_ind = Label(frame_info_img_ind, text='1/77', padx=10)
info_img_ind.config(font=("Courier", 14))
info_img_ind.pack()
# ----------------------------------------------
frame_info_img_name = LabelFrame(frame_info, padx=5, pady=5)
frame_info_img_name.grid(row=0, column=2)

info_img_name = Label(frame_info_img_name, text='064532.png', padx=10)
info_img_name.config(font=("Courier", 14))
info_img_name.pack()
# ----------------------------------------------
frame_info_sub_img_ind = LabelFrame(frame_info, padx=5, pady=5)
frame_info_sub_img_ind.grid(row=0, column=3)

info_sub_img_ind = Label(frame_info_sub_img_ind, text='1/2', padx=10)
info_sub_img_ind.config(font=("Courier", 14))
info_sub_img_ind.pack()
# ----------------------------------------------
frame_info_in_dict = LabelFrame(frame_info, padx=5, pady=5)
frame_info_in_dict.grid(row=0, column=4)

info_in_dict = Label(frame_info_in_dict, text='in dict [Yes]', padx=10)
info_in_dict.config(font=("Courier", 14))
info_in_dict.pack()
# ----------------------------------------------
frame_info_pass_time = LabelFrame(frame_info, padx=5, pady=5)
frame_info_pass_time.grid(row=0, column=5)

info_pass_time = Label(frame_info_pass_time, text='0:12:00', padx=10)
info_pass_time.config(font=("Courier", 14))
info_pass_time.pack()
# ----------------------------------------------
frame_info_objs_left = LabelFrame(frame_info, padx=5, pady=5)
frame_info_objs_left.grid(row=0, column=6)

info_objs_left = Label(frame_info_objs_left, text='35', padx=10)
info_objs_left.config(font=("Courier", 14))
info_objs_left.pack()
# ----------------------------------------------
frame_info_pred_time = LabelFrame(frame_info, padx=5, pady=5)
frame_info_pred_time.grid(row=0, column=7)

info_pred_time = Label(frame_info_pred_time, text='0:12:00', padx=10)
info_pred_time.config(font=("Courier", 14))
info_pred_time.pack()
# ++++++++++++++++++++++++++++++++++++++++++++++
frame_info_folder.grid_forget()
frame_info_img_ind.grid_forget()
frame_info_img_name.grid_forget()
frame_info_sub_img_ind.grid_forget()
frame_info_in_dict.grid_forget()
frame_info_pass_time.grid_forget()
frame_info_objs_left.grid_forget()
frame_info_pred_time.grid_forget()
# ----------------------------------------------
info_text_str = 'Press any key class to start mark images'
info_text = Label(frame_info, text=info_text_str, padx=10)
info_text.config(font=("Courier", 24))
info_text.grid(row=0, column=0)
# ==============================================

# ----------------------------------------------
#           ***  CLASSES FRAME  ***
frame_class = LabelFrame(root, padx=5, pady=5)
frame_class.pack(padx=10, pady=10)

# ++++++++++++++++++++++++++++++++++++++++++++++
button_m1a2 = Button(frame_class, text='00  M1A2', padx=30, pady=14, command=lambda: assign_class(0))
button_m1a2.config(font=("Calibri", 14))
button_typ98 = Button(frame_class, text='01  TYPE98', padx=30, pady=14, command=lambda: assign_class(1))
button_typ98.config(font=("Calibri", 14))
button_t90 = Button(frame_class, text='02  T90', padx=30, pady=14, command=lambda: assign_class(2))
button_t90.config(font=("Calibri", 14))

button_lav25 = Button(frame_class, text='03  LAV25', padx=30, pady=14, command=lambda: assign_class(3))
button_lav25.config(font=("Calibri", 14))
button_wz551 = Button(frame_class, text='04  WZ551', padx=30, pady=14, command=lambda: assign_class(4))
button_wz551.config(font=("Calibri", 14))
button_btr90 = Button(frame_class, text='05  BTR90', padx=30, pady=14, command=lambda: assign_class(5))
button_btr90.config(font=("Calibri", 14))

button_m6 = Button(frame_class, text='06 M6  BRADLY', padx=30, pady=14, command=lambda: assign_class(6))
button_m6.config(font=("Calibri", 14))
button_typ95 = Button(frame_class, text='07  TYPE95', padx=30, pady=14, command=lambda: assign_class(7))
button_typ95.config(font=("Calibri", 14))
button_tungs = Button(frame_class, text='08  TUNGUSKA', padx=30, pady=14, command=lambda: assign_class(8))
button_tungs.config(font=("Calibri", 14))

button_hamer = Button(frame_class, text='09  HMMWV', padx=30, pady=14, command=lambda: assign_class(9))
button_hamer.config(font=("Calibri", 14))
button_nanji = Button(frame_class, text='10  NANJING', padx=30, pady=14, command=lambda: assign_class(10))
button_nanji.config(font=("Calibri", 14))
button_vodnk = Button(frame_class, text='11  VODNIK', padx=30, pady=14, command=lambda: assign_class(11))
button_vodnk.config(font=("Calibri", 14))

button_faav = Button(frame_class, text='12  FAAV', padx=30, pady=14, command=lambda: assign_class(12))
button_faav.config(font=("Calibri", 14))
button_parat = Button(frame_class, text='13  PARATR', padx=30, pady=14, command=lambda: assign_class(13))
button_parat.config(font=("Calibri", 14))
button_boat = Button(frame_class, text='20  BOAT', padx=30, pady=14, command=lambda: assign_class(20))
button_boat.config(font=("Calibri", 14))

button_ah1z = Button(frame_class, text='14  AH1Z', padx=30, pady=14, command=lambda: assign_class(14))
button_ah1z.config(font=("Calibri", 14))
button_z10 = Button(frame_class, text='15  Z10', padx=30, pady=14, command=lambda: assign_class(15))
button_z10.config(font=("Calibri", 14))
button_havoc = Button(frame_class, text='16  HAVOC', padx=30, pady=14, command=lambda: assign_class(16))
button_havoc.config(font=("Calibri", 14))

button_uh60 = Button(frame_class, text='17  UH60', padx=30, pady=14, command=lambda: assign_class(17))
button_uh60.config(font=("Calibri", 14))
button_z8 = Button(frame_class, text='18  Z8', padx=30, pady=14, command=lambda: assign_class(18))
button_z8.config(font=("Calibri", 14))
button_mi17 = Button(frame_class, text='19  MI17', padx=30, pady=14, command=lambda: assign_class(19))
button_mi17.config(font=("Calibri", 14))
# **********************************************

button_m1a2.grid(row=0, column=0, sticky="we")
button_lav25.grid(row=0, column=1, sticky="we")
button_m6.grid(row=0, column=2, sticky="we")
button_hamer.grid(row=0, column=3, sticky="we")
button_faav.grid(row=0, column=4, sticky="we")
button_ah1z.grid(row=0, column=5, sticky="we")
button_uh60.grid(row=0, column=6, sticky="we")

button_typ98.grid(row=1, column=0, sticky="we")
button_wz551.grid(row=1, column=1, sticky="we")
button_typ95.grid(row=1, column=2, sticky="we")
button_nanji.grid(row=1, column=3, sticky="we")
button_parat.grid(row=1, column=4, sticky="we")
button_z10.grid(row=1, column=5, sticky="we")
button_z8.grid(row=1, column=6, sticky="we")

button_t90.grid(row=2, column=0, sticky="we")
button_btr90.grid(row=2, column=1, sticky="we")
button_tungs.grid(row=2, column=2, sticky="we")
button_vodnk.grid(row=2, column=3, sticky="we")
button_boat.grid(row=2, column=4, sticky="we")
button_havoc.grid(row=2, column=5, sticky="we")
button_mi17.grid(row=2, column=6, sticky="we")
# ==============================================

# ----------------------------------------------
#         ***  SERVICE FRAME  ***
frame_service = LabelFrame(root, padx=5, pady=5)
frame_service.pack(padx=10, pady=10)

button_exit = Button(frame_service, text='EXIT', padx=30, pady=14, command=save_dict)
button_exit.config(font=("Calibri", 14))
button_show = Button(frame_service, text='SHOW', padx=30, pady=14, command=show_img)
button_show.config(font=("Calibri", 14))
button_del = Button(frame_service, text='DELETE', padx=30, pady=14, command=delete_image)
button_del.config(font=("Calibri", 14))
button_prev = Button(frame_service, text=' << ', padx=30, pady=14, state=DISABLED)
button_prev.config(font=("Calibri", 14))
button_unknow = Button(frame_service, text='  ?  ', padx=30, pady=14, command=lambda: assign_class('?'))
button_unknow.config(font=("Calibri", 14))
button_paint = Button(frame_service, text=' [?] ', padx=30, pady=14, command=what_paint)
button_paint.config(font=("Calibri", 14))
button_next = Button(frame_service, text=' >> ', padx=30, pady=14, command=lambda: next_prev_image(1))
button_next.config(font=("Calibri", 14))
button_merger = Button(frame_service, text='MERGER', padx=30, pady=14, command=lambda: move_to_folder('ZX_MERGER'))
button_merger.config(font=("Calibri", 14))
button_near = Button(frame_service, text='NEAR', padx=30, pady=14, command=lambda: move_to_folder('ZY_NEAR'))
button_near.config(font=("Calibri", 14))
button_extra = Button(frame_service, text='EXTRA', padx=30, pady=14, command=lambda: move_to_folder('ZZ_EXTRA'))
button_extra.config(font=("Calibri", 14))

button_exit.grid(row=0, column=0, sticky="we")
button_show.grid(row=0, column=1, sticky="we")
button_del.grid(row=0, column=2, sticky="we")
button_prev.grid(row=0, column=3, sticky="we")
button_unknow.grid(row=0, column=4, sticky="we")
button_paint.grid(row=0, column=5, sticky="we")
button_next.grid(row=0, column=6, sticky="we")
button_merger.grid(row=0, column=7, sticky="we")
button_near.grid(row=0, column=8, sticky="we")
button_extra.grid(row=0, column=9, sticky="we")
# ==============================================

# ----------------------------------------------
root.mainloop()

end_mark = time.time()
mark_time = seconds_to_m_s(end_mark - start)
print("\nObjects mark took {0} minutes {1} seconds".format(mark_time[0], mark_time[1]))
if pass_objects != 0:
    print('Average seconds to mark one object:', (end_mark - start) / pass_objects)
if img_ind != 0:
    print('Average seconds to mark one image:', (end_mark - start) / img_ind)
print('\nWait, images are moving in folders')

new_folder_name = next_name_new(new_objs_dir)

for img_name in folder_files:
    if img_name in change_dict:
        paint_objs = change_dict[img_name]
        img = Image.open(join(current_dir, img_name))
        rgb = img.convert('RGB')
        rgb_array = np.array(rgb)

        for box in paint_objs:
            paint_object(rgb_array, box)

        img = Image.fromarray(rgb_array, 'RGB')
        if img_name in move_dict:
            folder = move_dict[img_name]
            move_dir = join(objects_dir, folder)
        else:
            move_dir = join(objects_dir, 'ZZ_EXTRA')

        if exists(move_dir) == False:
            mkdir(move_dir)

        img.save(join(move_dir, img_name))

        if folder != 'ZW_DELETED' and folder != 'ZX_MERGER' and folder != 'ZY_NEAR' and folder != 'ZZ_EXTRA':
            img.save(join(new_objs_dir, new_folder_name, img_name))

    elif img_name in move_dict:
        folder = move_dict[img_name]
        move_dir = join(objects_dir, folder)

        if exists(move_dir) == False:
            mkdir(move_dir)

        img = Image.open(join(current_dir, img_name))
        img.save(join(move_dir, img_name))

        if folder != 'ZW_DELETED' and folder != 'ZX_MERGER' and folder != 'ZY_NEAR' and folder != 'ZZ_EXTRA':
            img = Image.open(join(current_dir, img_name))
            img.save(join(new_objs_dir, new_folder_name, img_name))

    else:
        move_dir = join(objects_dir, 'ZW_DELETED')

        if exists(move_dir) == False:
            mkdir(move_dir)

        img = Image.open(join(current_dir, img_name))
        img.save(join(move_dir, img_name))

end_work = time.time()
work_time = seconds_to_m_s(end_work - start)
print("All work took {0} minutes {1} seconds".format(work_time[0], work_time[1]))
print('Folder:', work_folder)