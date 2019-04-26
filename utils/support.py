import requests
from clint.textui import progress
import os
import re
import shutil


def download_file(url, name_file):
    print('\n')
    r = requests.get(url, stream=True)
    with open(name_file, "wb") as Pymp4:

        total_length = int(r.headers.get('content-length'))
        print(name_file + '\t')
        for ch in progress.bar(r.iter_content(chunk_size=2391975), expected_size=(total_length / 1024) + 1):
            if ch:
                Pymp4.write(ch)


def classes_print(classes):
    i = 0
    for course in classes:
        if i > 0:
            print(str(i)+'. '+course)
        i += 1


def get_available_classes(driver):
    driver.get("https://didattica.polito.it/portal/page/portal/home/Studente")
    tbody = driver.find_element_by_xpath('//*[@id="portlet_container"]/div[2]/div/table/tbody')
    trs = tbody.find_elements_by_tag_name('a')
    classes = dict()
    i = 0
    for tr in trs:
        if i > 0:
            classes[tr.text.lower().strip()] = tr.get_attribute('href')
        i += 1
    return classes


def rename_if_space(file_text):
    if file_text.__contains__(' '):
        os.rename(file_text, file_text.replace(' ', '_'))


def get_start_index(name_course, start=1):
    # Check first if the folder exist
    if not os.path.isdir(name_course):
        os.mkdir(name_course.title())
        return start
    else:  # o.w. grab the maximun number
        pattern = re.compile(r'([0-9]{4}[_][a-zA-Z]+[_])(\d{2})\w*', re.IGNORECASE)
        list_names = os.listdir(name_course)
        max_str = max(list_names)
        m = re.match(pattern, max_str).group(2)
        if start > int(m):
            return start
        else:
            return int(m)


def material_exist(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath).get_attribute('href')
        return True
    except:
        print('Not available')
        return False


def rearrange_path(course_name, files_path, dest_path):
    new_dir = dest_path + '/' + course_name.replace(' ', '_') + '_Material'
    try:
        os.mkdir(new_dir)
    finally:
        for folder, files in files_path.items():
            sub_dir = new_dir + '/' + folder.title()
            os.mkdir(sub_dir)
            for file in files:
                idx = file.rfind('/') + 1
                try:
                    shutil.move(file, sub_dir + '/' + file[idx:])
                except:
                    name_file = file[idx:-4:]+' '+file[-3::]
                    shutil.move(file, sub_dir + '/' + name_file)
                    print(file + ' not found in download. It may have a different name')