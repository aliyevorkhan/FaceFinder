# Face Finder

Face Finder is a face find application which is working on web.

## Required libraries

For use this application you must own or install these libraries : 

[face_recognition](https://github.com/ageitgey/face_recognition)

[Flask](https://pypi.org/project/Flask/)

[OpenCV](https://pypi.org/project/Flask/)

[numpy](https://pypi.org/project/numpy/)

[Pillow](https://pypi.org/project/Pillow/)


## Usage

```bash
flask run
```
Application run on your machine: **127.0.0.1:5000**

When you visit this address you will see output below:

![MainPage](outputs/1.png)

You can see two upload buttons for upload images. First button is using for upload searched image. Second is using for upload group image which is include or not include searched face. Also you can check uploaded image is right image or not from preview partition. When you upload images right you can click Find button:


![UploadedImages](outputs/2.png)

After process of recognition, application routing you to Result page. 


You can see matched face(s) and their similarity scores on image. Result page output displayed as below: 

![Results](outputs/3.png)

Additionally you can check previous results from Previous Results page. 

![PreviousResults](outputs/4.png)
