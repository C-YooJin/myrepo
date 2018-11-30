#!/bin/bash

DIR=$1
#DIR=/home1/irteam/cuve/cuve-reader-3.6.30/download

cd $DIR
COUNT=`ls -1 | wc -l`
echo $COUNT

if [ $COUNT = 1 ]; then
    echo "last one"
    ls | xargs -i rsync --remove-source-files -av {} irteam@cnsmldb103.clova:~/twitter/
elif [ $COUNT = 0 ]; then
    echo "done"
    exit
else
    echo "moving files"
    ls | head -n -1 | xargs -i rsync --remove-source-files -av {} irteam@cnsmldb103.clova:~/twitter/
fi


