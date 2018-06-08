import pandas as pd
import numpy as np
import os
import glob
import csv
import itertools


def get_csvfiles(path, exclude=None):
    files = []
    os.chdir(path)
    if exclude:
        fileslist = [file for file in glob.glob("*.csv") if not os.path.basename(file).startswith(exclude)]
    for file in fileslist:
        files.append(file)
    return files


def csv2dataframe(file):
    df = pd.read_csv(file, header = 0)
    return df


def get_silence_dur(df):
    df = df.loc[df['label'] == 'silent'].copy()
    df['duration'] = df['xmax'] - df['xmin']
    return df


def dup_resultfile_chk(path, filename):
    yield filename
    base, ext = os.path.splitext(filename)
    yield base + "(Duplicate)" + ext
    for num in itertools.count(1):
        yield base + "(Duplicate %i)"%(num) + ext



def get_mean_result(path, result_file):
    data_path = path
    result_path = path + "/result_directory"
    print(result_file)
    try:
        os.stat(result_path)
    except:
        os.mkdir(result_path)

    if os.path.exists(result_file):
        print(result_file)
        filename = next(alt_name
                        for alt_name in dup_resultfile_chk(result_path, result_file)
                        if not os.path.exists(alt_name))

    else:
        filename = result_file
        print(filename)

    f = open(result_path+"/"+filename, "w")
    resultfile = csv.writer(f)
    resultfile.writerow(["filename", "Mean silence detected", "# of intervals"])

    files = get_csvfiles(data_path, exclude="final")
    for file in files:
        result = mean_silence_dur(file)
        resultfile.writerow(result)
    resultfile.writerow(["###", "finished", "###"])

    f.close()

    return result_path+"/"+filename


def mean_silence_dur(file):
    df = csv2dataframe(file)
    df = get_silence_dur(df)
    result = [file, df['duration'].mean(), len(df.index)]
    return result


def total_mean(result_file):
    df = pd.read_csv(result_file, header = 0)
    last_row = df.iloc[-1, :]
    df = df.iloc[:-1, :]
    df[["Mean silence detected"]] = df[["Mean silence detected"]].apply(pd.to_numeric)
    #print(last_row)
    #print(df)
    result = pd.Series(["total mean", df["Mean silence detected"].mean()])

    with open(result_file,'a') as f:
        result.to_csv(f)



