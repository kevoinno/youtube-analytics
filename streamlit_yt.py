import streamlit as st
import pandas as pd
from subprocess import call
import plotly.express as px
from datetime import datetime, timedelta

st.header('Youtube Analytics')

df = pd.read_csv('streamlit_data.csv')
df['published_at'] = pd.to_datetime(df['published_at'])

with st.sidebar:
   make_call = st.button("Make API Call")
   if make_call:
      call(["python", "youtube_trending_api.py"])
      st.write('API call was made')
   st.write(f"**Note:** Video data ranges from {df['published_at'].min().strftime('%Y-%m-%d')} to {df['published_at'].max().strftime('%Y-%m-%d')}\nVisualizations may not capture all months and years")

#Most Popular Trending Cateogries
select_time_frame = st.selectbox('Most popular trending categories (select an option)', ('today', 'in the last week', 'in the last month', 'in the last year', 'all time'))
if select_time_frame == 'today':
   subset = df[df['published_at'].dt.day == datetime.now().day].copy()
elif select_time_frame == 'in the last week':
   filter = (df['published_at'] <= datetime.now()) & (df['published_at'] >= datetime.now() - timedelta(days = 7))
   subset = df[filter].copy()
elif select_time_frame == 'in the last month':
   subset = df[df['published_at'].dt.month == datetime.now().month].copy()
elif select_time_frame == 'in the last year':
   subset = df[df['published_at'].dt.year == datetime.now().year].copy()
elif select_time_frame == 'all time':
   subset = df.copy()

#Most Popular Trending Cateogries
fig_trending = px.bar(x = subset['category_title'].value_counts().index, y = subset['category_title'].value_counts(), color_discrete_sequence=["#FF0000"])
fig_trending.update_layout(title = f"Most Popular Trending Categories {select_time_frame}",
                           xaxis_title = "Category",
                           yaxis_title = "Count"
                           )
st.plotly_chart(fig_trending, theme="streamlit", use_container_width=True)

#Explaining engagement metric
st.markdown("**Engagement** is a metric that is alternative to views, likes, and comments. One advantage this metric has over views as it factors in audience quality and sentiment. The assumption here is that an engaged audience will like and comment on a video they find entertaining.")
st.markdown("**Engagement** is calculated using the following formula:")
st.latex(r'Engagement = \frac{{\text{{Likes}} + \text{{Comments}}}}{{\text{{Views}}}}')
st.markdown("The graphs below let you observe how engagement and other metrics vary based on different variables.")

#Best Time to Upload
time_df = df[['published_at', 'view_count', 'like_count', 'comment_count', 'engagement']].copy()
time_df['published_at'] = pd.to_datetime(time_df['published_at'])

time_metric = st.selectbox('Select a metric to use', ('engagement', 'views', 'likes', 'comments'))
time_frame = st.selectbox('Select time to split by', ('hour', 'day of the week', 'month', 'year'))

metric_dict = dict(engagement = 'engagement',
                        views = 'view_count',
                        likes = 'like_count',
                        comments = 'comment_count')
if time_frame == 'hour':
   time_df_selection = time_df.groupby(time_df['published_at'].dt.hour).mean() 
elif time_frame == 'day of the week':
   time_df_selection = time_df.groupby(time_df['published_at'].dt.day_name()).mean()
   time_df_selection = time_df_selection.reindex(list(pd.Series(pd.date_range('2023-01-01', periods=7)).dt.day_name()))
elif time_frame == 'month':
   time_df_selection = time_df.groupby(time_df['published_at'].dt.month.map({1: 'January', 2: 'February', 3: 'March', 4: 'April',
                                            5: 'May', 6: 'June', 7: 'July', 8: 'August',
                                            9: 'September', 10: 'October', 11: 'November', 12: 'December'})).mean()
elif time_frame == 'year':
   time_df_selection = time_df.groupby(time_df['published_at'].dt.year).mean()



fig_upload = px.bar(x = time_df_selection.index, y = time_df_selection[metric_dict[time_metric]], color_discrete_sequence=["#FF0000"])
fig_upload.update_layout(title = f"Mean {time_metric} by {time_frame}",
                           xaxis_title = f"{time_frame}",
                           yaxis_title = f"{time_metric}"
                           )
st.plotly_chart(fig_upload, theme="streamlit", use_container_width=True)
st.write(f'Based on {time_metric}, the best {time_frame} to upload is {time_df_selection[time_df_selection[metric_dict[time_metric]] == time_df_selection[metric_dict[time_metric]].max()].index.tolist()[0]}, as the mean {time_metric} is {round(time_df_selection[metric_dict[time_metric]].max(), 2)}')

#Best time to upload
duration_metric = st.selectbox('Select a metric to compare to duration', ('engagement', 'views', 'likes', 'comments'))
fig_duration_scatter = px.scatter(x = df['duration'], y = df[metric_dict[duration_metric]], color_discrete_sequence=["#FF0000"])
fig_duration_scatter.update_layout(title = f"Scatterplot of {duration_metric} by duration (min)",
                           xaxis_title = f"duration (min)",
                           yaxis_title = f"{duration_metric}"
                           )

st.plotly_chart(fig_duration_scatter, theme="streamlit", use_container_width=True)




