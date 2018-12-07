#!/bin/bash

SCRIPT_PATH="`dirname \"$0\"`"
SCRIPT_PATH="`( cd \"$SCRIPT_PATH\" && pwd )`"

if [ "$#" -ne 3 ]; then
    echo "Usage: prepare_cuve_twitter_data.sh date data_dir output_dir"
    echo "Example: prepare_cuve_twitter_data.sh 20180701 /data1/twitter /data1/data/reduced"
    exit
fi

#mkdir -p $2
#mkdir -p $3

DATE=$1
DATA_DIR=$2/$DATE
OUTPUT_DIR=$3/$DATE

if [ ! -d $2 ]; then
    echo "You should already have raw data from $1"
    echo "Your data should be at $DATA_DIR"
    exit
fi

#echo "mkdir $DATA_DIR"
#mkdir $DATA_DIR

echo "mkdir $OUTPUT_DIR"
mkdir -p $OUTPUT_DIR

SECONDS=0

echo
echo "Get tweets on $DATE from $DATA_DIR"
echo "Reduce data to having only necessary fields..." 

echo "cd $SCRIPT_PATH"
cd $SCRIPT_PATH

FILES=$DATA_DIR/*
DONE=$DATA_DIR/DONE
if [ ! -d $DONE ]; then
    mkdir -p $DONE

fi



for f in $FILES
do
    if [ -f $f ]; then
        echo "Processing $f file to $OUTPUT_DIR..."
        python3.6 filter_preprocess.py $f $OUTPUT_DIR
        echo "Done with $f .. moving it to $DONE"
        echo "mv $f $DONE"
        echo -e $f ' \t ' `date` >> process_log_$DATE.txt 
        mv $f $DONE
    fi
done
