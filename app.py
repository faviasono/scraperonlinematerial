from utils.configuration import *
from video_lectures import *
from material import *


menu = {1: download_video_lecture, 2: download_material_wrapper}


def main():

    driver = init_driver()
    values = arg_parser()
    login(driver, values.user, values.psw)

    courses = get_available_classes(driver)
    classes_print(courses)

    # select among available classes
    while True:
        try:
            sel = int(input('Insert the number of the course: '))

            if sel == 0 or not sel <= len(courses.keys()) - 1:
                raise Exception
            break
        except:
            print('\nInsert numeric values lower than ' + str(len(courses.keys()) - 1) + '\n')

    # get the course name
    course_name = list(courses)[sel]

    # select among material or lectures download
    sel = 1
    while True:
        try:
            sel = int(input('Select '
                            '\n1. download video lectures'
                            '\n2. download course material\n'))

            if sel == 0 or not sel <= max(menu.keys()):
                raise Exception
            break
        except:
            print('Insert numeric values in range ' + str(list(menu.keys())) + '\n')

    # start the function selected
    menu[sel](driver, course_name, courses)

    driver.close()


if __name__ == '__main__':
    main()
