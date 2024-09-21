# This script performs a backup of a local directory to a remote server using rsync.

Author: Mayank Singh
Date: 21-09-2024

### Local Variables:
- LOCAL_DIR: The local directory to be backed up.
- REMOTE_USER: The username for the remote server.
- REMOTE_HOST: The IP address or hostname of the remote server.
- REMOTE_DIR: The directory on the remote server where the backup will be stored.

<p>The script captures the start time, performs the backup using rsync, and then captures the end time.<br>
It calculates the duration of the backup process and checks if rsync was successful.<br>
If the backup is successful, it prints a success message along with the time taken.<br>
If the backup fails, it prints a failure message along with the time taken.<br>
</p>

### Add to cron job 
    crontab -e
    #m h  dom mon dow   command
    0 2 * * * /path/to/backup.sh >> /path/to/backup.log 2>&1
This will run the script everyday 2 am with the output written to `/path/to/backup.log`

### Logrotate

Create a log rotate config file sample: `/etc/logrotate.d/backup_logrotate.conf`

    /path/to/backup.log {
        size 10M
        rotate 5
        compress
        missingok
        notifempty
        create 0640 root root
        postrotate
            /usr/bin/killall -HUP rsyslogd
        endscript
    }


