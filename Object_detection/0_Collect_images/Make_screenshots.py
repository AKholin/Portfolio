from PIL import Image
import pyautogui as pag
from os import listdir, mkdir
from os.path import isfile, isdir, join, exists
import time
import math
import winsound


def photo_id():
    file = open('index.txt', 'r')
    current_id = int(file.readline())
    file.close()

    if current_id < 10:
        id = '00000' + str(current_id)
    elif current_id < 100:
        id = '0000' + str(current_id)
    elif current_id < 1000:
        id = '000' + str(current_id)
    elif current_id < 10000:
        id = '00' + str(current_id)
    elif current_id < 100000:
        id = '0' + str(current_id)
    elif current_id < 1000000:
        id = str(current_id)

    next_id = current_id + 1

    file = open('index.txt', 'w')
    file.write(str(next_id))
    file.close()
    return id

def next_name(directory):
    dir_folder_lst = [dir for dir in listdir(directory) if isdir(join(directory, dir))]
    last_name = dir_folder_lst[-1].split('_')
    ind = int(last_name[1]) + 1
    if ind < 10:
        next_name = last_name[0] + '_00' + str(ind)
    elif ind < 100:
        next_name = last_name[0] + '_0' + str(ind)
    else:
        next_name = last_name[0] + '_' + str(ind)
    return next_name

start = time.time()  # запускаем отсчёт времени
print("Start working")
winsound.Beep(432, 200)
# ==============================================

group_dir = 'C:/Python/Projects/Task/Group_photos'

folder_name = next_name(group_dir)
current_dir = join(group_dir, folder_name)
mkdir(current_dir)

print("Wait 1 sec to continue")
time.sleep(15)
start = time.time()  # запускаем отсчёт времени
print("Continue")
winsound.Beep(432, 200)

save_ind = 0

while save_ind < 800:
    shot = pag.screenshot()
    shot = shot.crop((200, 140, 616, 556))
    winsound.Beep(432, 200)
    time.sleep(0.4)
    shot.save('{0}/{1}.png'.format(current_dir, photo_id()))
    save_ind += 1

    print(save_ind)

end = time.time()
scan_time = end - start
minutes = math.floor(scan_time / 60)
seconds = math.floor(scan_time % 60)
print("Сбор объектов занял {0} минут и {1} секунд".format(minutes, seconds))
print("Затрачено {0} секунд".format(scan_time))
print("Finish")