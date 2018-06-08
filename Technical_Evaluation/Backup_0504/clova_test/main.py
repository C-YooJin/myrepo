import textgrid_parser as tp
import calc3
import files_dirs


if __name__ == "__main__":
    # Change "lbpath" to run it on your computer.
    # It should be a directory that contains all TextGrid files of one brand
    # If you name the directory after the speaker brand's name,
    # it will be easier to compare the response time between brands in the final result file

    # Set directory path with label result
    dir_path = "/Users/user/Desktop/Sample_Test2"

    # Labeled TextGrids as input files
    find_these = "*.TextGrid"

    # Result file format
    result_file = "final_result.csv"

    all_dirs = files_dirs.get_immediate_subdirectories(dir_path)
    #print(all_dirs)
    for dir in all_dirs:
        #print(dir)
        tp.tg2csv(dir, find_these)
        resultfile = calc3.get_mean_result(dir, result_file)
        calc3.total_mean(resultfile)
    calc3.compare_results(dir_path, result_file)







