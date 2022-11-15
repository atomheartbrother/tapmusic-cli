import requests
import shutil
import click
import pathlib
from datetime import datetime

@click.command()
@click.argument('user')
@click.argument('size')
@click.argument('time')
@click.argument('dir')
@click.argument('caption', default='t')
@click.argument('playcount', default='f')


def tapmusic(user:str, size:str, time:str, dir:str, caption:str, playcount:str):
    
    """tapmusic-cli \n
    user = Your Last.fm username. \n
    size = Collage size.\n 
        OPTIONS: 3, 4, 5, 10 (premium) \n
    time = Time period of your Last.fm history. \n
        OPTIONS: 7d, 1m, 3m, 6m, 12m, all \n
    dir = Directory where you want to save your collage. \n
        To use a custom filename for your collage file, please use .jpg or .png as file extension. \n
            EX: /path/to/file/myCustomCollage.jpg \n
        Otherwise, if only a directory is provided, a filename will be generated using user inputs and current date. \n
            EX: /path/to/file/$USER_$TIME_$SIZE_$DATETIME.jpg \n
    caption = Display album/artist captions? \n
        OPTIONS: t, f \n
    playcount = Display playcount? \n
        OPTIONS: t, f \n
    """
    
    #Verify user entered acceptable inputs. If not, raise error to explain issue. 
    if size not in ('3', '4', '5', '10'):
        raise click.UsageError('Invalid size parameter \n OPTIONS: 3, 4, 5, 10 (premium)')

    elif time not in ('7d', '1m', '3m', '6m', '12m', 'all'):
        raise click.UsageError('Invalid time parameter \n OPTIONS: 7d, 1m, 3m, 6m, 12m')

    elif caption not in ('t', 'f'):
        raise click.UsageError('Invalid caption parameter \n  OPTIONS: t, f')

    elif playcount not in ('t','f'):
        raise click.UsageError('Invalid playcount parameter \n  OPTIONS: t, f')

    #Take users size input and construct correctly formatted string for URL.
    size = f'{size}x{size}'

    #Take users time input and construct correctly formatted string for URL.
    if 'm' in time:
        time = f'{time[0]}month'
    elif 'd' in time:
        time = f'{time[0]}day'
    else:
        time = 'overall'

    #Change caption input to correctly formatted string.
    if caption == 't':
        caption = 'true'
    else: caption = 'false'

    #Change playcount input to correctly formatted string.
    if playcount == 't':
        playcount = 'true'
    else: playcount = 'false'

    #Use .suffix on dir input to check if user added a file extension.
    #If user added file extension that is not jpg or png, construct filename using dir + user inputs + current datetime + .jpg.
    fe = pathlib.Path(dir).suffix
    
    if fe in ('.jpg','.png', 'jpeg'):
        fname = dir
    else:
        base_dir = f"{dir.rsplit('/',1)[0]}/"
        fname = f"{base_dir}/{user}_{time}_{size}_{datetime.today().strftime('%Y-%m-%d_%H:%M:%S')}.jpg"
    
    base_url = "https://tapmusic.net/collage.php"

    if caption == 'true' and playcount == 'true':
        url = f"{base_url}?user={user}&type={time}&size={size}&caption={caption}&playcount={playcount}"

    elif caption == 'true' and playcount == 'false':
        url = f"{base_url}?user={user}&type={time}&size={size}&caption={caption}"

    elif caption == 'false' and playcount == 'true':
        url = f"{base_url}?user={user}&type={time}&size={size}&playcount={playcount}"

    else: url = f"{base_url}?user={user}&type={time}&size={size}"
    
    #Send created request to tapmusic.net and output image to filepath contained in fname
    try:
        response = requests.get(url, stream=True)
        with open(f'{fname}', 'xb') as out_file:
            shutil.copyfileobj(response.raw, out_file)

    except requests.exceptions.Timeout as t:
        #Maybe set up for a retry, or continue in a retry loop
        print(t)

    except requests.exceptions.TooManyRedirects as tme:
        #Tell the user their URL was bad and try a different one
        print(tme)

    except requests.exceptions.RequestException as e:
        #Catastrophic error.
        raise SystemExit(e)

    except requests.exceptions.HTTPError as httpe:
        #If you want http errors (e.g. 401 Unauthorized) to raise exceptions, you can call Response.raise_for_status. That will raise an HTTPError, if the response was an http error.
        raise SystemExit(httpe)

    except Exception as e:
        print(e)

    del response

if __name__ == '__main__':
    tapmusic()