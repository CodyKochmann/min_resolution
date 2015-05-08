#!/usr/bin/env python

minimum={
    "width":raw_input("Enter the minimum pixel width:"),
    "height":raw_input("Enter the minimum pixel height:")
}

try:
    minimum["width"]=int(minimum["width"])
    minimum["height"]=int(minimum["height"])
except:
    print("invalid minimums")
    exit()

def script_path(include_name=False):
    # returns the full path of the script containing this snippet
    # by: Cody Kochmann
    from os import path
    full_path = path.realpath(__file__)
    if include_name:
        return(full_path)
    else:
        full_path = "/".join( full_path.split("/")[0:-1] ) + "/"
        return(full_path)

script_dir = script_path()

def ensure_dir(dir_name,parent_dir,verbose=False): 
    # ensures there is a directory of that name in that path
    # by: Cody Kochmann
    # ex: trash_dir=ensure_dir("trash", script_dir)
    def v_log(s):
        if(verbose):
            print(s)
    from os import listdir, path, mkdir
    dir_name=dir_name.replace("/", "")
    if parent_dir[-1] != "/":
        parent_dir+="/"
    new_dir = parent_dir+dir_name
    v_log(new_dir)
    if path.isdir(new_dir) == False:
        mkdir(new_dir)
    else:
        v_log("%s already exists" % (dir_name))
    return(new_dir+"/")

workzone_dir=ensure_dir("workzone", script_dir)

def get_image_resolution(img_path):
    # returns a tuple containing an images width and height in pixels
    # requires: PIL library
    # snippet by: Cody Kochmann
	from PIL import Image
	return(Image.open(img_path).size)

from os import listdir
photos = listdir(workzone_dir)


trash_dir=ensure_dir("trash", script_dir)

def send_to_trash(item):
    from os import rename
    t=item.replace("workzone","trash")
    rename(item, t)
    print (item.split("/")[-1]+" moved to "+t)

image_types="tiff png jpeg jpg TIFF PNG JPEG JPG".split(" ")
trash_list = []
for photo in photos:
    try:
        if photo.split(".")[-1] in image_types:
            photo = workzone_dir+photo
            print("checking: "+photo)
            if get_image_resolution(photo)[0] < minimum["width"] or get_image_resolution(photo)[1] < minimum["height"]:
                print("Throwing away"+str(get_image_resolution(photo))+": "+photo)
                trash_list.append(photo)
    except:
        if photo.split(".")[-1] in image_types: # this snippet handles corrupt photos
            trash_list.append(photo)
        pass

print "\n".join(trash_list)
if len(trash_list) > 0:
    #if raw_input("Found %s files to delete. Do I have permission? (y/n)\n" % (len(trash_list))) is "y":
    for i in trash_list:
        send_to_trash(i)
else:
    print("All photos met the minimum requirements.")
