#!/bin/bash
# take folder as 1st and only agrument where the files are located
# make file executable by chmod +x patchMFE.sh
# usage ./patchMFE.sh <folder_name_relative_to_curr_dir>
CURR_DIR=$(pwd)

CONTAINER_ID=$(docker ps | grep frontend | grep -Eo "\S*" | head -1)

#check if folder passed in argument and only proceed if it exists
if [ -z $1 ]; then
    echo "Please provide folder name as argument"
    exit 1
fi
cd $1

FILE_LIST_CURR_DIR=$(ls -1 | grep -E ".*\.(js|js.gz)$")

FILE_COUNT=$(echo $FILE_LIST_CURR_DIR | wc -w)
FILE_COPIED=0
for FILE in $FILE_LIST_CURR_DIR
do
    # echo "Copying $FILE to $CONTAINER_ID:/admin_ui/apps/"
    docker cp $FILE $CONTAINER_ID:/admin_ui/apps/
    if [ $? -eq 0 ]; then
        FILE_COPIED=$((FILE_COPIED+1))
    fi
done

if [ $FILE_COUNT -eq $FILE_COPIED ]; then
    echo "All $FILE_COPIED files copied successfully"
else
    echo "Some files failed to copy"
fi

cd $CURR_DIR