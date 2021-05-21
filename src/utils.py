import json_lines
from datetime import datetime
import pandas as pd
import altair as alt
import numpy as np

def iso_to_string(isostring):
    split = isostring.split("T")
    datetimestring = split[0] + " " + split[1][:5]
    return datetimestring

def tweetjson_to_df(filename):
    tweetlist = []
    with open(filename, 'rb') as f:
        for tweet in json_lines.reader(f):
            tweetdict = {}
            tweetdict["id"] = tweet["id"]
            time = tweet["created_at"]
            tweetdict["time"] = datetime.strptime(
                time, '%a %b %d %X %z %Y').isoformat()
            if 'retweeted_status' in tweet:
                tweetdict["type"] = "retweets"            
            else:
                tweetdict["type"] = "original tweets"
            tweetlist.append(tweetdict)
    tweetdf = pd.DataFrame(tweetlist)
    return tweetdf

def tweetjson_to_dff(data):
    tweettempdf = data
    # tweettempdf = pd.read_csv(filename)
    tweetdf = tweettempdf[['id', 'created_at']]
    tweetdf['type'] = np.where(tweettempdf['tweet'].str[0:2] == 'RT', 'retweets', 'original tweets')
    print("problem in tweetjson_to_dff")
    tweetdf['created_at'] = pd.to_datetime(tweetdf['created_at']).dt.strftime('%Y-%m-%dT%H:%M%:%SZ')
    print("problem in tweetjson_to_dff 2")
#     tweetdf['created_at'] = pd.to_datetime(tweetdf['created_at'] ,errors='coerce').dt.date
    print("no problem in tweetjson_to_dff")

    tweetdf.columns = ['id', 'time', 'type']

    return tweetdf


def groupby_dates(tweetdf):
    print("problem in groupby_dates")
    tweetdf["time"] = pd.to_datetime(tweetdf["time"])
    print("problem in groupby_dates 1")
    tweetdf = tweetdf.set_index("time")
    print("problem in groupby_dates 2")
    grouper = tweetdf.groupby([pd.Grouper(freq='1H'), 'type'])
    result = grouper['type'].count().unstack('type').fillna(0)
    print("problem in groupby_dates 3")
    result["datetime"] = result.index
    print("problem in groupby_dates 4")
    result["total"] = result["original tweets"] + result["retweets"]
    print("no problem in groupby_dates ")
    return result

def plot(grouped_tweetdf, order=["original tweets", "retweets"]):
    # set color range
    domain = ['retweets', 'original tweets','total']
    range_ = ['#1F77B4', '#D62728','grey']

    # plot original tweets and retweets
    C1 = alt.Chart(grouped_tweetdf).mark_area(opacity=0.6).transform_fold(
        fold=order,
        as_=['variable', 'value']
    ).encode(
        alt.X('datetime:T', timeUnit='yearmonthdatehours', title="date"),
        alt.Y('value:Q', stack=None, title="tweet count"),
        color=alt.Color("variable:N",
                        legend=alt.Legend(title="tweet type"),
                        scale=alt.Scale(domain=domain, range=range_),
                         )
    ).properties(width=800, height=500)

    # plot total in background    
    C2 = alt.Chart(grouped_tweetdf).mark_area(opacity=0.15).encode(
        alt.X(f'datetime:T', timeUnit='yearmonthdatehours', title='date'),
        alt.Y('total:Q'),
        color=alt.value("black"))

    return C1+C2    
