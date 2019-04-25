import requests
from clint.textui import progress

def download_file(url, name_file):
    print('\n')
    r = requests.get(url, stream=True)
    with open(name_file, "wb") as Pymp4:

        total_length = int(r.headers.get('content-length'))
        print(name_file + '\t')
        for ch in progress.bar(r.iter_content(chunk_size=2391975), expected_size=(total_length / 1024) + 1):
            if ch:
                Pymp4.write(ch)


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
