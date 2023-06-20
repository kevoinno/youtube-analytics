import streamlit as st
import pandas as pd
from subprocess import call
import plotly.express as px
from datetime import datetime, timedelta

st.header('Youtube Analytics Dashboard')

df = pd.read_csv('streamlit_data.csv')
df['published_at'] = pd.to_datetime(df['published_at'])

with st.sidebar:
   make_call = st.button("Make API Call")
   if make_call:
      call(["python", "youtube_trending_api.py"])
      st.write('API call was made')
   st.write(f"**Note:** Video data ranges from {df['published_at'].min().strftime('%Y-%m-%d')} to {df['published_at'].max().strftime('%Y-%m-%d')}\nVisualizations may not capture all months and years")
   
col1, col2 = st.columns([1, 3])

with col1:
   #Most Popular Trending Categories
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

with col2:
   #Most Popular Trending Cateogries
   fig_trending = px.bar(x = subset['category_title'].value_counts().index, y = subset['category_title'].value_counts(), color_discrete_sequence=["#FF0000"])
   fig_trending.update_layout(title = f"Most Popular Trending Categories {select_time_frame}",
                              xaxis_title = "Category",
                              yaxis_title = "Count"
                              )
   st.plotly_chart(fig_trending, theme="streamlit", use_container_width=True)

