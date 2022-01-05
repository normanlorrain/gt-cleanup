import os
import sys
import shutil
import re
import pyexiv2
import filetype

import log

log.init("gt-cleanup.log")


# Change accordingly: (TODO: command-line arguments...)
safe = True

src = r"D:\takeout_2021"
# src = root+ r"\Google Photos"
dst = src + r".Sorted"
dupes = src + r".Dupes"


def rm(filename):
    if safe:
        log.info(f"Removing {filename}")
        os.remove(filename)
    else:
        log.info(f"Would remove {filename}")


def mkdir(pathname):
    if safe:
        os.makedirs(pathname, exist_ok=True)


def mv(src, dst):
    if safe:
        log.info(f"Moving {src} to {dst}")
        shutil.move(src, dst)
    else:
        log.info(f"Would move {src} to {dst}")


def getDatefromExif(f):
    datetime = ""
    datetime_original = ""

    try:
        image = pyexiv2.Image(f)
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
        r".*\D(2007|2008|2009|2010|2011|2012|2013|2014|2015|2016|2017|2018|2019|2020|2021)[^0-9]?(\d\d)[^0-9]?(\d\d)"
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
        log.info(f"{root}\{f}:  {e}, Resorting to filename.")
    return getDateFromString(f)


def fixExtension(root, f):
    absFile = os.path.join(root, f)
    expectedExtension = filetype.guess_extension(absFile)
    if f.endswith != expectedExtension:
        os.rename(absFile, absFile + "." + expectedExtension)


def walk():
    for root, dirs, files in os.walk(src):
        log.info(f"In {root}")
        for f in files:
            if f.endswith(".json") or f.endswith(
                ".MP"
            ):  # We don't need the Json metadata, and MP files are those gimmicky short videos taken with a photo.
                log.info(f"removing {f}")
                rm(os.path.join(root, f))
                continue

            if not f.lower().endswith((".png", ".jpg", ".jpeg", "gif", "mp4")):
                log.warning(f"{f}  Unknown file type")
                continue

            if "(1)" in f:
                log.info(
                    f"skipping {f} (Google generated, lower res version, or Quicktime mov file)"
                )
                fixExtension(root, f)

                continue

            try:
                y, m, d = getDateFromFile(root, f)
            except ValueError as e:
                log.warning(f"{f}, {e}, (File not processed)")
                continue

            # Make dst directory if necessary
            newDir = os.path.join(dst, y, f"{y}-{m}", f"{y}-{m}-{d}")
            if not os.path.exists(newDir):
                log.info(f"Creating directory {newDir}")
                mkdir(newDir)

            srcFileName = os.path.join(root, f)
            dstFileName = os.path.join(newDir, f)

            # Test if dest already exists.  keep the larger one.
            if os.path.exists(dstFileName):
                if os.path.getsize(srcFileName) < os.path.getsize(dstFileName):
                    log.info(f"{f}, File already exists (Keeping larger one): ")
                    dupeFileName = os.path.join(dupes, f)
                    mv(srcFileName, dupeFileName)
                else:
                    mv(srcFileName, dstFileName)
            else:
                mv(srcFileName, dstFileName)


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
    mkdir(dst)
    mkdir(dupes)
    walk()
    # testGetDateFromString()
