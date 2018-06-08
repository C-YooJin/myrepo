import textgrid_parser as tp
import calculation


if __name__ == "__main__":
    # Change "lbpath" to run it on your computer.
    # It should be a directory that contains all TextGrid files of one brand
    # If you name the directory after the speaker brand's name,
    # it will be easier to compare the response time between brands in the final result file

    # Set directory path with label result
    lbpath = "/Users/user/Desktop/prep/clova"

    # Labeled TextGrids as input files
    find_these = "*.TextGrid"

    # Result file format
    result_file = "final_result.csv"

    tp.tg2csv(lbpath, find_these)
    resultfile = calculation.get_mean_result(lbpath, result_file)
    calculation.total_mean(resultfile)
    calculation.compare_results(lbpath)







