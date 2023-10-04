#!/bin/bash
for VIDPATH in $(find results -type f -name "*.h264")
do
    MKVPATH=$(echo $VIDPATH | sed -e 's/\.h264/\.mkv/')
    TCPATH=$(echo $VIDPATH | sed -e 's/\.h264/\.ts.txt/')
    if [ ! -e $MKVPATH ]
    then
        echo "Creating $MKVPATH"
        mkvmerge -o $MKVPATH --timecodes 0:$TCPATH $VIDPATH
    fi
done
