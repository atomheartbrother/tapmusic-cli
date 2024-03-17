from typing import Union
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import argparse
import requests

@dataclass
class Directory:
    """
    Descriptor for directory attribute
    """
    __dir: str = ''

    @staticmethod
    def dir_validate(value):
        if value.suffix != '':
            raise ValueError(f"{value} is not a valid directory. If you're trying to use a custom filename, use the `--file` flag.")

    def __get__(self, instance, owner):
        return self.__dir

    def __set__(self, instance, value):
        value_path = Path(value)
        self.dir_validate(value=value_path)
        self.__dir = value_path

@dataclass
class File:  
    """
    Descriptor for file attribute
    """
    __file: str = ""

    @staticmethod
    def ext_validate(value: Path, options: list = ['.jpg', '.jpeg', '.png']):
        if value.suffix not in options:
            raise ValueError(f"Invalid file extension {str(value.suffix)}. Valid values: {options!r}")

    def __get__(self, instance, owner):
        return self.__file

    def __set__(self, instance, value):
        if value is not None:
            self.ext_validate(value=Path(value))
            self.__file = value

@dataclass
class Size:
    """
    Descriptor for size attribute
    """
    __size: str = ''

    def __get__(self, instance, owner):
        return self.__size

    def __set__(self, instance, value):
        self.__size = f'{value}x{value}'

@dataclass
class Time:
    """
    Descriptor for time attribute
    """
    __time: str = ''

    def __get__(self, instance, owner):
        return self.__time

    def __set__(self, instance, value):
        last = value[-1]
        rest = value[:-1]

        if last == 'm':
            time_fmt = rest + 'month'
        elif last == 'd':
            time_fmt = rest + 'day'
        else:
            time_fmt = 'overall'

        self.__time = time_fmt

@dataclass
class StrToBool:
    """
    Descriptor for t/f attributes.
    If incoming value is 't' will change to 'true'. If 'f' then 'false' 
    """
    __value: str = ''

    def __get__(self, instance, owner):
        return self.__value

    def __set__(self, instance, value):
        if value == 't':
            self.__value = str(True).lower()
        else:
            self.__value = str(False).lower()

class TapMusicCLI():

    dir_ = Directory()
    size = Size()
    time = Time()
    caption = StrToBool()
    playcount = StrToBool()
    file_ = File()

    def __init__(self, user: str, dir_: str, size: str, time: str, caption: str, playcount: str, file_: Union[None, str]):
        """
        tapmusic-cli

        Args:
            `user:`
                Your last.fm username.

            `size:`
                Collage size. 
                `OPTIONS:` `[3, 4, 5, 10]`

            `time:`
                Time period of your Last.fm history.
                `OPTIONS:` `[7d, 1m, 3m, 6m, 12m, all]`

            `dir_:`
                Directory where you want to save your collage.

            `caption: (optional)`
                Display album/artist captions in collage?
                `OPTIONS:` `[t, f]`
                `DEFAULT:` `t`

            `playcount: (optional)`
                Display playcount in collage?
                `OPTIONS:` `[t, f]`
                `DEFAULT:` `f`

            `file_: (optional)`
                Save returned collage under a custom file name.
                File extension can only be .jpg, .jpeg, or .png.
                `DEFAULT:` `$USER_$TIME_$SIZE_$%Y-%m-%d_%H%M%S.jpg`
        """

        self.user: str = user
        self.dir_: str = dir_
        self.size: str = size
        self.time: str = time 
        self.caption: str = caption
        self.playcount: str = playcount
        self.file_: str = file_
        self.fpath: Path = self._build_filepath()

        self.base_url: str = "https://tapmusic.net/collage.php"
        self.url: str = self._build_url()

    def _build_filepath(self) -> Path:
        if self.file_ == '':
            self.file_ = f"{self.user}_{self.time}_{self.size}_{datetime.today().strftime('%Y-%m-%d_%H%M%S')}.jpg"
        return self.dir_ / self.file_

    def _build_url(self) -> str:
        url = f"{self.base_url}?user={self.user}&type={self.time}&size={self.size}"

        if self.caption == 'true':
            url = f"{url}&caption={self.caption}"

        if self.playcount == 'true':
            url = f"{url}&playcount={self.playcount}"

        return url

def cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("user", type=str, help="Your last.fm username")
    parser.add_argument("dir", type=str, help="Directory where you want to save your collage")
    parser.add_argument("size", type=str, choices=['3', '4', '5', '10'], help="Collage size")
    parser.add_argument("time", type=str, choices=['7d', '1m', '3m', '6m', '12m'], help="Time period of your Last.fm history")

    parser.add_argument("-f", "--file", type=str, help="File name for your collage")
    parser.add_argument("-c", "--caption", type=str, choices=['t', 'f'], default='t', help="Display album/artist captions in collage?")
    parser.add_argument("-pc", "--playcount", type=str, choices=['t', 'f'], default='f', help="Display playcount in collage?")
    
    return parser.parse_args()

def get_collage(url: str, fpath: str):
    try:
        #Send created request to tapmusic.net
        response = requests.get(url, stream=True)
        
        #Use iter_content to break down response content into list
        #Once all response content is appended to list, convert the chunk list to bytes
        chunks = [chunk for chunk in response.iter_content()]
        full_content = b''.join(chunks)

        #Check if response sends back any errors, if so, raise error to user. Otherwise, write image to filepath
        #Program will not overwrite a file if it already exists
        if 'Error 90' in str(full_content):
            raise Exception('User does not have any top albums for the selected time period. \nPlease choose different time period or listen to more music :)')
        elif 'Error 99' in str(full_content):
            raise Exception('Last.fm user does not exist or Last.fm API is currently unavailable')
        else:
            with open(fpath, 'xb') as f:
                f.write(full_content)

    except requests.exceptions.Timeout as t:
        print(f"Request timed out, try again later. Details:{t.__str__()}")

    except Exception as e:
        print(f"TapMusicCLI encountered an error. Details: {e.__str__()}")

def app():
    args = cli_args()
    t = TapMusicCLI(user=args.user, dir_=args.dir, size=args.size, time=args.time, caption=args.caption, playcount=args.playcount, file_=args.file)
    get_collage(url=t.url, fpath=t.fpath)

if __name__ == '__main__':
    app()

