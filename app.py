from configuration import *
from video_lectures import *

menu = {1: download_video_lecture, 2: download_material_wrapper}


def main():

    driver = init_driver()

    values = arg_parser()

    login(driver, values.user, values.psw)

    course_name = 'fisica ii' # select class name among your semester classes

    check = 1
    sel = 0
    while check:
        sel = input('Select '
                    '       \n1. download video lectures'
                    '       \n2. download course material\n')

        if sel.isdigit() and int(sel) <= max(menu.keys()):
            check = 0
        else:
            print('Insert numeric values in range ' + str(list(menu.keys())))

    menu[int(sel)](driver, course_name, int(values.start))

    driver.close()


if __name__ == '__main__':
    main()
