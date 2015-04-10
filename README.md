Poom-Poom
=========

Open document files from your linux file explorer in the free Microsoft Office Online version on your browser.

## Why?
I know Microsoft is Evil, but no matter what you can't deny one of their best creations, and that is Microsoft Office.
With the free online version we can now use it on linux as well. And who are we kidding, Open Office or Libre Office 
are not even close to the online free version of Microsoft Office. So this is why I set out on this mission, primarily 
to satisfy my own needs :)

## How?
This is primarily a Dropbox app and acts as a Dropbox client. The app doesn't have any permission over your existing
Dropbox files. So when you open a document with the app it first uploads the file to its own directory on your 
Dropbox and then open the file from there using the Microsoft Office online edition.

## With What?
-	Python 2.7.8
-	The superb [Dropbox API](https://www.dropbox.com/developers/core/docs/python) for python.

-----------------------------------------------------------------------------------------

## Installation
For system installation using pip

```bash
sudo pip install poom_poom
```

For installing from github source

```bash
git clone https://github.com/redmoses/poom-poom.git
cd poom-poom
python setup.py install
```

## Usage
After installing the app, use the following command to open document files

```bash
poom-poom /path/to/office/document
```
