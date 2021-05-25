#!/usr/bin/env python

"""Interactive interface for twitter explorer network generation.

Returns plotly timeline of tweets over time.

Transforms previously collected tweets into
retweet networks (link from i to j if i retweets j),
hashtag networks (link between i and j if i and j appear in
the same tweet), clustergraphs (nodes as communities).
"""

__author__ = "Armin Pournaki"
__copyright__ = "Copyright 2020, Armin Pournaki"
__credits__ = ["Felix Gaisbauer", "Sven Banisch", "Eckehard Olbrich"]
__license__ = "GPLv3"
__version__ = "0.1"
__email__ = "pournaki@mis.mpg.de"

import json_lines
import os
import numpy as np
import altair as alt
import pandas as pd
from src.transformations import *
from src.networks import *
from src.utils import *
from datetime import datetime
import datetime as dt
import pathlib



def timelineviz(request_id, hashtag, data):

    # if hashtag == 'covid19':
    #     filename = os.path.join('./data', 'covid19.csv')
    # else:
    #     filename = os.path.join('./data', 'tweetsdf.csv')

    datadir = "./data/"
    outputdir = "./templates/"
    projectdir = outputdir 

    #st.write("Plot the amount of tweets over time.")

    tweetdf = tweetjson_to_dff(data)
    grouped_df = groupby_dates(tweetdf)

    ot_count = int(sum(grouped_df["original tweets"]))
    rt_count = int(sum(grouped_df["retweets"]))
    tt_count = ot_count+rt_count

    if rt_count < ot_count:
        plots = plot(grouped_df, ["original tweets", "retweets"])
    else:
        plots = plot(grouped_df, ["retweets", "original tweets"])


    firstdate_str = str(list(tweetdf.iloc[[-1]]["time"])[0])[:16]
    lastdate_str = str(list(tweetdf.iloc[[0]]["time"])[0])[:16]

    if not os.path.exists(projectdir):
        os.makedirs(projectdir)

    plots.save(f"{projectdir}/{request_id}_timeline.html")

# -------------------------------------------------------------------

def retweetviz(request_id, hashtag, data):
    # if hashtag == 'covid19':
    #     filename = os.path.join('./data', 'covid19.csv')
    # else:
    #     filename = os.path.join('./data', 'tweetsdf.csv')

    datadir = "./data/"
    outputdir = "./templates/"
    projectdir = outputdir 

    G = new_retweetnetwork(data=data)

    # get the first and last tweet    
    edgeslist = list(G.es)

    #st.write(len(edgeslist))
    firstdate_str = iso_to_string(edgeslist[-1]["time"])
    lastdate_str = iso_to_string(edgeslist[0]["time"])

        
    G, cgl = compute_louvain(G)
    cgl_d3 = d3_cg_rtn(cgl)
    cgl_d3["graph"] = {}
    cgl_d3['graph']['type'] = "Retweet network <br> Louvain graph"
    cgl_d3['graph']['hashtag'] = hashtag
    cgl_d3['graph']['collected_on'] = "today"
    cgl_d3['graph']['first_tweet'] = firstdate_str
    cgl_d3['graph']['last_tweet'] = lastdate_str
    cgl_d3['graph']['N_nodes'] = len(cgl_d3["nodes"])
    cgl_d3['graph']['N_links'] = len(cgl_d3["links"])
    x = cg_rtn_html(cgl_d3)
    with open(f"{projectdir}/{request_id}_RTN_CG_louvain.html", "w",
              encoding='utf-8') as f:
        f.write(x)

    G = compute_infomap(G)

    # create d3-graph and fill it with info
    RTN = d3_rtn(G)
    RTN['graph'] = {}
    RTN['graph']['type'] = "Retweet network"
    RTN['graph']['N_nodes'] = len(RTN["nodes"])
    RTN['graph']['N_links'] = len(RTN["links"])
    RTN['graph']['hashtag'] = hashtag
    RTN['graph']['collected_on'] = "today"
    RTN['graph']['first_tweet'] = firstdate_str
    RTN['graph']['last_tweet'] = lastdate_str


    x = rtn_html(data=RTN)
    with open(f"{projectdir}/{request_id}_RTN.html", "w",
              encoding='utf-8') as f:
        f.write(x)

    savename = f"{projectdir}/{request_id}_RTN"
    exportname = f"{projectdir}/export/"
    if not os.path.exists(exportname):
        os.makedirs(exportname)
    convert_graph(G, exportname + "_RTN")
    
# ------------------------------------------------------------------

def hashtagviz(request_id, hashtag, data):

    outputdir = "./templates/"
    projectdir = outputdir 

    node_thresh_htn = 0
    link_thresh_htn = 0

    H = new_hashtagnetwork(data)
       
    H, Hcg = compute_louvain(H)
    cgl_d3 = d3_cg_htn(Hcg)
    cgl_d3["graph"] = {}
    cgl_d3['graph']['type'] = "Hashtag network <br> Louvain graph"
    cgl_d3['graph']['hastag'] = "hashtag here"
    cgl_d3['graph']['collected_on'] = 'today'
    cgl_d3['graph']['first_tweet'] = 'today'
    cgl_d3['graph']['last_tweet'] = 'today'
    cgl_d3['graph']['N_nodes'] = len(cgl_d3["nodes"])
    cgl_d3['graph']['N_links'] = len(cgl_d3["links"])
    x = cg_htn_html(cgl_d3)
    with open(f"{projectdir}/{request_id}_HTN_CG_louvain.html",
              "w", encoding='utf-8') as f:
        f.write(x)


    # get the first and last tweet    
    edgeslist = list(H.es)
    firstdate_str = iso_to_string(edgeslist[-1]["time"])
    lastdate_str = iso_to_string(edgeslist[0]["time"])

    HTN = d3_htn(H)
    HTN['graph'] = {}
    HTN['graph']['type'] = "Hashtag network"
    HTN['graph']['N_nodes'] = len(HTN["nodes"])
    HTN['graph']['N_links'] = len(HTN["links"])
    HTN['graph']['keyword'] = hashtag
    HTN['graph']['collected_on'] = 'today'
    HTN['graph']['first_tweet'] = firstdate_str
    HTN['graph']['last_tweet'] = lastdate_str

    x = htn_html(data=HTN)
    
    with open(f"{projectdir}/{request_id}_HTN.html", "w", encoding='utf-8') as f:
        f.write(x)

    savename = f"{projectdir}/HTN"
    exportname = f"{projectdir}/export/"
    if not os.path.exists(exportname):
        os.makedirs(exportname)
    convert_graph(H, exportname +  "_HTN")

