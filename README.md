# PhD Comics downloader (Piled Higher and Deeper)

Being a PhD student myself, PhD Comics is a part of my everyday life. It gives
me confidence in times of doubt and it often reminds me how important my small
"steps" are for research and science in general.

So many thanks to Jorge Cham (the author), and please check out
[http://phdcomics.com](http://phdcomics.com)

This repository contains a Python 3 script which aims at the bulk download of
the comic strips. For those who are familiar with PhD Comics, writing this
Python script was a great pleasure as it was a very enjoyable way to
procrastinate.

The script has only been tested successfully on Linux distributions, as it has
been developed on one of them. So, Windows users out there, if you find a way
to make it work, just create an issue here and tell us how to make it work.



## Requirements

The script makes use of the usual python classes such as csv, re and pathlib.
Apart from these, it uses the **requests** library. I have seen some systems
without a default installation of **requests** in their Python 3 installation.
For example, I use Slackware GNU/Linux and had to install **requests**  from
[SlackBuilds.org](https://slackbuilds.org/). On Fedora, it can be installed
using dnf with the following:
```
# dnf install python3-requests
```
On Debian as well, it is called python3-requests. I'm not a Debian user, but I
guess it should be something like
```
# apt-get install python3-requests
```



## How the script works

Firstly, there are two versions of the script because, initially, I tried using
**urllib**, which is generally a default library in Python. However, things
didn't work out beautifully, as for some webpages there were errors due to
unicode conversion. So, version 2 was based on **requests** instead, and it is
much much better. Version 2 is also better developed than version 1, and
includes more features and stuff. I left version 1 here just as an example of
an implementation making use of **urllib**, for anyone out there experimenting
with such things. *So, please use version 2*.

For everything to work, we need two files:
* **PhDComics_download_v2.x.py** : executable Python 3 script,
* **PhDComics_dates_titles.txt** : plain text file containing the dates and
  titles of every comic strip and is used by the download script to name the
  comic strips.

The dates and titles file is easily created by copying the list at
[http://phdcomics.com/comics/archive_list.php](http://phdcomics.com/comics/archive_list.php).
There's a small space in front of every date and it is left as is for easier
bulk copying. A PhDComics_dates_titles.txt file is already found in the repo
and I will try to keep it up-to-date.

The script also needs a start index and end index. *All* the comics strips do
not necessarily have to be downloaded at once. The script will download the
comic strips corresponding to the range **startIdx** -- **endIdx** inclusively.
The script needs to be edited and the variables **startIdx** and **endIdx**
initialised. A small trick to know which comics you need to download is to look
at their addresses. The index is the number at the end, just after the equal
sign.  e.g.  http://phdcomics.com/comics/archive.php?comicid=1124

When everything is set, the script is just executed:
```
$ ./PhDComics_download_v2.x.py
  if the script is executable, OR:
$ python3 PhDComics_download_v2.x.py
```

One very useful feature of the script is that it will write a log report about
the whole process. The log file is named **Comics_[startIdx]_-_[endIdx].log**. It
will contain messages about every issue encountered while trying to download
the comic strips. There will be issues because some of the comic strips are not
actually strips, but links, audio or video. Then, you'll have to manually
download the media, if you wish. In cases where the script has not been able to
download an *image*, it will create an empty file with the correct name,
without any extension (.gif, .png, ...). This is very useful, especially on
Linux, where the missing files can be visually seen when the output of *ls*
is coloured. Also, in a Bash terminal, the downloaded media can be easily
renamed (*mv*) using the name of the empty file.



## Anomalies

As mentioned above, there are comic strips which are more than simple gif
images. In these cases the script will run in trouble, so we call them
anomalies. A message will be written in the log for each one of these. In some
cases, an image found at the target address can still be downloaded
__manually__. So, to make sure you got the right medium downloaded, please
check using the log file.

During tests, comic strips with the following indices have been found to pose
problems:</br>
[ Normal font: video or audio; **Bold**: links or other stuff ]

191, 194, **574**, **657**, 1433, 1489, 1513, 1519, 1522, 1524, 1526, 1529,
1533, 1535, 1538, 1542, 1547, 1549, 1552, 1556, 1560, 1565, 1567, 1575, 1579,
1582, 1584, 1588, 1594, 1599, 1605, 1616, 1622, 1628, 1635, 1639, 1643, 1649,
1657, 1663, 1669, 1680, 1683, 1685, 1691, 1694, 1707, **1714**, 1716, **1718**,
1726, 1748, 1766, 1769, 1770, 1777, 1788, **1805**, 1845, 1853, 1855, 1864,
1874, 1880, **1886**, 1889, **1902**, 1931, **1933**, **1935**, 1939, **1949**,
**1954**, **1959**, 1964, **1985**, **2009**, 2025, **2033**, **2041**,
**2047**
</br></br>

**Notes about some of the anomalies:** </br>
1718: Turing test awaiting input from user, </br>
1805: doodles for all the people who donated to kickstart the sequel to the PhD
Movie, </br>
1933: the comic on this page cycles randomly through 3 different images every
time the page is loaded, </br>
1949: contains a few pages of the book "We Have No Idea" plus audio and a link.
</br>

**1168:** this is not an anomaly, but I would like to mention that this page
contains a link to obtain a full size desktop wallpaper in terms of a comic
signed by Jorge Cham.

**2047:** the page contains not just one but a series of comics explaining the
SARS-CoV-2 (COVID-19) virus. Translations in several different languages are
available. The technical issue in downloading the comic strip arises due to the
fact that the series of comics actually consists of many separate JPG images.
</br></br>

**Note about date discrepancies in "list of all comics":** </br>
Comics 2032 to 2040 were released in 2019 but are listed in the 2018 section of
the list of comics at
[http://phdcomics.com/comics/archive_list.php](http://phdcomics.com/comics/archive_list.php).

</br>

### Enjoy the PhD universe!
