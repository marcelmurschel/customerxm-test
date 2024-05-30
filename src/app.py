import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np

# Load the dataset
data = pd.read_csv("google_reviews_test.csv")

data['date'] = pd.to_datetime(data['date'])

# List of topics
topics = ['Kundenservice', 'Beratung', 'Freundlichkeit', 'Fahrzeugübergabe', 'Zubehör', 'Werkstattservice', 'Preis-Leistungs-Verhältnis', 'Sauberkeit', 'Zuverlässigkeit', 'Terminvereinbarung', 'Lieferzeit', 'Garantieabwicklung', 'Reparaturqualität', 'Auswahl']

# Initialize the app
app = dash.Dash(__name__)
server = app.server

# External stylesheet for Roboto Condensed font
app.css.append_css({"external_url": "https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@300;400;700&display=swap"})

app.layout = html.Div([

    html.Div([
        html.Img(src='assets/vcx_kunde.png', style={'width': '100%', 'border-radius': '10px'})
    ]),

    html.Div([
        html.Div([
            html.Label('Standort auswählen:', style={'fontFamily': 'Roboto Condensed'}),
            dcc.Dropdown(
                id='standort-filter',
                options=[{'label': name, 'value': name} for name in data['name'].unique()],
                value=data['name'].unique().tolist(),
                multi=True
            )
        ], style={'width': '85%', 'display': 'inline-block'}),

        html.Div([
            html.H2('Anzahl Interviews', style={'fontFamily': 'Roboto Condensed'}),
            html.P(id='respondent-count', style={'fontSize': '24px', 'fontFamily': 'Roboto Condensed'})
        ], style={'width': '15%', 'display': 'inline-block', 'verticalAlign': 'top'})
    ], style={'display': 'flex', 'marginTop': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'border': '1px solid #ccc', 'padding': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),

    html.Div([
        html.Div([
            dcc.Graph(id='average-satisfaction-gauge')
        ], style={'width': '30%', 'display': 'inline-block', 'backgroundColor': 'white', 'borderRadius': '10px', 'border': '1px solid #ccc', 'padding': '10px', 'marginRight': '40px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),

        html.Div([
            dcc.Graph(id='satisfaction-trend')
        ], style={'width': '70%', 'display': 'inline-block', 'backgroundColor': 'white', 'borderRadius': '10px', 'border': '1px solid #ccc', 'padding': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
    ], style={'display': 'flex', 'marginTop': '20px'}),
    
    html.Div([
        html.Label('Adjust Threshold Percentage:', style={'fontFamily': 'Roboto Condensed'}),
        dcc.Slider(
            id='threshold-slider',
            min=0,
            max=30,
            step=1,
            value=10,
            marks={i: f'{i}%' for i in range(0, 31, 5)}
        )
    ], style={'marginTop': '20px', 'marginBottom': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'border': '1px solid #ccc', 'padding': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
    
    html.Div([
        dash_table.DataTable(
            id='topic-heatmap',
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '5px', 'fontFamily': 'Roboto Condensed'},
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold'
            },
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto'
            },
            style_data_conditional=[]  # This will be populated dynamically
        )
    ], style={'marginTop': '20px', 'marginBottom': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'border': '1px solid #ccc', 'padding': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
    
    html.Div([
        html.Label('Adjust Rating Threshold:', style={'fontFamily': 'Roboto Condensed'}),
        dcc.Slider(
            id='rating-threshold-slider',
            min=0.1,
            max=1.5,
            step=0.1,
            value=1,
            marks={i: f'{i:.1f}' for i in np.arange(0.1, 1.6, 0.1)}
        )
    ], style={'marginTop': '75px', 'marginBottom': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'border': '1px solid #ccc', 'padding': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),

    html.Div([
        dash_table.DataTable(
            id='average-rating-table',
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '5px', 'fontFamily': 'Roboto Condensed'},
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold'
            },
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto'
            },
            style_data_conditional=[]  # This will be populated dynamically
        )
    ], style={'marginTop': '20px', 'marginBottom': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'border': '1px solid #ccc', 'padding': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
    
    html.Div([
        html.Div([
            html.Label('Thema:', style={'fontFamily': 'Roboto Condensed'}),
            dcc.Dropdown(
                id='topic-dropdown',
                options=[{'label': topic, 'value': topic} for topic in topics],
                value=topics[0],
                clearable=False
            )
        ], style={'width': '19%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '0 10px'}),

        html.Div([
            html.Label('Betrieb:', style={'fontFamily': 'Roboto Condensed'}),
            dcc.Dropdown(
                id='standort-dropdown',
                options=[{'label': name, 'value': name} for name in data['name'].unique()],
                value=data['name'].unique()[0],
                clearable=False
            )
        ], style={'width': '19%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '0 10px'}),

        html.Div([
            html.Label('Zeitspanne', style={'fontFamily': 'Roboto Condensed'}),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=data['date'].min().date(),
                end_date=data['date'].max().date(),
                display_format='YYYY-MM-DD'
            )
        ], style={'width': '19%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '0 10px'}),

        html.Div([
            html.Label('Rating Threshold:', style={'fontFamily': 'Roboto Condensed'}),
            dcc.Slider(
                id='review-rating-slider',
                min=1,
                max=5,
                step=1,
                value=5,
                marks={i: f'<{i}' for i in range(2, 6)}
            )
        ], style={'width': '19%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '0 10px'}),

        html.Div([
            html.Label('Suchbegriff:', style={'fontFamily': 'Roboto Condensed'}),
            dcc.Input(
                id='search-term',
                type='text',
                placeholder='Search term'
            )
        ], style={'width': '19%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '0 10px'})
    ], style={'marginTop': '75px', 'marginBottom': '20px', 'display': 'flex', 'backgroundColor': 'white', 'borderRadius': '10px', 'border': '1px solid #ccc', 'padding': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),

    html.Div([
        dash_table.DataTable(
            id='filtered-reviews-table',
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '5px', 'fontFamily': 'Roboto Condensed'},
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold'
            },
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto'
            }
        )
    ], style={'marginTop': '20px', 'marginBottom': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'border': '1px solid #ccc', 'padding': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
    
], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '20px', 'border': '1px solid #ccc', 'boxShadow': '2px 2px 12px #aaa', 'backgroundColor': '#e0e0e0', 'fontFamily': 'Roboto Condensed'})

@app.callback(
    [Output('average-satisfaction-gauge', 'figure'),
     Output('respondent-count', 'children'),
     Output('satisfaction-trend', 'figure'),
     Output('topic-heatmap', 'data'),
     Output('topic-heatmap', 'columns'),
     Output('topic-heatmap', 'style_data_conditional'),
     Output('average-rating-table', 'data'),
     Output('average-rating-table', 'columns'),
     Output('average-rating-table', 'style_data_conditional'),
     Output('filtered-reviews-table', 'data'),
     Output('filtered-reviews-table', 'columns')],
    [Input('standort-filter', 'value'),
     Input('threshold-slider', 'value'),
     Input('rating-threshold-slider', 'value'),
     Input('topic-dropdown', 'value'),
     Input('standort-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('review-rating-slider', 'value'),
     Input('search-term', 'value')]
)
def update_dashboard(selected_standorte, threshold, rating_threshold, selected_topic, selected_standort, start_date, end_date, review_rating, search_term):
    filtered_data = data[data['name'].isin(selected_standorte)].copy()
    
    # Calculate the overall average satisfaction
    average_satisfaction = filtered_data['Rating'].mean()
    
    # Calculate the number of respondents
    respondent_count = len(filtered_data)
    
    # Define the colors list
    colors = ['#b22122', '#141F52', '#1DC9A4', '#C91D42', '#F97A1F', '#1A1A1A']
    
    # Create the gauge chart for average satisfaction
    fig_gauge = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=average_satisfaction,
        mode="gauge+number",
        title={'text': "CSAT"},
        gauge={
            'axis': {'range': [1, 5]},
            'steps': [
                {'range': [1, 2], 'color': "#b22122"},
                {'range': [2, 3], 'color': "grey"},
                {'range': [3, 5], 'color': "#1DC9A4"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': average_satisfaction}
        }
    ))

    # Create the line chart for overall satisfaction trend
    traces_line = []
    filtered_data['quarter'] = filtered_data['date'].dt.to_period('Q')
    
    # Ensure quarters are sorted in the correct order
    quarters_order = pd.period_range(start='2018Q1', end='2024Q2', freq='Q')
    filtered_data['quarter'] = pd.Categorical(filtered_data['quarter'], categories=quarters_order, ordered=True)
    
    window_size = 4  # Set the window size for the moving average
    
    for i, name in enumerate(selected_standorte):
        name_data = filtered_data[filtered_data['name'] == name]
        trend_data = name_data.groupby('quarter', observed=True)['Rating'].mean().reindex(quarters_order).reset_index()
        trend_data.columns = ['quarter', 'Rating']  # Renaming columns after reindex
        trend_data['Rating'] = trend_data['Rating'].interpolate(method='linear')  # Interpolating missing values
        trend_data['Moving_Avg'] = trend_data['Rating'].rolling(window=window_size, min_periods=1).mean()  # Calculate the moving average
        traces_line.append(go.Scatter(
            x=trend_data['quarter'].astype(str),
            y=trend_data['Moving_Avg'],
            mode='lines+markers',
            line_shape='spline',
            name=name,
            line=dict(color=colors[i % len(colors)])
        ))

    figure_line = {
    'data': traces_line,
    'layout': go.Layout(
        title='Durchschnittliche Zufriedenheit pro Quartal (Moving Average)',
        yaxis={'title': 'Durchschnittliche Zufriedenheit', 'range': [1, 5]},
        xaxis={'title': 'Quartal'},
        legend=dict(
            orientation="h",  # This makes the legend horizontal
            x=0.5,            # Position the legend in the center
            y=-0.35,           # Position the legend below the chart
            xanchor='center',  # Anchor the center of the legend box to the x coordinate
            yanchor='top'     # Anchor the top of the legend box to the y coordinate
        )
    )
}
    
    # Create the data for the topic heatmap/datatable
    topic_data = []
    for topic in topics:
        row = {'Topic': topic}
        total_count = filtered_data[topic].sum()
        overall_total = len(filtered_data)
        row['Total'] = round((total_count / overall_total * 100), 1) if overall_total > 0 else 0
        for standort in selected_standorte:
            count = filtered_data[filtered_data['name'] == standort][topic].sum()
            total = len(filtered_data[filtered_data['name'] == standort])
            row[standort] = round((count / total * 100), 1) if total > 0 else 0
        topic_data.append(row)
    
    # Define the columns for the DataTable
    columns = [{'name': 'Topic', 'id': 'Topic'}, {'name': 'Total', 'id': 'Total'}] + [{'name': name, 'id': name} for name in selected_standorte]
    
    # Sort topic_data by 'Total' column in descending order
    topic_data = sorted(topic_data, key=lambda x: x['Total'], reverse=True)
    
    # Create style_data_conditional for conditional formatting
    style_data_conditional = []
    for row in topic_data:
        total_value = row['Total']
        for standort in selected_standorte:
            if row[standort] > total_value + threshold:
                style_data_conditional.append({
                    'if': {
                        'filter_query': '{{{}}} = {}'.format(standort, row[standort]),
                        'column_id': standort
                    },
                    'backgroundColor': 'green',
                    'color': 'white'
                })
            elif row[standort] < total_value - threshold:
                style_data_conditional.append({
                    'if': {
                        'filter_query': '{{{}}} = {}'.format(standort, row[standort]),
                        'column_id': standort
                    },
                    'backgroundColor': 'red',
                    'color': 'white'
                })

    # Calculate the average rating per topic and location
    average_rating_data = []
    for topic in topics:
        row = {'Topic': topic}
        total_avg_rating = filtered_data[filtered_data[topic] == 1]['Rating'].mean()
        row['Total'] = round(total_avg_rating, 1) if not np.isnan(total_avg_rating) else 'N/A'
        for standort in selected_standorte:
            filtered_reviews = filtered_data[(filtered_data['name'] == standort) & (filtered_data[topic] == 1)]
            avg_rating = filtered_reviews['Rating'].mean()
            row[standort] = round(avg_rating, 1) if not np.isnan(avg_rating) else 'N/A'
        average_rating_data.append(row)
    
    # Define the columns for the average rating DataTable
    average_rating_columns = [{'name': 'Topic', 'id': 'Topic'}, {'name': 'Total', 'id': 'Total'}] + [{'name': name, 'id': name} for name in selected_standorte]
    
    # Sort average_rating_data by 'Total' column in descending order
    average_rating_data = sorted(average_rating_data, key=lambda x: x['Total'] if x['Total'] != 'N/A' else float('-inf'), reverse=True)
    
    # Create style_data_conditional for conditional formatting for average rating table
    rating_style_data_conditional = []
    for row in average_rating_data:
        total_value = row['Total']
        for standort in selected_standorte:
            if row[standort] != 'N/A':
                if row[standort] > total_value + rating_threshold:
                    rating_style_data_conditional.append({
                        'if': {
                            'filter_query': '{{{}}} = {}'.format(standort, row[standort]),
                            'column_id': standort
                        },
                        'backgroundColor': 'green',
                        'color': 'white'
                    })
                elif row[standort] < total_value - rating_threshold:
                    rating_style_data_conditional.append({
                        'if': {
                            'filter_query': '{{{}}} = {}'.format(standort, row[standort]),
                            'column_id': standort
                        },
                        'backgroundColor': 'red',
                        'color': 'white'
                    })
    
    # Filter reviews based on the user's selection
    reviews_filtered = data[
        (data['name'] == selected_standort) &
        (data['date'] >= pd.to_datetime(start_date)) &
        (data['date'] <= pd.to_datetime(end_date)) &
        (data[selected_topic] == 1) &
        (data['Rating'] < review_rating)
    ]

    if search_term:
        reviews_filtered = reviews_filtered[reviews_filtered['Review'].str.contains(search_term, case=False, na=False)]
    
    # Create the data for the filtered reviews table
    reviews_data = reviews_filtered[['date', 'Review', 'Rating', selected_topic]].to_dict('records')
    
    # Define the columns for the filtered reviews table
    reviews_columns = [{'name': col, 'id': col} for col in ['date', 'Review', 'Rating', selected_topic]]
    
    return (fig_gauge, str(respondent_count), figure_line, topic_data, columns, style_data_conditional, 
            average_rating_data, average_rating_columns, rating_style_data_conditional, reviews_data, reviews_columns)

if __name__ == '__main__':
    app.run_server(debug=True)
