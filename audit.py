import os
import sys
import shutil
import pyexiv2
import re

import fix_print_encoding
import log

log.init("takeout-fix.log")


src = r"D:\GooglePhotoTakeout - 2012-12\Takeout"
dst = r"D:\GooglePhotosSorted"
dupes = r"D:\GooglePhotosDupes"


def getDatefromExif(f):
    datetime = ""
    datetime_original = ""

    image = pyexiv2.Image(f)
    try:
        exif = image.read_exif()
    except RuntimeError:
        raise ValueError("Exif library can't read this")

    if "Exif.Image.DateTime" in exif:
        datetime = exif["Exif.Image.DateTime"]
    if "Exif.Photo.DateTimeOriginal" in exif:
        datetime_original = exif["Exif.Photo.DateTimeOriginal"]

    if datetime_original:
        date, _ = datetime_original.split(" ")
        return date.split(":")

    if datetime:
        date, _ = datetime.split(" ")
        return date.split(":")  # y,m,d

    raise ValueError("No Exif date information.")


def getDateFromString(s):
    regex = re.compile(
        r".*(2007|2008|2009|2010|2011|2012|2013|2014|2015|2016|2017|2018|2019)[^0-9]?(\d\d)[^0-9]?(\d\d)"
    )
    result = regex.match(s)
    if result:
        return result.group(1), result.group(2), result.group(3)
    else:
        raise ValueError("No date found in string.")


def getDateFromFile(root, f):
    filename = os.path.join(root, f)
    try:
        return getDatefromExif(filename)  # Format is: "2014:02:08 09:52:31"
    except ValueError as e:
        log.info(f"{f}, {e}, Resorting to filename.")
    return getDateFromString(f)


def walk():
    for root, _, files in os.walk(src):
        for f in files:
            if f.endswith(".json"):
                log.info(f"removing {f}")

                os.remove(os.path.join(root, f))

            if not f.lower().endswith((".png", ".jpg", ".jpeg", "gif", "mp4")):
                log.warn(f"{f}  Unknown file type")
                continue

            try:
                y, m, d = getDateFromFile(root, f)
            except ValueError as e:
                log.warn(f"{f}, {e}, (File not processed)")
                continue

            # Make dst directory if necessary
            newDir = os.path.join(dst, y, f"{y}_{m}", f"{y}_{m}_{d}")
            if not os.path.exists(newDir):
                log.info(f"Creating directory {newDir}")
                os.makedirs(newDir, exist_ok=True)

            srcFileName = os.path.join(root, f)
            dstFileName = os.path.join(newDir, f)

            # Test if dest already exists.  keep the larger one.
            if os.path.exists(dstFileName):
                if os.path.getsize(srcFileName) < os.path.getsize(dstFileName):
                    log.info(f"{f}, File already exists (Keeping larger one): ")
                    dupeFileName = os.path.join(dupes, f)
                    shutil.move(srcFileName, dupeFileName)
                else:
                    shutil.move(srcFileName, dstFileName)
            else:
                shutil.move(srcFileName, dstFileName)


def testGetDateFromString():
    for i in [
        "2017_12_05_17_27_28.jpg",
        "Screenshot_20180409-130824.png",
        "00005IMG_00005_BURST20180707151029.jpg",
        "craxy.jpg",
    ]:
        y, m, d = getDateFromString(i)
        print(f"{y}:{m}:{d}")


if __name__ == "__main__":
    walk()
    # testGetDateFromString()

