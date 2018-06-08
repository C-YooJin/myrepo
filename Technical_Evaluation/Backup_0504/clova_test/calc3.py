import pandas as pd
import os
import glob
import csv
import files_dirs






def csv2dataframe(file):
    """
    :param file: One CSV file
    :return: DataFrame object read from the CSV file
    """
    df = pd.read_csv(file, header = 0, encoding='utf8')
    return df


def get_silence_dur(df):
    """
    Calculates silence duration using the "silent" label of the original DataFrame
    :param df: DataFrame object
    :return: DataFrame object with 'duration' column
    """
    # Get only the "silent" intervals from the original DataFrame
    df = df.loc[df['label'] == 'silent'].copy()
    df['duration'] = df['xmax'] - df['xmin']
    return df





def get_mean_result(data_path, result_file):
    """
    Get mean silence duration of each csv file(result of TextGrid parsing) in a given directory,
    and saves it in a csv file.
    Output csv file contains summarized information of all audio files in a given path.
    :param data_path: directory path that contains csv files
    :param result_file: name of the result file
    :return: path of the result file
    """
    result_path = data_path + "/result_directory"
    result_file_path = result_path + "/" + result_file
    try:
        os.stat(result_path)
    except:
        os.mkdir(result_path)

    if os.path.exists(result_file_path):
        filename = next(alt_name
                        for alt_name in files_dirs.rename_duplicate_newfile(result_file_path)
                        if not os.path.exists(alt_name))

    else:
        filename = result_file_path

    f = open(filename, "w", encoding='utf8')
    resultfile = csv.writer(f)
    resultfile.writerow(["filename", "Mean silence detected", "# of intervals"])

    files = files_dirs.get_files(data_path, format="*.csv")
    for file in files:
        result = mean_silence_dur(file)
        resultfile.writerow(result)
    resultfile.writerow(["###", "finished", "###"])

    f.close()

    return filename


def mean_silence_dur(file):
    """
    Get pandas DataFrame from a csv file and calculate mean silence duration,
    and returns the result new row with mean silence duration of given file.
    :param file: file path
    :return: one row
    """
    df = csv2dataframe(file)
    df = get_silence_dur(df)
    result = [file, df['duration'].mean(), len(df.index)]
    return result


def total_mean(result_file):
    """
    Calculates total mean from information given in each row of the result file.
    Adds one row(calculated total mean) to the result file.
    :param result_file: result file path
    """
    df = pd.read_csv(result_file, encoding='utf8', header = 0)
    last_row = df.iloc[-1, :]
    df = df.iloc[:-1, :]
    df[["Mean silence detected", "# of intervals"]] = df[["Mean silence detected", "# of intervals"]].apply(pd.to_numeric)
    df["Total"] = df["Mean silence detected"] * df["# of intervals"]
    two_up = os.path.abspath(os.path.join(result_file, "../.."))
    result = ["total mean(entire dataset)", os.path.basename(two_up), (df["Total"].sum()) / (df["# of intervals"].sum())]

    with open(result_file,'a') as f:
        result_file = csv.writer(f)
        result_file.writerow(result)


def compare_results(dir_path, result_files):
    """
    Goes through all the subdirectories from the given path,
    and finds csv files that contains total mean of all files in one directory.
    Gets necessary information from each files and saves the final result so that it would be easier to compare
    results from different directories.
    :param dir_path: Directory path
    :return: Gets all the result files from different subdirectories and puts the result in one final csv file
    """
    comparison_file = open(dir_path+"/comparison.csv", "w", encoding = "utf8")
    #for filename in glob.iglob(upper_dir + '/*/result_directory/final_result.csv', recursive=True):

    filenames = files_dirs.get_files(dir_path+"/*/result_directory", format=result_files)
    for filename in filenames:
        df = pd.read_csv(filename, encoding='utf8', header = 0)
        one_brand_mean_result = df.iloc[-1, :]
        add_to_comparison = csv.writer(comparison_file)
        add_to_comparison.writerow(one_brand_mean_result)