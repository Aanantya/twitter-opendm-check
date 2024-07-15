import json
from configparser import ConfigParser
from datetime import datetime
import jsonpickle
import pandas as pd
import tweepy

config = ConfigParser()


def reset_config(infile):
    config.read('my.ini')
    config.set('FILE', 'name', infile)
    config.set('Cursor', 'cursor', str(-1))
    with open("my.ini", 'w') as configfile:
        config.write(configfile)


def add2columns(infile):
    file = pd.read_csv(infile)
    file["can_dm"] = ""
    file["last_active"] = ""
    file["days"] = ""
    file.to_csv(infile, index=False)
    return


def get_column(column, col_name):
    # i = 0
    try:
        i = column.index(col_name)
    except IndexError as e:
        raise e
    return i


def fetch(infile):
    config.read("my.ini")

    consumer_key = config.get("DEFAULT", "consumer_key")
    consumer_secret = config.get("DEFAULT", "consumer_secret")
    file = config.get('FILE', 'name')
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth)
    if not api:
        return "error"

    if file != infile:
        reset_config(infile)
        add2columns(infile)

    today = datetime.today()
    d1 = today.date()

    #example screen_name = 'ashiv28983908'
    screen_name = 'screen_name'

    df = pd.read_csv(infile)

    column = list(df.columns)

    # Receive header column index
    p = get_column(column, "user_screen_name")
    q = get_column(column, "can_dm")
    r = get_column(column, "last_active")
    s = get_column(column, "days")

    users = df.iloc[:, p]

    config.read('my.ini')

    cursor = config.get('Cursor', 'cursor')

    k = int(cursor) + 1

    try:
        for user in users:
            print(user)
            try:
                data = api.show_friendship(source_screen_name=screen_name, target_screen_name=user)
                data = jsonpickle.encode(data[0]._json, unpicklable=False)
                friendship = json.loads(data)
                #print(friendship)

                statuses = api.user_timeline(screen_name=user, count=1)
                #print(statuses)

                df.iloc[k, q] = friendship['can_dm']
                if len(statuses) != 0:
                    data = [s.created_at for s in statuses]
                    df.iloc[k, r] = data[0]
                    d2 = data[0].date()
                    diff = d1 - d2

                    df.iloc[k, s] = diff.days
                    #print("today : {0}\tdate[0] : {1}\t = {2}".format(today, data[0], str(diff.days)))

                else:
                    df.iloc[k, r] = '--'
                    df.iloc[k, s] = '--'

            except tweepy.error.TweepError:
                raise tweepy.error.TweepError
                df.iloc[k, q] = '--'
                df.iloc[k, r] = '--'
                df.iloc[k, s] = '--'
    except IndexError as e:
        # print("Done!!")
        raise e

    finally:
        with open("my.ini", 'w') as configfile:
            config.set('Cursor', 'cursor', str(k - 1))
            config.write(configfile)
            df.to_csv(infile, index=False)
        return "Done"
