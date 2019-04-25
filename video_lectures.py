import os
import re
import time
import shutil
from utils.utils import download_file, get_available_classes


def rearrage_path(course_name, files_path, dest_path):
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


def download_material_wrapper(driver,course_name):
    files_path = download_course_material(driver,course_name)
    if not files_path:
        print('Any material available')
    else:
        print('Download completed. Rearranging files in the destination folder')
        dwn_path = os.path.expanduser("~/Desktop")  # move files in Desktop folder ( modifiable)
        rearrage_path(course_name, files_path, dwn_path)


def download_course_material(driver, course_name):
    files_path = {}

    driver.get("https://didattica.polito.it/portal/page/portal/home/Studente")
    classes = get_available_classes(driver)
    driver.get(classes[course_name])
    url_material = driver.find_element_by_xpath('//*[@id="menu_pag_corso"]/li[5]/a').get_attribute('href')
    driver.get(url_material)

    time.sleep(2)

    elements_l = driver.find_elements_by_css_selector('.item-list a .ng-binding')
    values_l = list()
    [values_l.append(ele) for ele in elements_l if ele.text]
    size = len(values_l)

    if not values_l:  # if the list is empty(hence no material available)
        return files_path

    i = 0
    files_path['default'] = list()

    while i < size:
        # get folder name
        elements = driver.find_elements_by_css_selector('.item-list a .ng-binding')
        values = list()
        [values.append(ele) for ele in elements if ele.text]
        folder_name = values[i].text
        time.sleep(3)

        print('Downloading material...')
        if values[i].text.find('.') > 0:
            values[i].click()
            time.sleep(3)
            file_text = max([os.path.join(os.getenv('HOME') + '/Downloads', d) for d in os.listdir(os.getenv('HOME') +'/Downloads')],key=os.path.getmtime)  # get the latest file downloaded ( they may have a different name from html value)
            files_path['default'].append(file_text.replace(' ', '_'))
            i += 1
        else:
            files_path[folder_name] = list()
            # open the page
            values[i].click()
            time.sleep(3)
            # select & download files
            files = driver.find_elements_by_css_selector('.text-warning')
            files = files[1::2]  # multiple items selected

            for file in files:
                file.click()
                time.sleep(3)
                file_text = max([os.path.join(os.getenv('HOME') + '/Downloads', d) for d in
                                 os.listdir(os.getenv('HOME') + '/Downloads')], key=os.path.getmtime) #get the latest file downloaded ( they may have a different name from html value)
                files_path[folder_name].append(file_text.replace(' ', '_'))

            # click the back button & wait js
            back_button = driver.find_element_by_xpath('//*[@id="portlet_corso_container"]/div/div/div[2]/div/div[2]/angular-filemanager/div/div[2]/div/div[1]/ul/li/a')
            time.sleep(2)
            back_button.click()
            time.sleep(4)
            i += 1

    return files_path


def download_video_lecture(driver, course_name):

    driver.get("https://didattica.polito.it/portal/page/portal/home/Studente")
    classes = get_available_classes(driver)
    driver.get(classes[course_name])
    url_material = driver.find_element_by_xpath('//*[@id="menu_pag_corso"]/li[5]/a').get_attribute('href')
    driver.get(url_material)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="portlet_corso_container"]/div/div/div[2]/div/div[2]/angular-filemanager/div/div[2]/div/div[1]/ul/li/ul/li[2]/a').click()
    time.sleep(2)

    name_course = driver \
        .find_element_by_xpath('/html/body/div[3]/div/div[2]/div[1]/div/div[1]') \
        .text.replace(' ', '_')

    # I need to create a list to overcome Stale Exception
    lesson_list = driver.find_element_by_id('lessonList')
    elements = lesson_list.find_elements_by_class_name('h5')
    len_list = len(elements)


    while True:
        try:
            start = int(input('Insert the video lecture you want to start from [1 default]'))
            if start == 0:
                raise Exception
            break
        except:
            print("That's not a valid option!")

    i = get_start_index(name_course, start - 1)

    while i < len_list:
        # reconnect DOM every time
        lesson_list = driver.find_element_by_id('lessonList').find_elements_by_class_name('h5')
        list_el = list(lesson_list)
        # For each value I can navigate in another page
        anchor = list_el[i].find_element_by_tag_name('a')
        # get_name video lesson
        text = anchor.text.replace(' ', '_') + '.mp4'
        video_page = anchor.get_attribute('href')
        # move to the downloading page where is possible to find the link of the video to download
        driver.get(''.join(video_page))
        video = driver.find_element_by_tag_name('video').find_element_by_tag_name('source')
        src = video.get_attribute('src')

        download_file(src, name_course + '/' + text)
        i = i + 1
        # go back to the page
        driver.back()


def get_start_index(name_course, start):
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

