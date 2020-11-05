from PIL import Image
import numpy as np
import time
import math
from os import listdir, mkdir
from os.path import isfile, isdir, join, exists
import winsound
import pickle

# without filtered after paint small osnvnoy

def scan_limits(imray):
    len_x = imray.shape[0]
    len_y = imray.shape[1]
    # print('Image size {0} х {1} pixels'.format(len_x, len_y))
    # -----------------------------------------------
    # scan configuration
    distance = 8
    theshold_up = 1.05  # theshold up for main ratio
    theshold_dn = 0.78  # theshold down for main ratio # 0.78 for bright objects
    theshold_m = 1.2  # theshold for magenta
    theshold_c = 1.57  # theshold for cyan
    # ===============================================

    no_objects = True
    limits = [[] for i in range(len_x)]

    found_obj = False
    there_is = False

    for x in range(len_x):
        min_y = None
        for y in range(len_y):
            r, g, b = imray[x, y]
            if r == 0:
                r = 1
            if g == 0:
                g = 1
            if b == 0:
                b = 1

            ratio_br = b / r  # ratio blue to red
            ratio_bg = b / g  # ratio blue to green

            if ratio_br > theshold_dn and ratio_br < theshold_up and ratio_bg > theshold_m: # magenta
                there_is = True
            elif ratio_bg > theshold_dn and ratio_bg < theshold_up and ratio_br > theshold_c: # cyan
                there_is = True

            if r < 45 and g < 45 and b < 45:  # remove black
                there_is = False

            if r > 253 and g > 253 and b > 253:  # remove white
                there_is = False

            # ----------------------------------
            if there_is:
                there_is = False
                no_objects = False

                if found_obj == False:
                    found_obj = True
                    min_y = y
                    max_y = y

                found_y = y

                if min_y > y:
                    min_y = y
                if max_y < y:
                    max_y = y

            else:
                if found_obj:
                    if abs(y - found_y) > distance:
                        found_obj = False
                        limits[x].append((min_y, max_y))
        else:
            found_obj = False
            if min_y != None:
                if limits[x] == [] or limits[x][-1] != (min_y, max_y):
                    limits[x].append((min_y, max_y))

    # for l in range(len(limits)):
    #     if limits[l] != []:
    #         print('Limits[{}] = {}'.format(l, limits[l]))

    if no_objects:
        return 0
    else:
        return limits
    # ==========================================

def scan_objects(limits):
    coordinates = []
    slice = 0
    while slice < len(limits):
        if limits[slice] != []:
            min_x = slice

            min_y = limits[slice][0][0]
            max_y = limits[slice][0][1]
            del limits[slice][0]
            slice += 1

            prev_min_y = min_y
            prev_max_y = max_y

            if slice == len(limits):
                exit = True
            else:
                exit = False

            while not exit:

                len_slice = len(limits[slice])
                check = 0

                point_ind = 0

                slice_min_y = 0
                slice_max_y = 0

                while point_ind < len(limits[slice]):
                    cur_min_y, cur_max_y = limits[slice][point_ind]

                    if prev_max_y >= cur_min_y and cur_max_y >= prev_min_y:
                        del limits[slice][point_ind]

                        if slice_min_y == 0:
                            slice_min_y = cur_min_y
                        else:
                            if cur_min_y < slice_min_y:
                                slice_min_y = cur_min_y

                        if slice_max_y == 0:
                            slice_max_y = cur_max_y
                        else:
                            if cur_max_y > slice_max_y:
                                slice_max_y = cur_max_y
                    else:
                        point_ind += 1
                        check += 1

                    if limits[slice] == []:
                        break
                else:
                    if check == len_slice:
                        max_x = slice - 1
                        coordinates.append((min_x, max_x, min_y, max_y))
                        slice = 0
                        # exit = 1
                        break

                prev_min_y = slice_min_y
                prev_max_y = slice_max_y

                if slice_min_y < min_y:
                    min_y = slice_min_y

                if slice_max_y > max_y:
                    max_y = slice_max_y

                slice += 1

                if slice == len(limits):
                    exit = True
            else:
                max_x = slice - 1
                coordinates.append((min_x, max_x, min_y, max_y))
        else:
            slice += 1
    else:
        if coordinates[-1] != (min_x, max_x, min_y, max_y):
            max_x = slice - 1
            coordinates.append((min_x, max_x, min_y, max_y))

    return coordinates
    # ===============================================

def along_contour_object(objects, len_x, len_y):
    boxes = []
    for points in range(len(objects)):

        min_x, max_x, min_y, max_y = objects[points]

        if min_x != 0:
            min_x -= 1
        if min_y != 0:
            min_y -= 1
        if max_x != (len_x - 1):
            max_x += 1
        if max_y != (len_y - 1):
            max_y += 1

        boxes.append((min_x, max_x, min_y, max_y))
    return boxes

def show_boxes(imray, boxes):

    temp_img = np.copy(imray)
    colors = what_color_objects()

    for box in range(len(boxes)):
        box_color = next(colors)
        min_x, max_x, min_y, max_y = boxes[box]
        for sq in range(min_x, max_x + 1):
            temp_img[sq][min_y] = box_color
            temp_img[sq][max_y] = box_color

        for sq in range(min_y, max_y):
            temp_img[min_x][sq] = box_color
            temp_img[max_x][sq] = box_color

    img = Image.fromarray(temp_img, 'RGB')
    img.show()

def highlight_boxes(imray, boxes):
    colors = what_color_objects()

    for box in range(len(boxes)):
        box_color = next(colors)
        min_x, max_x, min_y, max_y = boxes[box]
        for sq in range(min_x, max_x + 1):
            imray[sq][min_y] = box_color
            imray[sq][max_y] = box_color

        for sq in range(min_y, max_y):
            imray[min_x][sq] = box_color
            imray[max_x][sq] = box_color

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

def filtering_inside(all_objects):
    boxes = []
    objects = all_objects[:]

    for i in range(len(objects)):
        if objects[i] == 0:
            continue
        i_min_x, i_max_x, i_min_y, i_max_y = objects[i]
        for j in range(len(objects)):
            if i == j:
                continue

            if objects[j] == 0:
                continue

            j_min_x, j_max_x, j_min_y, j_max_y = objects[j]

            if j_min_x > i_min_x and j_max_x < i_max_x and j_min_y > i_min_y and j_max_y < i_max_y:
                objects[j] = 0

    for obj in objects:
        if obj != 0:
            boxes.append(obj)
    return boxes

def big_to_small(objects):
    return sorted(objects, key=lambda coord: (coord[1] - coord[0]) * (coord[3] - coord[2]), reverse=True)

def filtering_near(objects):
    border = -10
    distance_near = 3
    boxes = []

    for i in range(len(objects)):
        if objects[i] == 0:
            continue

        buf_min_x = []
        buf_max_x = []
        buf_min_y = []
        buf_max_y = []

        i_min_x, i_max_x, i_min_y, i_max_y = objects[i]
        for j in range(len(objects)):
            if i == j:
                continue

            if objects[j] == 0:
                continue

            j_min_x, j_max_x, j_min_y, j_max_y = objects[j]

            if abs(j_min_x - i_max_x) < distance_near:
                if j_max_y >= i_min_y and j_min_y <= i_max_y:
                    buf_min_x.append(j_min_x)
                    buf_max_x.append(j_max_x)
                    buf_min_y.append(j_min_y)
                    buf_max_y.append(j_max_y)
                    objects[j] = 0

            if abs(j_min_y - i_max_y) < distance_near:
                if j_max_x >= i_min_x and j_min_x <= i_max_x:
                    buf_min_x.append(j_min_x)
                    buf_max_x.append(j_max_x)
                    buf_min_y.append(j_min_y)
                    buf_max_y.append(j_max_y)
                    objects[j] = 0

            if j_min_x - i_min_x > border and \
                    i_max_x - j_max_x > border and \
                    j_min_y - i_min_y > border and \
                    i_max_y - j_max_y > border:

                    buf_min_x.append(j_min_x)
                    buf_max_x.append(j_max_x)
                    buf_min_y.append(j_min_y)
                    buf_max_y.append(j_max_y)
                    objects[j] = 0
        else:
            if buf_min_x != []:
                buf_min_x.append(i_min_x)
                buf_max_x.append(i_max_x)
                buf_min_y.append(i_min_y)
                buf_max_y.append(i_max_y)

                objects[i] = 0
                min_x = min(buf_min_x)
                max_x = max(buf_max_x)
                min_y = min(buf_min_y)
                max_y = max(buf_max_y)

                boxes.append((min_x, max_x, min_y, max_y))

    for obj in objects:
        if obj != 0:
            boxes.append(obj)
    return boxes

def filtering_small(objects):

    min_box_x = 6
    min_box_y = 8
    boxes = []

    for obj in objects:
        min_x, max_x, min_y, max_y = obj
        if max_x - min_x >= min_box_x and max_y - min_y >= min_box_y: # or
            boxes.append(obj)

    if boxes == []:
        return 0
    else:
        #boxes = tuple(boxes)
        return boxes

def paint_small(imray, objects):
    min_box_x = 21
    min_box_y = 23
    boxes = []

    for object in objects:
        min_x, max_x, min_y, max_y = object

        if (max_x - min_x >= min_box_x and max_y - min_y >= min_box_y):
            boxes.append(object)
        else:
            w_n = imray[min_x, min_y]
            w_s = imray[max_x, min_y]
            e_n = imray[min_x, max_y]
            e_s = imray[max_x, max_y]

            r = sum([w_n[0], w_s[0], e_n[0], e_s[0]]) // 4
            g = sum([w_n[1], w_s[1], e_n[1], e_s[1]]) // 4
            b = sum([w_n[2], w_s[2], e_n[2], e_s[2]]) // 4

            box_color = (r, g, b)

            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    imray[x, y] = box_color

    if boxes == []:
        return 0
    else:
        return boxes

def seconds_to_h_m_s(all_seconds):
    hour = math.floor(all_seconds // 3600)
    minutes = math.floor(all_seconds % 3600 // 60)
    seconds = math.ceil(all_seconds % 3600 % 60)
    return hour, minutes, seconds

def now_time_seconds():
    now_time = time.localtime()
    now_time_seconds = now_time.tm_hour * 3600 + now_time.tm_min * 60 + now_time.tm_sec
    return now_time_seconds

def predicted_left_time(total_imgs, current_img, start_time):
    pass_imgs = current_img + 1
    left_imgs = total_imgs - pass_imgs
    if left_imgs != 0:
        now_time = time.time()
        one_img_seconds = (now_time - start_time) / pass_imgs
        left_seconds = one_img_seconds * left_imgs
        left_time = seconds_to_h_m_s(left_seconds)
        print('Images left:', left_imgs)
        print("Predicted left time {0} hours {1} minutes {2} seconds".format(left_time[0], left_time[1], left_time[2]))
        finish_time = seconds_to_h_m_s(now_time_seconds() + left_seconds)
        print("Predicted finish time at {0}:{1}:{2}".format(finish_time[0], finish_time[1], finish_time[2]))

def calculated_finish_time(quantity):
    start_time = time.localtime()
    print('Start work at {0}:{1}:{2}'.format(start_time.tm_hour, start_time.tm_min, start_time.tm_sec))
    start_seconds = now_time_seconds()
    spent_seconds = 6.84 * quantity
    spent_time = seconds_to_h_m_s(spent_seconds)
    print("Calculated spent time {0} hours {1} minutes {2} seconds".format(spent_time[0], spent_time[1], spent_time[2]))
    finish_time = seconds_to_h_m_s(spent_seconds + start_seconds)
    print("Calculated finish time at {0}:{1}:{2}".format(finish_time[0], finish_time[1], finish_time[2]))

def marking_objects_folder(directory, folder):
    start = time.time()
    current_dir = join(directory, folder)
    print('Current_dir:', current_dir)

    out_dir = join(current_dir, (folder + '_out'))
    if exists(out_dir) == False:
        mkdir(out_dir)

    orig_dir = join(current_dir, folder)
    if exists(orig_dir) == False:
        mkdir(orig_dir)

    folder_files = [f for f in listdir(current_dir) if isfile(join(current_dir, f))]

    if '!' in folder_files[0]:
        folder_files = folder_files[1:]
        if '!' in folder_files[0]:
            folder_files = folder_files[1:]

    calculated_finish_time(len(folder_files))

    data_dict = {}

    for img_ind in range(len(folder_files)):
        img_name = folder_files[img_ind]
        print('\n{0}/{1} Image name: {2}'.format(img_ind+1, len(folder_files), img_name))

        img = Image.open(join(current_dir, img_name))
        rgb = img.convert('RGB')
        rgb_array = np.array(rgb)
        len_x = rgb_array.shape[0]
        len_y = rgb_array.shape[1]

        limits = scan_limits(rgb_array)
        if limits != 0:
            all_objects = scan_objects(limits)
            all_objects = along_contour_object(all_objects, len_x, len_y)
            print('All objects =', len(all_objects), all_objects)

            # ++++++++++++++++++++++++++++++++++
            objects = filtering_inside(all_objects)
            objects_sort = big_to_small(objects)
            objects = filtering_near(objects_sort)
            objects = paint_small(rgb_array, objects)
            # ++++++++++++++++++++++++++++++++++

            if objects != 0:
                print('Objects =', len(objects), objects)

                # add to dict
                data_dict[img_name] = objects

                img = Image.fromarray(rgb_array, 'RGB')
                img.save(join(orig_dir, img_name))

                # highlight_boxes
                highlight_boxes(rgb_array, objects)

                # save out image
                img = Image.fromarray(rgb_array, 'RGB')
                img.save(join(out_dir, img_name))

            else:
                print('***  Objects are too small  ***')
        else:
            print('***  There are no objects  ***')

        if (img_ind + 1) % 5 == 0:
            predicted_left_time(len(folder_files), img_ind, start)

    print("\nEnd of folder")
    file = open(join(orig_dir, '!_{}_coordinates.p'.format(folder)), 'wb')
    pickle.dump(data_dict, file)
    file.close()

    end = time.time()
    winsound.Beep(432, 700)
    winsound.Beep(432, 300)
    winsound.Beep(432, 300)
    scan_time = seconds_to_h_m_s(end - start)
    print("\nObjects scan took {0} hours {1} minutes {2} seconds".format(scan_time[0], scan_time[1], scan_time[2]))
    # ==============================================

# ----------------------------------------------
# group_dir = '\Python\Tasks\Task\Group_pack'
# current_folder = 'Pack_029'
group_dir = '\Python\Tasks\Task\Group_photos'
current_folder = 'Rescan_af_01'
# group_dir = '/Python/Tasks/Task/Work'
# current_folder = 'Viewer'
# current_folder = 'G48'
marking_objects_folder(group_dir, current_folder)
# ----------------------------------------------
