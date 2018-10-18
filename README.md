# Coming soon: PhD Comics downloader

Being a PhD student myself, PhD Comics is a part of my everyday life. It gives me confidence in times of doubt and it often reminds me how important my small "steps" are for research and science in general.

So, do check out [http://phdcomics.com](http://phdcomics.com)

This repository contains a Python 3 script which aims at the bulk download of the comic strips. It has only been tested successfully on Linux systems, as it has been developed on one of them. So, Windows users out there, if you find a way to make it work, just create an issue here and tell us how to make it work.



## Requirements

The script makes use of the usual python classes such as csv, re and pathlib. Apart from these, it uses the **requests** library. I have seen some systems without a default installation of **requests** in their Python 3 installation. For example, I use Slackware GNU/Linux and had to install **requests**  from [SlackBuilds.org](https://slackbuilds.org/). On Fedora, it can be installed using dnf with the following:
```
# dnf install python3-requests
```
On Debian as well, it is called python3-requests. I'm not a Debian user, but I guess it can be something like
```
# apt-get install python3-requests
```



## How the script works

Firstly, there are two versions of the script because, initially, I tried using **urllib**, which is generally a default library in Python. However, things didn't work out beautifully as for some webpages there is an error due to unicode conversion. So, version 2 was based on **requests** instead, and it is much much better. Further, version 2 is better developed than version 1, and includes more features and stuff. Well, it's just better, thus *please use version 2*.

I left version 1 here just as an example of an implementation making use of **urllib**, for anyone out there experimenting with such things.

For everything to work, we need two files:
* **PhDComics_download_v2.x.py** : executable Python 3 script,
* **PhDComics_dates_titles.txt** : plain text file containing the dates and titles of every comic strip and is used by the download script to name the comic strips.

The dates and titles file is easily created by copying the list at [http://phdcomics.com/comics/archive_list.php](http://phdcomics.com/comics/archive_list.php). There's a small space in front of every date and it is left as is for easier bulk copying. A PhDComics_dates_titles.txt file is already found in the repo and I will try to keep it up-to-date.

The script also needs a start index and end index. You don't necessarily have to download everything at once. The script needs to be edited and the variables **startIdx** and **endIdx** must be initialised. A small trick to know which comics you need to download is to look at their addresses. The index is the number at the end.
e.g. http://phdcomics.com/comics/archive.php?comicid=**1124**

When everything is set, the script is just executed:
```
$ ./PhDComics_download_v2.x.py
```

One very useful feature of the script is that it will write a log report about the whole process. The log file is named **comic_[startIdx]_[endIdx].log**. It will contain messages about every issue encountered while trying to download the comic strips. There will be issues because some of the comic strips are not actually strips, but links, audio or video. Then, you'll have to manually download the media, if you wish. In cases where the script has not been able to download an *image*, it will create an empty file with the correct name, without any extension (.gif, .png, ...). This is very useful, especially on Linux, where the missing files can be visually observed when the output of *ls* is coloured. Also, in a Bash terminal, the downloaded media can be easily renamed (*mv*) using the name of the empty file.



## Anomalies

As mentioned above, there are comic strips which are more than simple gif images. In these cases the script will run in trouble. A message will be written in the log for each one of these. In some cases, an image found at the target address can still be downloaded, but it will probably be some small banner. So, just to make sure you got the right medium downloaded, please check, putting the log file to good use.

During tests of the scripts, comic strips with the following indices have been found to pose problems:


**to be continued ...**



