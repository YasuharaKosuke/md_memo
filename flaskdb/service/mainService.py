from glob import glob
import pathlib
import os
from flask import session

def create_private_folder(username):
        current_dir = os.getcwd()
        mdfile = os.path.join(current_dir,'flaskdb', 'view', 'static', 'article')
        path = mdfile + '/' + username
        if os.path.exists(path):
            pass
        else:
            os.makedirs(path, exist_ok=True)
            img_path = path + '/' + 'img'
            os.makedirs(img_path, exist_ok=True)


def private_dir(username):
    current_dir = os.getcwd()
    mdfile = os.path.join(current_dir, 'flaskdb', 'view', 'static', 'article',  username)
    return mdfile

def private_image_dir(username):
    current_dir = os.getcwd()
    img = os.path.join(current_dir,'flaskdb', 'view', 'static', 'img',  username)
    return img


def file_name_list():
    mdfile_list = []
    username = session["username"]
    mdfile = private_dir(username)
    mdfiles = os.listdir(mdfile)
    for path in mdfiles:
        file = os.path.splitext(path)[0]
        mdfile_list.append(file)
    mdfiles_list = sorted(mdfile_list)
    return mdfiles_list
    

def private_file_rename(before_title, after_title):
    before_file = private_dir(session["username"]) + '/' + before_title + '.md'
    after_file = private_dir(session["username"]) + '/' + after_title + '.md' 
    os.rename(before_file, after_file)

def catch_img(username):
    img_path = private_image_dir(username)
    img_list = []
    for img in glob(img_path +  '/*'):
        img_name = os.path.basename(img)
        img_list.append('/static/img/'+ username + '/' + img_name)
    return ", ".join(img_list)
