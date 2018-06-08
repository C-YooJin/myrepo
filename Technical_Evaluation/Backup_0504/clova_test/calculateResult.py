import pandas as pd
import os
import glob
import csv
#import itertools


def get_csvfiles(path, exclude=None):
    files = []
    os.chdir(path)
    if exclude:
        fileslist = [file for file in glob.glob("*.csv") if not os.path.basename(file).startswith(exclude)]
    for file in fileslist:
        files.append(file)
    return files


def csv2dataframe(file):
    df = pd.read_csv(file, header = 0, encoding='utf8')
    return df


def get_silence_dur(df):
    df = df.loc[df['label'] == 'silent'].copy()
    df['duration'] = df['xmax'] - df['xmin']
    return df

"""
def dup_resultfile_chk(path, filename):
    yield filename
    base, ext = os.path.splitext(filename)
    yield base + "(Duplicate)" + ext
    for num in itertools.count(1):
        yield base + "(Duplicate %i)"%(num) + ext
"""


def get_mean_result(path, result_file):
    data_path = path
    result_path = path + "/result_directory"
    try:
        os.stat(result_path)
    except:
        os.mkdir(result_path)

    #if os.path.exists(result_file):
    #    print(result_file)
    #    filename = next(alt_name
    #                    for alt_name in dup_resultfile_chk(result_path, result_file)
    #                    if not os.path.exists(alt_name))

    #else:
    filename = result_file
    #print(filename)

    f = open(result_path+"/"+filename, "w", encoding='utf8')
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
    df = pd.read_csv(result_file, encoding='utf8', header = 0)
    last_row = df.iloc[-1, :]
    df = df.iloc[:-1, :]
    df[["Mean silence detected", "# of intervals"]] = df[["Mean silence detected", "# of intervals"]].apply(pd.to_numeric)
    df["Total"] = df["Mean silence detected"] * df["# of intervals"]
    two_up = os.path.abspath(os.path.join(result_file, "../.."))
    result = ["total mean(entire dataset)", os.path.basename(two_up), (df["Total"].sum()) / (df["# of intervals"].sum())]

    with open(result_file,'a') as f:
        resultfile = csv.writer(f)
        resultfile.writerow(result)


def compare_results(lbpath):
    upper_dir = os.path.abspath(os.path.join(lbpath, os.pardir))
    comparison_file = open(upper_dir+"/comparison.csv", "w", encoding = "utf8")
    for filename in glob.iglob(upper_dir + '/*/result_directory/final_result.csv', recursive=True):
        df = pd.read_csv(filename, encoding='utf8', header = 0)
        one_brand_mean_result = df.iloc[-1, :]
        add_to_comparison = csv.writer(comparison_file)
        add_to_comparison.writerow(one_brand_mean_result)