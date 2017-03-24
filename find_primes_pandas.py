#!/usr/bin/python3
import pandas as pd
import multiprocessing as mp
import sys, os, subprocess, re

LARGE_FILE = "test"
CHUNKSIZE = 100000 # processing 100,000 rows at a time
WORKERS = 200

def process_frame(df):
    print(type(df))
#    return df
if __name__ == '__main__':
    reader = pd.read_table(LARGE_FILE, chunksize=CHUNKSIZE)
    pool = mp.Pool(WORKERS) 

    funclist = []
    for df in reader:
        # process each data frame
        f = pool.apply_async(process_frame,[df])
        funclist.append(f)

    result= []
    for f in funclist:
        result += [f.get(timeout=10)] # timeout in 10 seconds

#    print(result)
