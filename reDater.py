#!/usr/bin/env python3.8

import exifread
import os
import sys
import time
from datetime import datetime
import platform
import pywintypes
import win32file
import win32con
from dateutil.parser import parser


showDetails = False
bestDateTag = 'Image DateTimeOriginal'
dateTags = ('Image DateTimeOriginal', 'Image DateTimeDigitized', 'Image DateTime',
            'EXIF DateTimeOriginal', 'EXIF DateTimeDigitized', 'GPS GPSDate',)


def getCreatedTimestamp(filePath):
    if platform.system() == 'Windows':
        return os.path.getctime(filePath)
    else:
        stat = os.stat(filePath)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


def getModifiedTimestamp(filePath):
    if platform.system() == 'Windows':
        return os.path.getmtime(filePath)
    else:
        stat = os.stat(filePath)
        return stat.st_mtime


def getBestEXIFDate(filePath):
    bestEXIFDate = ''
    binaryReadFile = open(filePath, 'rb')
    tags = exifread.process_file(
        binaryReadFile, details=showDetails, stop_tag=bestDateTag)

    for dateTag in dateTags:
        if dateTag in tags and tags[dateTag] != '':
            print("    Best date from {label}".format(label=dateTag))
            bestEXIFDate = tags[dateTag]
            break

    return bestEXIFDate


def getBestTimestamp(filePath):
    """
        Return a 'best guess' at what the correct file creation date should be.
        This may come from EXIF data or if the file's modification date is
        earlier than its creation date.

        Arguments:
            args {[type]} -- [description]

        Returns:
            [type] -- [description]
    """

    bestDate = ''
    bestTimestamp = None

    # Replace the 'best date' with what we can gleen from EXIF data
    bestDate = str(getBestEXIFDate(filePath))
    print('    Best Date: {bestDate}'.format(bestDate=bestDate))
    if bestDate != '':
        try:
            bestTimestamp = datetime.strptime(
                bestDate[0:19], '%Y:%m:%d %H:%M:%S').timestamp()
        except:
            print("[ERROR] Unable to convert from '{date}'".format(
                date=bestTimestamp))
    else:
        createdTimestamp = getCreatedTimestamp(filePath)
        modifiedTimestamp = getModifiedTimestamp(filePath)
        if modifiedTimestamp < createdTimestamp:
            bestTimestamp = modifiedTimestamp
            print("    Best data from file Last Modified Date")
        else:
            bestTimestamp = createdTimestamp
            print("    Best data from file Created Date")

    return bestTimestamp


def setCreationDate(filePath, newDate):
    if platform.system() == 'Windows':
        wintime = pywintypes.Time(int(newDate))
        winfile = win32file.CreateFile(
            filePath, win32con.GENERIC_WRITE,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
            None, win32con.OPEN_EXISTING,
            win32con.FILE_ATTRIBUTE_NORMAL, None)
        win32file.SetFileTime(winfile, wintime, None, None)
        winfile.close()
    else:
        os.utime(filePath, (newDate, newDate))


def main(args):
    filePath = ''
    try:
        filePath = sys.argv[1]
    except:
        filePath = '.'

    for root, dirs, files in os.walk(filePath, topdown=True):
        for filename in files:
            currentFile = os.path.join(root, filename)
            print('Processing: ' + currentFile)
            bestTimeStamp = getBestTimestamp(currentFile)
            if bestTimeStamp != None:
                setCreationDate(currentFile, bestTimeStamp)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
