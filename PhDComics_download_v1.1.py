#!/usr/bin/env python3
#
#  Script to download comic strips from PhD Comics <http://phdcomics.com/>
#  Version 1.1 -- Implemented with urllib
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
#  1.0: 23.06.2018
#       * Initial script.
#
#  1.1: 29.09.2018
#       * Added the creation of an empty file for undownloaded files, and
#         added the GNU Public License version 3.
#


import csv
import re
from urllib import request as urlreq
from urllib import error as urlerror
from pathlib import Path


#  Range of indices of the comic strips which have to be
#  downloaded.
startIdx = 1
endIdx   = 2052

#  Base link of all the PhD Comics pages
BaseUrl = "http://phdcomics.com/comics/archive.php?comicid="

#  File containing dates and titles copied from
#  < http://phdcomics.com/comics/archive_list.php >
TitlesFile = "PhDComics_dates_titles.txt"

#  Log file for errors
LogFile = "Comics_" + str(startIdx) + "_-_" + str(endIdx) + ".log"

#  Anomalies: some comic strips are actually linked to
#  audio or video, sometimes YouTube video. This is a
#  list of their indices.
anomalies = [  191,  194,  574,  657, 1433, 1489, 1513, 1519, 1522, 1524,
              1526, 1529, 1533, 1535, 1538, 1542, 1547, 1549, 1552, 1556,
              1560, 1565, 1567, 1575, 1579, 1582, 1584, 1588, 1594, 1599,
              1605, 1616, 1622, 1628, 1635, 1639, 1643, 1649, 1657, 1663,
              1669, 1680, 1683, 1685, 1691, 1694, 1707, 1714, 1716, 1718,
              1726, 1748, 1766, 1769, 1770, 1777, 1788, 1805, 1845, 1853,
              1855, 1864, 1874, 1880, 1886, 1889, 1902, 1931, 1933, 1935,
              1939, 1949, 1954, 1959, 1964, 1985, 2009, 2025, 2033, 2041,
              2047, 2050, 2052]



###  Functions  ###
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



###  Main program  ###

#  Verify if indices of comic strips are within range
try:
    if startIdx<=0 or endIdx<=0 or endIdx<startIdx:
        raise ValueError
except ValueError:
    print("startIdx = {:4d} and endIdx = {:4d} are not allowed.".format(startIdx, endIdx))
    exit(1)



#  Open file containing dates and titles
try:
    f = open(TitlesFile, 'r')
except OSError:
    print("Cannot open {:s} !\n".format(TitlesFile))
    exit(2)

#  Storing dates and titles in arrays
date_list = []
title_list = []
for row in csv.reader(f, delimiter="\t"):
    # row[0] is a whitespace
    date_list.append(row[1])
    title_list.append(row[2].replace(" ","_"))

f.close()

#  Verifying if the number of dates and titles correspond
#  to the number of comic strips to download
try:
    if len(date_list) < (endIdx - startIdx + 1):
        raise ValueError
except ValueError:
    print("There are {:d} items in the dates and titles list,".format(len(date_list)))
    print("while there are only {:d} comic strips to fetch (indices {:d} to {:d}).".format(endIdx-startIdx+1, startIdx, endIdx))
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

    print("Retrieving page <{:s}> ...".format(BaseUrl + str(ComicIdx)))
    try:
        response = urlreq.urlopen(urlreq.Request(BaseUrl + str(ComicIdx)))
    except urlerror.URLError as Url_error:
        f.write(Url_error)
        f.write("\n")
        print(Url_error)
        f.write("Stopped at comic strip #{:d}".format(ComicIdx))
        f.write(" ({:s}: {:s}) ".format((date_list[ComicIdx-1], title_list[ComicIdx-1])))
        f.write("due to above error.\n\n")
        print("Stopped at comic strip #{:d} due to above error.".format(ComicIdx))
        exit(3)

    #  If success in retrieving page, then continue.
    #  Convert html code to bytearray, then string
    htmlBytes = response.read()
    try:
        htmlString = htmlBytes.decode("utf8")
    except UnicodeError:
        print("Could not convert html page corresponding to above url due to UnicodeError error.")
        print("Logging this issue and moving to next comic strip.")
        print()
        f.write("Fail to complete work on comic strip #{:d}".format(ComicIdx))
        f.write(" ({:s}: {:s}) ".format(date_list[ComicIdx-1], title_list[ComicIdx-1]))
        f.write("due to UnicodeError.\n")
        f.write("Could not convert html page corresponding to url:\n")
        f.write("<{:s}>\n\n".format(BaseUrl + str(ComicIdx)))
        continue

    htmlSplit = htmlString.split('\n')

    #  Retrieve image link
    for line in htmlSplit:
        if "id=comic name=comic src" in line:
            ImageUrl = re.search("(?P<url>https?://[^\s]+)", line).group("url")
            break

    print("Image link is <{:s}>".format(ImageUrl))

    # Construct filename for the comic strip
    ComicName = construct_filename(date_list[ComicIdx-1], ComicIdx, title_list[ComicIdx-1])


    #  Retrieve image
    if ImageUrl.endswith(".gif"):
        print("Retrieving image under the name {:s} ...".format(ComicName))
        urlreq.urlretrieve(ImageUrl, ComicName)
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
###  END Loop through indices and retrieving comic strips ###

exit(0)
