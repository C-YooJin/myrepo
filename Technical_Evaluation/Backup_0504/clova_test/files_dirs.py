import os
import itertools
import glob


def get_files(path, format):
    """
    :param path: path to the directory that contains csv files with TextGrid label information
    :param format: file extension (ex: "*.csv", "*.TextGrid"..)
    :return: list of all files in specified extension
    """
    format = path + "/" + format
    filelist = [file for file in glob.glob(format)]
    #print("filelist:", filelist)
    return filelist


def rename_duplicate_newfile(file_path):
    """
    If there is(are) a file(s) with same base name in the given directory,
    it gives a new name in a basename_duplicate(count) format
    :param file_path: where to save file
    :return: file name
    """
    yield file_path
    base, ext = os.path.splitext(file_path)
    yield base + "_duplicate" + ext
    for num in itertools.count(1):
        yield base + "_duplicate(%i)"%(num) + ext


def get_immediate_subdirectories(path):
    return [path+"/"+name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name))]


