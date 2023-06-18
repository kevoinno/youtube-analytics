## Plan
1. Use Youtube API to get data on the trending page
2. Look at tags, upload time, etc.
3. Make visualizations of most popular tags over time, best time to upload, most trending today, title length vs views, # of tags vs views
4. streamlit part 3

## Notes about limitation / assumptions
- some videos did not have tags, likeCounts, commentCounts. Were not included in the analysis. Limitations because of this
- duplicate values while collecting data
- does not take into account how long the video was on the most popular page

## To do
- continue questions and analysis
## The Data
I gathered data about the most popular youtube videos by pulling data using Youtube Data API. I wrote a script that collected video data from Youtube videos at 11:00 AM and PM everyday. More information about the data collection process can be found in youtube_trending_api.py.

## Assumptions and Limitations about the data
Since my script only ran once a day, and Youtube's trending page updates around every 15 minutes, it is possible that I missed the opportunity to collect some videos that were on the trending page for a short amount of time. I could have automated the script to collect more frequently than once per day, but the limited quota usage of the API prevented me from doing so. 

During the data collection process, there were some duplicate videos, as some videos can be on the trending page for more than one day. I decided to remove these duplicates, not taking into account the amount of time a video was on the trending page.

The data was only US youtube videos.