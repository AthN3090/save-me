# save-me
save-me is a command-line tool for saving your work files with just a single command through your terminal to common cloud space. Users are required to register for the application. Upon registration, users can upload, list and delete files on the common cloud space with specific terminal commands. The application uses python for command-line interface and the server code is written in Express. 
<br>
![front](/Screenshots/saveme-front.png)
<br>
[!help](/Screenshots/help.png)
# Installation
* clone the repository
```
git clone https://github.com/AthN3090/save-me
```
```
cd save-me
```
* setup
```
pip install .
```
# How to use

* User registeration 
```
saveme -r
```
![registeration](Screenshots/save-me-reg.gif)

* File upload
```
saveme [-u user] [-f filename]
```
![file-upload](/Screenshots/save-me-upload.gif)


* Download file
```
saveme [-u user] [-s filename]
```
![file-save](/Screenshots/saveme-save.gif)


* List files
```
saveme [-u user] -l
```
![file-list](/Screenshots/saveme-listfile.gif)

* Delete file
```
saveme [-u user] [-d filename]
```
![file-delete](/Screenshots/save-me-delete.gif)

* Delete all files
```
saveme [-u user] -da
```
![file-deleteall](/Screenshots/saveme-empty.gif)
