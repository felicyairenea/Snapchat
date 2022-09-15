import pandas as pd
import altair as alt
from pyodide.http import open_url


url = "https://raw.githubusercontent.com/felicyairenea/Snapchat/main/IN-ADH-90-days.csv"
df = pd.read_csv(open_url(url))
df = df.dropna(axis=0)

alt.data_transformers.disable_max_rows()

pts = alt.selection(type = 'single', encodings=['x'])
scales = alt.selection_interval(bind='scales')
interval_x = alt.selection_interval(encodings=['x'], empty='none')
#multi_mouseover = alt.selection_multi(on='mouseover', toggle=False, empty='none')

cost = alt.Chart(df).mark_bar(color='burlywood').encode(
    alt.X('day(Date):N', title='Day of week'),
    alt.Y('average(cost_usd)', title='Average Cost (in USD)'),
    color='month(Date):N'
).properties(
    width=300,
    height=300
).add_selection(
    pts
)

clicks = alt.Chart(df).mark_line().encode(
    alt.X('day(Date):N', title='Day of week'),
    alt.Y('average(clicks)', title='Average Clicks'),
    color='month(Date):N'
).properties(
    width=200,
    height=300
)

impressions = alt.Chart(df).mark_point().encode(
    alt.X('day(Date):N', title='Day of week'),
    alt.Y('average(impressions)', title='Average Impressions'),
    color='month(Date):N'
).properties(
    width=200,
    height=300
)

line = alt.Chart(df).mark_line(color='lightgrey').encode(
    alt.Y('average(d7_retention)'), 
    alt.X('cost_usd', title='The Ads Cost (usd)'),
    tooltip=['cost_usd','average(d7_retention)','impressions','clicks']
).properties(
    width= 1000,
    height = 400
)

bar = alt.Chart(df).mark_bar(color='coral').encode(
    alt.X('Date:T'),
    alt.Y('impressions:Q'),
    color=alt.condition(interval_x, 'count()', alt.value('lightgray'))
).add_selection(
    interval_x
)

rect = alt.Chart(df).mark_bar().encode(
    alt.X('impressions:Q', bin=True),
    alt.Y('clicks:Q', bin=True),
    color=alt.condition(pts, 'clicks:Q', alt.value('lightgray'))
)

alt.vconcat(cost | line + line.mark_circle(color='pink'), 
(impressions + clicks).add_selection(
    scales
)| rect | bar)
#alt.vconcat(cost, (impressions + clicks).add_selection(
#    scales
#)) | alt.vconcat(line + line.mark_circle(color='pink'), rect) | bar 




