# This script performs a backup of a local directory to a remote server using rsync.
#
# Author: Mayank Singh
# Date: 21-09-2024
#
# Variables:
#   LOCAL_DIR: The local directory to be backed up.
#   REMOTE_USER: The username for the remote server.
#   REMOTE_HOST: The IP address or hostname of the remote server.
#   REMOTE_DIR: The directory on the remote server where the backup will be stored.
#
# The script captures the start time, performs the backup using rsync, and then captures the end time.
# It calculates the duration of the backup process and checks if rsync was successful.
# If the backup is successful, it prints a success message along with the time taken.
# If the backup fails, it prints a failure message along with the time taken.
#
# Add to cron job list by 
# crontab -e
# m h  dom mon dow   command
# 0 2 * * * /path/to/backup.sh >> /path/to/backup.log 2>&1
# this will run the script everyday 2 am with the output written to /path/to/backup.log
#
# to prevent 

#!/bin/bash

# Define variables
LOCAL_DIR="/path/to/local/dir"
REMOTE_USER="mayank"
REMOTE_HOST="1.1.1.1"
REMOTE_DIR="/path/to/bkp/dir"

# Capture the start time
START_TIME=$(date +%s)

# Getting the current working branch on the local machine
WORKING_BRANCH_NAME=$(cd $TOPDIR && git branch --show-current)

echo "----------- Starting Backup -----------"
echo "Backup started at $(date)"
echo "Wokring branch on local machine: $WORKING_BRANCH_NAME"

# Use rsync to copy the directory
rsync -avz --delete --update $LOCAL_DIR $REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR

# Capture the end time
END_TIME=$(date +%s)

# Calculate the duration
DURATION=$((END_TIME - START_TIME))

# Check if rsync was successful
if [ $? -eq 0 ]; then
    echo "Backup completed successfully at $(date)"
    echo "Time taken: $DURATION seconds"
else
    echo "Backup failed at $(date)"
    echo "Time taken: $DURATION seconds"
fi

echo "----------- Backup Finished -----------"