from PIL import Image
from os import listdir
from os.path import isfile, isdir, join
import pickle
import time
import math

start_work = time.time()
# ==============================================

# ----------------------------------------------
#            ***  DIRECTORY  ***
base_dir = '/Python/Tasks/Task/Objects'
need_class = 16
out_dir = '/Python/Tasks/Task/Objects/Out_class'
objects_dir = '/Python/Tasks/Task/Objects'
# ==============================================

def seconds_to_m_s(seconds):
    minutes = math.floor(seconds // 60)
    seconds = math.ceil(seconds % 60)
    return minutes, seconds

dictionaries = [f for f in listdir(objects_dir) if isfile(join(objects_dir, f))]

file = open(join(objects_dir, dictionaries[-1]), 'rb')
labels_dict = pickle.load(file)
file.close()

folder_list = [dir for dir in listdir(base_dir) if isdir(join(base_dir, dir))]

if '16_HAVOC_g' in folder_list:
    index = folder_list.index('16_HAVOC_g')
    del folder_list[index]

if '16_HAVOC_s' in folder_list:
    index = folder_list.index('16_HAVOC_s')
    del folder_list[index]

if 'ZV_QUANTITY' in folder_list:
    index = folder_list.index('ZV_QUANTITY')
    del folder_list[index]

if '!_Allready' in folder_list:
    index = folder_list.index('!_Allready')
    del folder_list[index]

if 'Basic_stend' in folder_list:
    index = folder_list.index('Basic_stend')
    del folder_list[index]

if 'Delete_check' in folder_list:
    index = folder_list.index('Delete_check')
    del folder_list[index]

if 'Large_stend' in folder_list:
    index = folder_list.index('Large_stend')
    del folder_list[index]

if 'Out_class' in folder_list:
    index = folder_list.index('Out_class')
    del folder_list[index]

if '00_All' in folder_list:
    index = folder_list.index('00_All')
    del folder_list[index]

if 'ZW_DELETED' in folder_list:
    index = folder_list.index('ZW_DELETED')
    del folder_list[index]

if 'ZX_MERGER' in folder_list:
    index = folder_list.index('ZX_MERGER')
    del folder_list[index]

if 'ZY_NEAR' in folder_list:
    index = folder_list.index('ZY_NEAR')
    del folder_list[index]

if 'ZZ_EXTRA' in folder_list:
    index = folder_list.index('ZZ_EXTRA')
    del folder_list[index]

for current_folder in folder_list:
    current_dir = join(base_dir, current_folder)

    current_img_list = [f for f in listdir(current_dir) if isfile(join(current_dir, f))]

    for img_name in current_img_list:
        if img_name in labels_dict:
            objects = labels_dict[img_name]

            for nclass, coordinates in objects:
                if nclass == need_class:
                    img = Image.open(join(current_dir, img_name))
                    img.save(join(out_dir, img_name))
                    break

end_work = time.time()
work_time = seconds_to_m_s(end_work - start_work)
print("\nAll work took {} minutes {} seconds".format(work_time[0], work_time[1]))