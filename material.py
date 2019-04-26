import time
from utils.support import *


def download_material_wrapper(driver, course_name, courses):
    files_path = download_course_material(driver, course_name, courses)
    if not files_path:
        print('Any material available')
    else:
        print('Download completed. Rearranging files in the destination folder')
        dwn_path = os.path.expanduser("~/Desktop")  # move files in Desktop folder ( modifiable)
        rearrange_path(course_name, files_path, dwn_path)


def download_course_material(driver, course_name, courses):
    files_path = {}
    driver.get(courses[course_name])
    xpath = '//*[@id="menu_pag_corso"]/li[5]/a'

    if material_exist(driver, xpath):
        url_material = driver.find_element_by_xpath(xpath).get_attribute('href')

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
                file_text = max([os.path.join(os.getenv('HOME') + '/Downloads', d) for d in os.listdir(os.getenv('HOME') +'/Downloads')], key=os.path.getmtime)  # get the latest file downloaded ( they may have a different name from html value)
                rename_if_space(file_text)
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
                    rename_if_space(file_text)
                    files_path[folder_name].append(file_text.replace(' ', '_'))

                # click the back button & wait js
                back_button = driver.find_element_by_xpath('//*[@id="portlet_corso_container"]/div/div/div[2]/div/div[2]/angular-filemanager/div/div[2]/div/div[1]/ul/li/a')
                time.sleep(2)
                back_button.click()
                time.sleep(4)
                i += 1

    return files_path

