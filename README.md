# reDater

## Introduction

While cleaning up my photo archives, I noticed that I had quite a few files where the creation date had been set to various incorrect dates. As the images have come from a number of sources, the dates may have reflected when the were copied/moved into the archive. Who knows? I just wanted them to be correct.

I threw together this script to fix things and, full disclosure, it's not perfect as there were a few areas that I was unfamiliar with. The good news is that there is room for improvement (more to learn).

There are a number of possibilities when choosing the "correct" date. EXIF data has several options itself. ReDater will look for the "best" date first. If it does not find it, it will continue to work through the list.

The following is what reDater will look for, in order of highest priority first:

- Image DateTimeOriginal
- Image DateTimeDigitized
- Image DateTime
- EXIF DateTimeOriginal
- EXIF DateTimeDigitized
- GPS GPSDate (This is date _only_. GPSTime is available, but I did not feel it worth extra code for an edge case.)
- Modifed By Date (If the modified date is earlier than the created date, it is probably "more correct".)

## Instructions

Run the script as you would any python script. Pass the full path of the target root folder.

```bash
python reDater.py "C:\My Image Files\"
```

> *NOTE*: If you do not include a path, the script will still run using the current path as the root folder.

## Supporting Software

### Python Version(s)

This was written in *Python 3.8*. It has not be tested in any other version.

### Python Modules

This script requires the following modules to be installed:

- ExifRead
- pywin32

## Known Issues/Concerns

Please take note of the following!

- The script will recursively process every folder and file. I have not filtered out image files as the folders I needed to process contained _only_ image files.
