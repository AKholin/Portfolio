import math
import pickle
import sys
import time
from os import listdir
from os.path import isfile, isdir, join

import matplotlib.pyplot as plt

start = time.time()
# ==============================================

# ----------------------------------------------
#            ***  DIRECTORY  ***
objects_dir = '/Python/Tasks/Task/Objects'
# ==============================================

# ----------------------------------------------
#               ***  GLOBAL  ***
m1a2 = 0
lav25 = 0
m6bradly = 0
hammer = 0
faav = 0
ah1z = 0
uh60 = 0

typ98 = 0
wz551 = 0
typ95 = 0
nanji = 0
parat = 0
z10 = 0
z8 = 0

t90 = 0
btr90 = 0
tungs = 0
vodnk = 0
boat = 0
havoc = 0
mi17 = 0

total_images = 0
total_objects = 0
# ==============================================

# ----------------------------------------------
#               ***  FUNCTIONS  ***
def counting_objects(nclass):
    global m1a2
    global lav25
    global m6bradly
    global hammer
    global faav
    global ah1z
    global uh60

    global typ98
    global wz551
    global typ95
    global nanji
    global parat
    global z10
    global z8

    global t90
    global btr90
    global tungs
    global vodnk
    global boat
    global havoc
    global mi17

    if nclass == 0:
        m1a2 += 1
    elif nclass == 1:
        typ98 += 1
    elif nclass == 2:
        t90 += 1
    elif nclass == 3:
        lav25 += 1
    elif nclass == 4:
        wz551 += 1
    elif nclass == 5:
        btr90 += 1
    elif nclass == 6:
        m6bradly += 1
    elif nclass == 7:
        typ95 += 1
    elif nclass == 8:
        tungs += 1
    elif nclass == 9:
        hammer += 1
    elif nclass == 10:
        nanji += 1
    elif nclass == 11:
        vodnk += 1
    elif nclass == 12:
        faav += 1
    elif nclass == 13:
        parat += 1
    elif nclass == 14:
        ah1z += 1
    elif nclass == 15:
        z10 += 1
    elif nclass == 16:
        havoc += 1
    elif nclass == 17:
        uh60 += 1
    elif nclass == 18:
        z8 += 1
    elif nclass == 19:
        mi17 += 1
    elif nclass == 20:
        boat += 1
    else:
        print('!!!  Somthing went wrong  !!!')

def seconds_to_m_s(seconds):
    minutes = math.floor(seconds // 60)
    seconds = math.ceil(seconds % 60)
    return minutes, seconds

def next_name_quantity(current):
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
# ==============================================

# ----------------------------------------------
#       ***  OPEN and PREPARE DATA  ***
dictionaries = [f for f in listdir(objects_dir) if isfile(join(objects_dir, f))]

if '!' not in dictionaries[-1]:
    print('There are no data dictionary in this folder')
    sys.exit()

file = open(join(objects_dir, dictionaries[-1]), 'rb')
labels_dict = pickle.load(file)
file.close()
# ==============================================

# ----------------------------------------------
#          ***  LIST OF FOLDERS  ***
folder_list = [dir for dir in listdir(objects_dir) if isdir(join(objects_dir, dir))]

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

if 'ZV_QUANTITY' in folder_list:
    index = folder_list.index('ZV_QUANTITY')
    del folder_list[index]

if 'Out_class' in folder_list:
    index = folder_list.index('Out_class')
    del folder_list[index]
# ==============================================

# ----------------------------------------------
#          ***  COUNTING OBJECTS  ***
for name_dir in folder_list:
    current_dir = join(objects_dir, name_dir)
    folder_files = [f for f in listdir(current_dir) if isfile(join(current_dir, f))]

    name_dir_str = ' '.join(name_dir.split('_'))

    total_images = total_images + len(folder_files)

    print('{}: {}'.format(name_dir_str, len(folder_files)))

    for img_name in folder_files:
        objects = labels_dict[img_name]

        for nclass, box in objects:
            counting_objects(nclass)
# ==============================================

# ----------------------------------------------
#          ***  INFORMATION  ***
print('\n------------------------------')
print('How many objects we have now')
print('\nM1A2:', m1a2)
print('TYPE 98:', typ98)
print('T90:', t90)
print('LAV25:', lav25)
print('WZ551:', wz551)
print('BTR90:', btr90)
print('M6 BRADLY:', m6bradly)
print('TYPE 95:', typ95)
print('TUNGUSKA:', tungs)
print('HMMWV:', hammer)
print('NANJING:', nanji)
print('VODNIK:', vodnk)
print('FAAV:', faav)
print('PARATROOPER:', parat)
print('AH1Z:', ah1z)
print('Z10:', z10)
print('HAVOC:', havoc)
print('UH60:', uh60)
print('Z8:', z8)
print('MI17:', mi17)
print('BOAT:', boat)

print('\n------------------------------')
print('How many objects we need to collect')
print('\nM1A2:   {0:3d}  {1:3d}'.format( m1a2, 168+800-m1a2))
print('TYPE98: {0:3d}  {1:3d}'.format( typ98, 168+800-typ98))
print('T90:    {0:3d}  {1:3d}'.format( t90, 168+800-t90))
print('LAV25:  {0:3d}  {1:3d}'.format( lav25, 168+800-lav25))
print('WZ551:  {0:3d}  {1:3d}'.format( wz551, 168+800-wz551))
print('BTR90:  {0:3d}  {1:3d}'.format( btr90, 168+800-btr90))
print('M6BR:   {0:3d}  {1:3d}'.format( m6bradly, 168+800-m6bradly))
print('TYPE95: {0:3d}  {1:3d}'.format( typ95, 168+800-typ95))
print('TUNGUS: {0:3d}  {1:3d}'.format( tungs, 168+800-tungs))
print('HMMWV:  {0:3d}  {1:3d}'.format( hammer, 72+800-hammer))
print('NANJIN: {0:3d}  {1:3d}'.format( nanji, 72+800-nanji))
print('VODNIK: {0:3d}  {1:3d}'.format( vodnk, 72+800-vodnk))
print('FAAV:   {0:3d}  {1:3d}'.format( faav, 72+800-faav))
print('PARATR: {0:3d}  {1:3d}'.format( parat, 72+800-parat))
print('AH1Z:   {0:3d}  {1:3d}'.format( ah1z, 120+800-ah1z))
print('Z10:    {0:3d}  {1:3d}'.format( z10, 120+800-z10))
print('HAVOC:  {0:3d}  {1:3d}'.format( havoc, 120+800-havoc))
print('UH60:   {0:3d}  {1:3d}'.format( uh60, 120+800-uh60))
print('Z8:     {0:3d}  {1:3d}'.format( z8, 120+800-z8))
print('MI17:   {0:3d}  {1:3d}'.format( mi17, 120+800-mi17))
print('BOAT:   {0:3d}  {1:3d}'.format( boat, 172+800-boat))

total_objects = m1a2 + lav25 + m6bradly + hammer + faav + ah1z + uh60 + typ98 + wz551 + typ95 + nanji + parat + z10 + z8 + t90 + btr90 + tungs + vodnk + boat + havoc + mi17
print('\n------------------------------')
print('\nTotal images:', total_images)
print('Total objects:', total_objects)
print('Average objects in one image: {0:.3f}\n'.format(total_objects/total_images))
# ==============================================

class_list = [('M1A2', m1a2), ('TYPE 98', typ98), ('T90', t90), ('LAV25', lav25), ('WZ551', wz551), ('BTR90', btr90), ('M6 BRADLY', m6bradly), ('TYPE 95', typ95), ('TUNGUSKA', tungs), ('HMMWV', hammer), ('NANJING', nanji), ('VODNIK', vodnk), ('FAAV', faav), ('PARATROOPER', parat), ('AH1Z', ah1z), ('Z10', z10), ('HAVOC', havoc), ('UH60', uh60), ('Z8', z8), ('MI17', mi17), ('BOAT', boat)]

class_list.sort(key=lambda object: object[1])
for object in class_list:
    print(*object)

class_list_y = [m1a2, typ98, lav25, wz551, btr90, m6bradly, typ95, tungs, hammer, nanji, vodnk, faav, parat, ah1z, z10, havoc, uh60, z8, mi17, boat]

x_range = list(range(len(class_list_y)))

quantity_dir = join(objects_dir, 'ZV_QUANTITY')
quantity_lists = [f for f in listdir(quantity_dir) if isfile(join(quantity_dir, f))]
current_name = quantity_lists[-1]
next_quantity = next_name_quantity(current_name)

file = open(join(quantity_dir, quantity_lists[-1]), 'rb')
prev_class_list = pickle.load(file)
file.close()

file = open(join(quantity_dir, 'quantity_{}.p'.format(next_quantity)), 'wb')
pickle.dump(class_list_y, file)
file.close()

#prev_class_list = class_list_y[::-1]

plt.plot(x_range, class_list_y, '-')
plt.plot(x_range, prev_class_list, '--')
plt.show()

print('\n')
for object in class_list:
    print(*object)

end_work = time.time()
work_time = seconds_to_m_s(end_work - start)
print("\nAll work took {} minutes {} seconds".format(work_time[0], work_time[1]))