# Activity Monitoring Tool for Program Monitoring
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
from shiny import reactive
from shiny.express import render, input, ui
from shinywidgets import render_plotly

ui.page_opts(window_title="Activity Monitoring Tool", fillable=False)

df_path = Path(__file__).parent.parent / "data/processed/households_coaching_visits_merged.csv"
df23 = pd.read_csv(df_path)

for col in ["startTime_dt", "endTime_dt"]:
    if col in df23.columns:
        df23[col] = pd.to_datetime(df23[col], errors='coerce')

total_households = df23['household_id'].nunique()
total_visits = len(df23)
lowest_region = df23['region_name'].value_counts().idxmin()
lowest_district = df23['district_name'].value_counts().idxmin()

with ui.layout_column_wrap(width=1/4):
    with ui.value_box(showcase=None, theme='primary'):
        ui.h3("Total Households")
        ui.h2(f"{total_households:,}")
    with ui.value_box(showcase=None, theme='primary'):
        ui.h3("Total Visits")
        ui.h2(f"{total_visits:,}")
    with ui.value_box(showcase=None, theme='warning'):
        ui.h3("Lowest Region (Visits)")
        ui.h2(f"{lowest_region}")
    with ui.value_box(showcase=None, theme='warning'):
        ui.h3("Lowest District (Visits)")
        ui.h2(f"{lowest_district}")

with ui.card():
    ui.card_header("Visits by Region (Highlighting Low Performance)")
    @render_plotly
    def plot_region_monitor():
        visits = df23.groupby('region_name').size().reset_index(name='visits')
        visits['highlight'] = np.where(visits['region_name'] == lowest_region, 'Needs Improvement', 'OK')
        fig = px.bar(visits, x='region_name', y='visits', color='highlight',
                    color_discrete_map={'Needs Improvement': 'red', 'OK': 'steelblue'},
                    title='Visits by Region')
        fig.update_layout(xaxis_title='Region', yaxis_title='Number of Visits', plot_bgcolor='rgba(0,0,0,0)')
        return fig

with ui.card():
    ui.card_header("Visits by District (Highlighting Low Performance)")
    @render_plotly
    def plot_district_monitor():
        visits = df23.groupby('district_name').size().reset_index(name='visits')
        visits['highlight'] = np.where(visits['district_name'] == lowest_district, 'Needs Improvement', 'OK')
        fig = px.bar(visits, x='district_name', y='visits', color='highlight',
                    color_discrete_map={'Needs Improvement': 'orange', 'OK': 'seagreen'},
                    title='Visits by District')
        fig.update_layout(xaxis_title='District', yaxis_title='Number of Visits', plot_bgcolor='rgba(0,0,0,0)')
        return fig

with ui.card():
    ui.card_header("Visits by Cluster")
    @render_plotly
    def plot_cluster_monitor():
        visits = df23.groupby('cluster_name').size().reset_index(name='visits')
        fig = px.bar(visits, x='cluster_name', y='visits', color='visits', color_continuous_scale="Purples", title='Visits by Cluster')
        fig.update_layout(xaxis_title='Cluster', yaxis_title='Number of Visits', plot_bgcolor='rgba(0,0,0,0)')
        return fig

with ui.card():
    ui.card_header("Sample Data Table")
    @render.data_frame
    def sample_data():
        return render.DataTable(
            df23.head(100),
            selection_mode='row',
            filters=True
        )
