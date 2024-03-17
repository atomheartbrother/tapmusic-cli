# tapmusic-cli
![PyPI](https://img.shields.io/pypi/v/tpmsc?color=g)

CLI tool to download music collages from [tapmusic.net](https://tapmusic.net/)

## Requirements

-  Last.FM account connected to your music player of choice
   - [Create Last.FM account](https://www.last.fm/home) if you do not already have one
   - Connect your music player to Last.FM, [Guide for Spotify ](https://community.spotify.com/t5/FAQs/How-can-I-connect-Spotify-to-Last-fm/ta-p/4795301)
-  Python 3.5^ installed on your machine

## Installation and Usage

### Install 
`pip install tpmsc`

### Run 
`tpmsc [user] [size] [time] [dir] [caption]* [playcount]* [file]`
   -  `*` = optional args

#### Args:
   -  **user** = Your Last.fm username.
   
   -  **size** = Collage size.
      -  Options: `3, 4, 5, 10`

   -  **time** = Time period of your Last.fm history.
      -  Options: `7d, 1m, 3m, 6m, 12m, all`
      
   -  **dir** = Directory where you want to save your collage.
         
   -  **caption** = Display album/artist captions? *Optional*
      -  Options: `t, f`
      -  Default = `t`
      
   -  **playcount** = Display playcount? *Optional*
      -  Options: `t, f`
      -  Default = `f`
   
   -  **file** = Save returned collage under a custom file name. *Optional*
      - Default = `$USER_$TIME_$SIZE_$%Y-%m-%d_%H%M%S.jpg`

## Examples
###### 5x5 (artist name & playcount):

![5x5](/images/5x5_playcount.jpg)

###### 3x3 (no artist name or playcount):

![3x3](/images/3x3.jpg)

###### 10x10 (artist name, no playcount):

![10x10](/images/10x10.jpg)

## Todo
- [x] UNIX support

- [x] Windows support