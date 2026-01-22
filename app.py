# RTV Interview Dashboard: df23 Plotly Shiny App
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
from shiny import reactive
from shiny.express import render, input, ui
from shinywidgets import render_plotly

ui.page_opts(window_title="Monitoring tool", fillable=False)

# Load df23
df_path = Path(__file__).parent / "data/processed/households_coaching_visits_merged.csv"
df23 = pd.read_csv(df_path)

# If datetime columns exist, parse them
for col in ["startTime_dt", "endTime_dt"]:
    if col in df23.columns:
        df23[col] = pd.to_datetime(df23[col], errors='coerce')


# Value box metrics (guaranteed to have data)
total_households = df23['household_id'].nunique()
total_visits = len(df23)
total_regions = df23['region_name'].nunique()
total_districts = df23['district_name'].nunique()

with ui.layout_column_wrap(width=1/4):
    with ui.value_box(showcase=None, theme='primary'):
        ui.h3("Total Households")
        ui.h2(f"{total_households:,}")
    with ui.value_box(showcase=None, theme='primary'):
        ui.h3("Total Visits")
        ui.h2(f"{total_visits:,}")
    with ui.value_box(showcase=None, theme='primary'):
        ui.h3("Regions Covered")
        ui.h2(f"{total_regions:,}")
    with ui.value_box(showcase=None, theme='primary'):
        ui.h3("Districts Covered")
        ui.h2(f"{total_districts:,}")

# --- Visualizations ---

with ui.card():
    ui.card_header("Visits per Region")
    @render_plotly
    def plot_visits_per_region():
        visits = df23.groupby('region_name').size().reset_index(name='visits')
        fig = px.bar(visits, x='region_name', y='visits', color='visits', color_continuous_scale="Blues", title='Visits per Region')
        fig.update_layout(xaxis_title='Region', yaxis_title='Number of Visits', plot_bgcolor='rgba(0,0,0,0)')
        return fig

with ui.card():
    ui.card_header("Visits per District")
    @render_plotly
    def plot_visits_per_district():
        visits = df23.groupby('district_name').size().reset_index(name='visits')
        fig = px.bar(visits, x='district_name', y='visits', color='visits', color_continuous_scale="Greens", title='Visits per District')
        fig.update_layout(xaxis_title='District', yaxis_title='Number of Visits', plot_bgcolor='rgba(0,0,0,0)')
        return fig

with ui.card():
    ui.card_header("Visits per Cluster")
    @render_plotly
    def plot_visits_per_cluster():
        visits = df23.groupby('cluster_name').size().reset_index(name='visits')
        fig = px.bar(visits, x='cluster_name', y='visits', color='visits', color_continuous_scale="Purples", title='Visits per Cluster')
        fig.update_layout(xaxis_title='Cluster', yaxis_title='Number of Visits', plot_bgcolor='rgba(0,0,0,0)')
        return fig

with ui.card():
    ui.card_header("Visits per Village")
    @render_plotly
    def plot_visits_per_village():
        visits = df23.groupby('village_name').size().reset_index(name='visits')
        fig = px.bar(visits, x='village_name', y='visits', color='visits', color_continuous_scale="Oranges", title='Visits per Village')
        fig.update_layout(xaxis_title='Village', yaxis_title='Number of Visits', plot_bgcolor='rgba(0,0,0,0)')
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
