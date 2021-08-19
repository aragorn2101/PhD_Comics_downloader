#!/usr/bin/env python3
#
#  Script to download comic strips from PhD <http://phdcomics.com/>
#  Version 2.1 -- Implemented using requests
#
#  Copyright (C) 2018  Nitish Ragoomundun, Mauritius
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# -----------------------------------------------------------------------------
#
#  Changelog:
#  2.0: 21.08.2018
#       * Initial script using requests instead of urllib.
#
#  2.1: 03.10.2018
#       * Added the creation of an empty file for undownloaded files, and
#         added the GNU Public License version 3.
#


import csv
import re
import requests
from pathlib import Path


###  BEGIN Preliminary setup  ###

#  Range of indices of the comic strips which have to be
#  downloaded.
startIdx = 2042
endIdx   = 2042

#  Base link of all the PhD Comics pages
BaseUrl = "http://phdcomics.com/comics/archive.php?comicid="

#  File containing dates and titles copied from
#  < http://phdcomics.com/comics/archive_list.php >
TitlesFile = "PhDComics_dates_titles.txt"

#  Log file for errors
LogFile = "Comics_" + str(startIdx) + "_-_" + str(endIdx) + ".log"

#  Anomalies: some comic strips are actually linked to
#  audio or video, and this causes errors in retrieving
#  the file. This is a list of their indices.
anomalies = [  191,  194,  574,  657, 1433, 1489, 1513, 1519, 1522, 1524,
              1526, 1529, 1533, 1535, 1538, 1542, 1547, 1549, 1552, 1556,
              1560, 1565, 1567, 1575, 1579, 1582, 1584, 1588, 1594, 1599,
              1605, 1616, 1622, 1628, 1635, 1639, 1643, 1649, 1657, 1663,
              1669, 1680, 1683, 1685, 1691, 1694, 1707, 1714, 1716, 1718,
              1726, 1748, 1766, 1769, 1770, 1777, 1788, 1805, 1845, 1853,
              1855, 1864, 1874, 1880, 1886, 1889, 1902, 1931, 1933, 1935,
              1939, 1949, 1954, 1959, 1964, 1985, 2009, 2025, 2033, 2041]


###  END Preliminary setup  ###


###  BEGIN Function to construct output filename  ###
def construct_filename(date, ComicIdx, title):
    #  Construct date string in yyyymmdd format
    tmp_date = date.split("/")
    str_date = tmp_date[2]

    if int(tmp_date[0]) < 10:
        str_date = str_date + "0" + tmp_date[0]
    else:
        str_date = str_date + tmp_date[0]

    if int(tmp_date[1]) < 10:
        str_date = str_date + "0" + tmp_date[1]
    else:
        str_date = str_date + tmp_date[1]

    #  Remove dot at the end if title sentence finishes with fullstop
    if title[-1] == '.' and title[-2] != '.':
        title = title[:-1]

    return (str_date + "_" + str(ComicIdx) + "_-_" + title + ".gif")

###  END Function to construct output filename  ###



###  Main program  ###

#  Open file containing dates and titles
try:
    f = open(TitlesFile, 'r')
except OSError:
    print("Cannot open {:s} !\n".format(TitlesFile))
    exit(2)

#  Loading dates and titles into arrays
date_list = []
title_list = []
for row in csv.reader(f, delimiter="\t"):
    # row[0] is a single whitespace
    date_list.append(row[1])

    # replace whitespaces in title and store
    title_list.append(row[2].replace(" ","_"))

f.close()


#  Verify if indices of comic strips are within valid ranges
try:
    if startIdx<=0 or endIdx<=0 or endIdx<startIdx:
        raise ValueError
except ValueError:
    print("startIdx = {:4d} and endIdx = {:4d} are not allowed.".format(startIdx, endIdx))
    exit(1)



#  Verifying if the number of dates and titles available are plausibly
#  numerous enough to name the number of comic strips to download
try:
    if len(date_list) < (endIdx - startIdx + 1):
        raise ValueError
except ValueError:
    print("There are {:d} items in the dates and titles list,".format(len(date_list)))
    print("while there are {:d} comic strips to fetch (indices {:d} to {:d}).".format(endIdx-startIdx+1, startIdx, endIdx))
    exit(1)



#  Creating log file
try:
    f = open(LogFile, 'w')
except OSError:
    print("Cannot create {:s} !\n".format(LogFile))
    exit(2)



###  BEGIN Loop through indices and retrieving comic strips ###
for ComicIdx in range(startIdx, endIdx+1):

    #  Veryfying if it is part of the anomaly group
    if ComicIdx in anomalies:
        f.write("--  Anomaly #{:d}  --\n".format(ComicIdx))
        print("--  Anomaly #{:d}  --".format(ComicIdx))

    print("Working on comic strip #{:d} ...".format(ComicIdx))

    ###  BEGIN Retrieving webpage  ###
    print("Retrieving page <{:s}> ...".format(BaseUrl + str(ComicIdx)))

    try:
        htmlPage = requests.get(BaseUrl + str(ComicIdx))
        htmlPage.raise_for_status()

    except ConnectionError:
        f.write("Connection error while retrieving page for comic strip #{:d}".format(ComicIdx))
        f.write("Will not continue due to this error. Please mend connection and re-launch script.")
        print("Connection error while retrieving page for comic strip #{:d}".format(ComicIdx))
        print("Will not continue due to this error. Please mend connection and re-launch script.")
        f.close()
        exit(3)

    except HTTPError:
        f.write("HTTP Error while retrieving page for comic strip #{:d}".format(ComicIdx))
        print("HTTP Error while retrieving page for comic strip #{:d}".format(ComicIdx))
        continue

    except Timeout:
        f.write("Time out error while working on comic strip #{:d}".format(ComicIdx))
        print("Time out error while working on comic strip #{:d}".format(ComicIdx))
        continue

    htmlSplit = (htmlPage.text).split('\n')

    ###  END Retrieving webpage  ###



    #  Retrieve image link
    for line in htmlSplit:
        if "id=comic name=comic src" in line:
            ImageUrl = re.search("(?P<url>https?://[^\s]+)", line).group("url")
            break

    print("Image link is <{:s}>".format(ImageUrl))

    # Construct filename for the comic strip
    ComicName = construct_filename(date_list[ComicIdx-1], ComicIdx, title_list[ComicIdx-1])


    ###  BEGIN Retrieve image file  ###
    if ImageUrl.endswith(".gif"):
        print("Retrieving image under the name {:s} ...".format(ComicName))

        try:
            ImageResp = requests.get(ImageUrl)
            ImageResp.raise_for_status()

        except ConnectionError:
            f.write("Connection error while retrieving image for comic strip #{:d}".format(ComicIdx))
            f.write("Will not continue due to this error. Please mend connection and re-launch script.")
            print("Connection error while retrieving image for comic strip #{:d}".format(ComicIdx))
            print("Will not continue due to this error. Please mend connection and re-launch script.")
            f.close()
            exit(3)

        except HTTPError:
            f.write("HTTPError while retrieving image for comic strip #{:d}".format(ComicIdx))
            print("HTTPError while retrieving image for comic strip #{:d}".format(ComicIdx))
            continue

        except Timeout:
            f.write("Time out error while retrieving image for comic strip #{:d}".format(ComicIdx))
            print("Time out error while retrieving image for comic strip #{:d}".format(ComicIdx))
            continue

        # If succeeded in retrieving an image
        with open(ComicName, 'wb') as ImageFile:
            for chunk in ImageResp.iter_content(chunk_size=128):
                ImageFile.write(chunk)
        ImageFile.close()

        #  Mention in log if it was an anomaly
        if ComicIdx in anomalies:
            f.write("Successfully retrieved <")
            f.write(ImageUrl)
            f.write(">\nunder the name {:s}.\n\n".format(ComicName))
        print()
        continue

    else:
        print("Image url does not link to image. Creating empty file {:s}.".format(ComicName[:-4]))
        print("Logging this issue and moving to next comic strip ...")
        print()
        f.write("Fail to complete work on comic strip #{:d}".format(ComicIdx))
        f.write(" ({:s}: {:s})\n".format(date_list[ComicIdx-1], title_list[ComicIdx-1]))
        f.write("Image url <")
        f.write(ImageUrl)
        f.write("> does not link to image.\n")
        f.write("Creating empty file {:s}.\n".format(ComicName[:-4]))
        f.write("Moving to the next comic strip ...\n\n")

        # Create an empty file with the comic strip name
        # without the .gif extension
        Path("{:s}".format(ComicName[:-4])).touch()

        continue

    ###  END Retrieve image file  ###

###  END Loop through indices and retrieving comic strips ###


#  Close log file
f.close()


exit(0)
