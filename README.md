# polito-material-downloader

My university, Politecnico di Torino, provides useful video lectures visible on the online platform. However, it is not possible to download them all together and watch them offline. You need to download each one after the other and I was tired of this procedure, and hence I have develop this program to download both course material (e.g. slides) and video lectures directly.

## Getting Started
To run this project you need to install these components on your machine:
* Python 3.7
* Google Chrome 74.x
* Selenium Webdriver library for chrome version 74.X

## Information
### headless chrome
It is possible to use _headless_ chrome only to download video lectures. However, since the program must interact with Javascript to downlaod material files (they don't have a visible url) we have to keep chrome in a window.
Feel free to uncomment the line below in the _configuration.py_ if you only  want to download video lectures with chrome in background.
```
# options.add_argument('headless') 
```
### Material downloader
The program will download all the course in the _Downloads_ directory of your os. After thast, it will create an hierarchical structure in the _Desktop_ folder. There should not be a folder called as _Name_Course_Material_ in Desktop, or the program will raise an exception.

## Usage
You must write in _course_name_ variable in **app.py** the name of the course in your semester curriculum. (in the code is selected _Fisica II / Physics II_ )
```
python3 app.py -u <username> -p <password>
```
## Task List
- [x] input course name & check if it exists
- [ ] headless chrome with material downloader 
- [ ] add screenshots
- [ ] considering new video lectures online platform for scraping & other courses name 

## Built With
* [Python 3](https://docs.python.org/3/)
