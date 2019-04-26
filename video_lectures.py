import time
from utils.support import *


def download_video_lecture(driver, course_name, courses):
    driver.get(courses[course_name])
    xpath = '//*[@id="menu_pag_corso"]/li[5]/a'
    if material_exist(driver, xpath):
        url_material = driver.find_element_by_xpath(xpath).get_attribute('href')
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