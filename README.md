# ![alt text](https://github.com/PhilWicke/IMDBot/blob/master/BotLogo02.jpg "Plot Bot Logo")
This repository contains the files for the IMDB Plotbot [@imdplotbot](https://twitter.com/imdplotbot). This twitter bot will take the top 250 titles of [IMDb](www.imdb.com) in order to create new plots out of the given archives by combining them. The creative approach is a mere random one. Applying the [cut-up technique](https://en.wikipedia.org/wiki/Cut-up_technique) popularized by   William S. Burroughs plot segments will be cut up in beginnings and ends, to be reunited under the restriction of 140 characters.

## Files
Most of the methods used by the bot are stored in _imdpy_. This library features methods that will fetch the necessary data form the IMDb website via an easy and [open source access](http://www.imdb.com/interfaces) via FU Berlin. I refer to the [copyright/license information](http://www.imdb.com/conditions) listed in each file for instructions on allowed usage. The data is _NOT FREE_ although it may be used for free in specific circumstances and I do not claim any copyright.

Importantly, there are two versions that allow to run the plot bot. One that is the enitre process in _imdbot.py_. This one will run and start tweeting plots according to the internal timer. The other method is the _imdbot2txt.py_ which will make use of all the remaining files. The difference here is, that this is outsourcing the computational part and will create a text file holding the created plots. The text file can then be uploaded on a webserver/webservice and a helper scipt _plotbot.py_ will tweet the list. This approach also sends emails if the list of plots shortens or runs out.

## Modules
Python version 2.7 (should be compatible with 3.5)
Modules available for 2.7:

[Tweepy](https://pypi.python.org/pypi/tweepy/2.0) (also available for 3+)

[gzip File Support](https://docs.python.org/2/library/gzip.html) (also available for 3+)

[FTP Protocol Client](https://docs.python.org/2/library/ftplib.html) (also available for 3+)

## Necessary segments
The twitter handle requires a consumer access and keys. This can be found at _apps.twitter.com -> my applications -> Keys and Access Tokens_. Naturally, the email sender and recipient for the status alert has to be adapted.

I hope you enjoy the project and feel free to share any ideas, additions and criticism.
