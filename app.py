from utils.configuration import *
from video_lectures import *
from utils import *

menu = {1: download_video_lecture, 2: download_material_wrapper}


def main():

    driver = init_driver()

    values = arg_parser()

    login(driver, values.user, values.psw)

    courses = get_available_classes(driver)
    print_classes(courses)

    course_name = 'fisica ii' # select class name among your semester classes

    sel = 0
    while True:
        try:
            sel = int(input('Select '
                        '       \n1. download video lectures'
                        '       \n2. download course material\n'))

            if sel == 0 or not sel <= max(menu.keys()) :
                raise Exception
            break
        except:
            print('Insert numeric values in range ' + str(list(menu.keys()))+'\n')

    menu[sel](driver, course_name)

    driver.close()


if __name__ == '__main__':
    main()
