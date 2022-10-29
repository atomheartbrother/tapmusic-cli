import requests
import shutil
import click
import pathlib
from datetime import datetime
# Tapmusic

@click.command()
@click.argument('user')
@click.argument('size')
@click.argument('time')
@click.argument('dir')
@click.argument('caption', default='t')
@click.argument('playcount', default='f')


def tapmusic(user:str, size:str, time:str, dir:str, caption:str, playcount:str):
    
    """tapmusic-cli \n
    user = Your Last.fm username \n
    size = Collage size.\n 
        OPTIONS: 3, 4, 5, 10 (premium) \n
    time = Time period of your Last.fm history. \n
        OPTIONS: 7d, 1m, 3m, 6m, 12m \n
    caption = Display album/artist captions? \n
        OPTIONS: t, f \n
    playcount = Display playcount? \n
        OPTIONS: t, f \n
    """

    if size not in ('3', '4', '5', '10'):
        raise click.UsageError('Invalid size parameter \n OPTIONS: 3, 4, 5, 10 (premium)')

    elif time not in ('7d', '1m', '3m', '6m', '12m'):
        raise click.UsageError('Invalid time parameter \n OPTIONS: 7d, 1m, 3m, 6m, 12m')

    elif caption not in ('t', 'f'):
        raise click.UsageError('Invalid caption parameter \n  OPTIONS: t, f')

    elif playcount not in ('t','f'):
        raise click.UsageError('Invalid playcount parameter \n  OPTIONS: t, f')

    size = f'{size}x{size}'
    #if direcotry has filetype, use that as filename. otherwise generate filename from user inputs

    if 'm' in time:
        time = f'{time[0]}month'
    else:
        time = f'{time[0]}day'

    if caption == 't':
        caption = 'true'
    else: caption = 'false'

    if playcount == 't':
        playcount = 'true'
    else: playcount = 'false'


    fe = pathlib.Path(dir).suffix

    if fe not in ('.jpg','.png'):
        fname = f'{dir}{user}_{time}_{size}_{datetime.today().strftime("%Y-%m-%dcd_%H:%M:%S")}.jpg'
    else:
        fname = dir
    
    base = "https://tapmusic.net/collage.php"

    if caption == 'true' and playcount == 'true':
        url = f"{base}?user={user}&type={time}&size={size}&caption={caption}&playcount={playcount}"

    elif caption == 'true' and playcount == 'false':
        url = f"{base}?user={user}&type={time}&size={size}&caption={caption}"

    elif caption == 'false' and playcount == 'true':
        url = f"{base}?user={user}&type={time}&size={size}&playcount={playcount}"

    else: url = f"{base}?user={user}&type={time}&size={size}"
    

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
        #catastrophic error. bail.
        raise SystemExit(e)

    except requests.exceptions.HTTPError as httpe:
        #If you want http errors (e.g. 401 Unauthorized) to raise exceptions, you can call Response.raise_for_status. That will raise an HTTPError, if the response was an http error.
        raise SystemExit(httpe)

    except Exception as e:
        print(e)

    del response
# Render output in terminal before user saves it(future update)

if __name__ == '__main__':
    tapmusic()