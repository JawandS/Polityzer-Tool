#!/bin/bash

# create log with timestamp for _year_month_day_hour_minute_second
timestamp=$(date +%Y_%m_%d_%H_%M_%S)
touch ./logs/start_time_log_$timestamp.txt
echo "START polityzer at $date(%H:%M:%S)" >> ./logs/start_time_log_$timestamp.txt

# clear old data
rm -r html/
rm -r results/
rm -r storage/

# run the autodownloader for website downlaoder
echo "START auto_downloader at $date(%H:%M:%S)" >> ./logs/start_time_log_$timestamp.txt
python3 auto_downloader.py
echo "END auto_downloader at $date(%H:%M:%S)" >> ./logs/start_time_log_$timestamp.txt

# run polityzer
python3 polityzer.py
echo "END polityzer at $date(%H:%M:%S)" >> ./logs/logstart_time_log__$timestamp.txt