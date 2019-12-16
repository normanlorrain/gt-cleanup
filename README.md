# gt-cleanup
Restructure the photos from Google Takeout into a folder structure, removing duplicates and extra files.
Files are structured as follows

      {destination directory}/{year}/{year}_{month}/{year}_{month}_{day}



After that, you can process the files further, looking for duplicates with your library, etc.



# Random notes


TODO: dedect duplicate files as in https://github.com/adrianlopezroche/fdupes


Tag (hex)	Tag (dec)	IFD	Key	Type	Tag description
0x0132	306	Image	Exif.Image.DateTime	Ascii	The date and time of image creation. In Exif standard, it is the date and time the file was changed.

0x9003	36867	Photo	Exif.Photo.DateTimeOriginal	Ascii	The date and time when the original image data was generated. For a digital still camera the date and time the picture was taken are recorded.



# MVIMG files

https://android.jlelse.eu/working-with-motion-photos-da0aa49b50c
https://www.bitquabit.com/post/moving-and-backing-up-google-moving-images/



# json files
example content:
    {
    "title": "IMG_20150728_203925.jpg",
    "description": "",
    "imageViews": "0",
    "creationTime": {
        "timestamp": "1438139564",
        "formatted": "29 Jul 2015, 03:12:44 UTC"
    },
    "modificationTime": {
        "timestamp": "1566513771",
        "formatted": "22 Aug 2019, 22:42:51 UTC"
    },
    "geoData": {
        "latitude": 0.0,
        "longitude": 0.0,
        "altitude": 0.0,
        "latitudeSpan": 0.0,
        "longitudeSpan": 0.0
    },
    "geoDataExif": {
        "latitude": 0.0,
        "longitude": 0.0,
        "altitude": 0.0,
        "latitudeSpan": 0.0,
        "longitudeSpan": 0.0
    },
    "photoTakenTime": {
        "timestamp": "1438137567",
        "formatted": "29 Jul 2015, 02:39:27 UTC"
    }
    }

this file had an exif timestamp: 2015:07:28 20:39:27, matching photoTakenTime




Files with "(1)" seem to be resized to fit on the screen of the phone (confirm?).  These are deleted.
