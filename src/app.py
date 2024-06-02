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

# External stylesheet for Roboto Condensed font
external_stylesheets = ['https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@300;400;700&display=swap', '/assets/custom_styles.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.Div([
    html.Div([
        html.Div([], style={'width': '80%'}),  # Empty 80% column
        
        html.Div([
            html.H3('Anzahl Freitexte', className='header', style={'color': 'white', "marginBottom": "0px", "marginTop": "12px"}),
            html.P(id='respondent-count', style={'fontSize': '20px', 'marginTop': '0px', "marginBottom": "2px", 'color': 'white', 'textAlign': 'right'})
        ], style={'width': '30%', 'padding': '20px', 'border-radius': '10px', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'flex-end', 'alignItems': 'flex-end'})
    ], style={'display': 'flex', 'width': '100%'})
], style={
    'background-color': '#3A4D9F',  # Blue background
    'background-image': 'url(assets/header_feedbackexplorer.png)',
    'background-size': 'cover',
    'background-position': 'center',
    'border-radius': '10px',
    'margin-bottom': '10px',
    'padding': '20px',
    'display': 'flex'
}),

    html.Div([
        html.Div([
            html.H3('Analyse', className='header_menu')
        ], className='box_menu', style={'width': '25%',}),
        
        html.Div([
            html.H3('Treiberanalyse', className='header_menu')
        ], className='box_menu', style={'width': '25%',}),
        
        html.Div([
            html.H3('ChatWithYourFeedback', className='header_menu')
        ], className='box_menu', style={'width': '25%', }),

        html.Div([
            html.H3('Impressum', className='header_menu')
        ], className='box_menu', style={'width': '25%', })
    ], className='container_menu', style={'display': 'flex', 'justify-content': 'space-between'}),
    
    

    html.Div([
        html.Div([
            html.H3('Selektion A auswählen:', className='header'),
            dcc.Dropdown(
                id='main-standort1-filter',
                options=[{'label': name, 'value': name} for name in data['name'].unique()],
                value=[],
                multi=True
            )
        ], className='box', style={'width': '85%'}),

        html.Div([
            html.H3('Selektion B auswählen:', className='header'),
            dcc.Dropdown(
                id='main-standort2-filter',
                options=[{'label': name, 'value': name} for name in data['name'].unique()],
                value=[],
                multi=True
            )
        ], className='box', style={'width': '85%'}),

        html.Div([
            html.H3('Wettbewerber auswählen:', className='header'),
            dcc.Dropdown(
                id='competitor-filter',
                options=[{'label': name, 'value': name} for name in data['name'].unique()],
                value=[],
                multi=True
            )
        ], className='box', style={'width': '85%'}),
    ], className='container'),


    html.Div([
        html.Div([
            html.H3('Status', className='header'),
            dcc.Graph(id='average-satisfaction-bar', config={'displayModeBar': False})
        ], className='box', style={'width': '40%'}),

        html.Div([
            html.H3('Entwicklung', className='header'),
            dcc.Graph(id='satisfaction-trend', config={'displayModeBar': False})
        ], className='box', style={'width': '60%'})
    ], className='container'),

    html.Div([
        html.Div([
            html.H3('Discover Key Topics', className='header_manual'),
            html.P("""Diese Tabelle zeigt die häufigsten Themen in den Kundenbewertungen. 
                   Vergleichen Sie, wie oft diese Themen bei verschiedenen Unternehmen vorkommen, 
                   und identifizieren Sie wichtige Themenbereiche.""",  style={'color': 'white', 'fontSize': '18px' })
        ], className='box_text', style={'flex': '1'}),

        html.Div([
            html.H3('Adjust Threshold Percentage:', className='header dark-text'),
            html.P("""Stellen Sie mit diesem Schieberegler ein, ab welcher Differenz 
                   in Prozentpunkten die Themen farblich hervorgehoben werden. Passen Sie die Sensibilität an, 
                   um relevante Unterschiede sichtbar zu machen.""",  style={'color': 'black', 'fontSize': '14px' }),
            dcc.Slider(
                id='threshold-slider',
                min=0,
                max=20,
                step=1,
                value=10,
                marks={i: f'{i}%' for i in range(0, 31, 5)}
            )
        ], className='box', style={'flex': '1'})
    ], className='container'),

    html.Div([
        dash_table.DataTable(
            id='topic-heatmap',
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '5px', 'font-family': 'Roboto Condensed, sans-serif'},
            style_header={'backgroundColor': '#D9D9D9', 'fontWeight': 'bold', 'font-family': 'Roboto Condensed, sans-serif'},
            style_data={'whiteSpace': 'normal', 'height': 'auto'},
            style_data_conditional=[]
        )
    ], className='box', style={'marginTop': '20px', 'marginBottom': '20px'}),

    html.Div([
        html.Div([
            html.H3('Adjust Rating Threshold', className='header'),
            html.P("""Stellen Sie ein, ab welcher Differenz in den Durchschnittsbewertungen (1 bis 5) die Werte 
                   farblich hervorgehoben werden. Schon kleine Unterschiede können signifikant sein.""",  style={'color': 'black', 'fontSize': '14px' }),
            dcc.Slider(
                id='rating-threshold-slider',
                min=0.1,
                max=1.0,
                step=0.1,
                value=0.2,
                marks={i: f'{i:.1f}' for i in np.arange(0.1, 1.6, 0.1)}
                
            )
        ], className='box', style={'flex': '1'}),

        html.Div([
            html.H3('Understand Review Sentiment', className='header_manual'),
            html.P("""Hier sehen Sie die durchschnittliche Bewertung für jedes Schlüsselthema. 
                   Erkennen Sie, ob ein Thema positiv oder negativ bewertet wurde, und nutzen Sie diese 
                   Erkenntnisse zur Identifikation von Stärken und Schwächen.""", style={'color': 'white', 'fontSize': '18px' })
        ], className='box_text', style={'flex': '1'})
    ], className='container'),

    html.Div([
        dash_table.DataTable(
            id='average-rating-table',
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '5px', 'font-family': 'Roboto Condensed, sans-serif'},
            style_header={'backgroundColor': '#D9D9D9', 'fontWeight': 'bold', 'font-family': 'Roboto Condensed, sans-serif'},
            style_data={'whiteSpace': 'normal', 'height': 'auto'},
            style_data_conditional=[]
        )
    ], className='box', style={'marginTop': '20px', 'marginBottom': '20px'}),

    html.Div([
        html.H3("Deep Dive - Explore Your Data", className='header_manual', style={'textAlign': 'center',  }),
        html.P("""Tauchen Sie tief in die Kundenbewertungen ein und analysieren Sie spezifische Feedbacks. 
               Nutzen Sie die Filter, um nach Themen, Unternehmen, Zeiträumen, Bewertungen und Suchbegriffen zu suchen. 
               Diese Funktion ermöglicht es Ihnen, detaillierte Einblicke zu gewinnen und gezielt auf Kundenfeedback zu reagieren.""", style={'textAlign': 'center', 'color': '#fff', 'fontSize': '18px' }),
    ], className='box_text', style={'marginTop': '20px', 'marginBottom': '0px'} ),


    html.Div([
        html.Div([
            html.H3('Thema:', className='header'),
            dcc.Dropdown(
                id='topic-dropdown',
                options=[{'label': topic, 'value': topic} for topic in topics],
                value=topics[0],
                clearable=False
            )
        ], style={'width': '19%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '0 10px'}),

        html.Div([
            html.H3('Betrieb:', className='header'),
            dcc.Dropdown(
                id='standort-dropdown',
                options=[{'label': name, 'value': name} for name in data['name'].unique()],
                value=data['name'].unique()[0],
                clearable=False
            )
        ], style={'width': '19%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '0 10px'}),

        html.Div([
            html.H3('Zeitspanne', className='header'),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=data['date'].min().date(),
                end_date=data['date'].max().date(),
                display_format='DD.MM.YYYY',
                month_format='DD.MM.YYYY',
                style={'fontSize': '10px'}
            )
        ], style={'width': '19%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '0 10px'}),

        html.Div([
            html.H3('Rating Range:', className='header'),
            dcc.RangeSlider(
                id='review-rating-slider',
                min=1,
                max=5,
                step=1,
                value=[1, 3],
                marks={i: f'{i}' for i in range(1, 6)}
            )
        ], style={'width': '19%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '0 10px'}),

        html.Div([
            html.H3('Suchbegriff:', className='header'),
            dcc.Input(
                id='search-term',
                type='text',
                placeholder='Suchbegriff eingeben'
            )
        ], style={'width': '19%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '0 10px'})
    ], className='box', style={'marginTop': '20px', 'marginBottom': '20px', 'display': 'flex'}),

    html.Div([
        dash_table.DataTable(
            id='filtered-reviews-table',
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '5px', 'font-family': 'Roboto Condensed, sans-serif'},
            style_header={'backgroundColor': 'D9D9D9', 'fontWeight': 'bold', 'font-family': 'Roboto Condensed, sans-serif'},
            style_data={'whiteSpace': 'normal', 'height': 'auto'},
            style_data_conditional=[
                {'if': {'row_index': 'odd'}, 'backgroundColor': '#F5F4EF'},
                {'if': {'row_index': 'even'}, 'backgroundColor': 'white'}
            ]
        )
    ], className='box', style={'marginTop': '20px', 'marginBottom': '20px'})
], className='wrapper')

@app.callback(
    [Output('average-satisfaction-bar', 'figure'),
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
    [Input('main-standort1-filter', 'value'),
     Input('main-standort2-filter', 'value'),
     Input('competitor-filter', 'value'),
     Input('threshold-slider', 'value'),
     Input('rating-threshold-slider', 'value'),
     Input('topic-dropdown', 'value'),
     Input('standort-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('review-rating-slider', 'value'),
     Input('search-term', 'value')]
)
def update_dashboard(main_standort1, main_standort2, competitors, threshold, rating_threshold, selected_topic, selected_standort, start_date, end_date, review_rating, search_term):
    # Combine the main standorte 1 into one group
    if main_standort1:
        main_data1 = data[data['name'].isin(main_standort1)]
        main_data1['name'] = 'Selektion A'
        main_data1['quarter'] = main_data1['date'].dt.to_period('Q')
    else:
        main_data1 = pd.DataFrame(columns=data.columns)

    # Combine the main standorte 2 into one group
    if main_standort2:
        main_data2 = data[data['name'].isin(main_standort2)]
        main_data2['name'] = 'Selektion B'
        main_data2['quarter'] = main_data2['date'].dt.to_period('Q')
    else:
        main_data2 = pd.DataFrame(columns=data.columns)

    # Combine the data for main standorte and competitors
    competitor_data = data[data['name'].isin(competitors)]
    competitor_data['quarter'] = competitor_data['date'].dt.to_period('Q')
    filtered_data = pd.concat([main_data1, main_data2, competitor_data])

    # Ensure all date columns are in datetime format
    filtered_data['date'] = pd.to_datetime(filtered_data['date'])

    # Calculate the overall average satisfaction for each selection
    average_ratings = {}
    colors = {
        'Selektion A': '#b22122',
        'Selektion B': '#141F52'
    }
    color_list = ['#1DC9A4', '#C91D42', '#1A1A1A', '#F9C31F', '#E1DFD0']
    if not main_data1.empty:
        average_ratings['Selektion A'] = round(main_data1['Rating'].mean(), 1)
    if not main_data2.empty:
        average_ratings['Selektion B'] = round(main_data2['Rating'].mean(), 1)
    for idx, competitor in enumerate(competitors):
        competitor_avg_rating = round(filtered_data[filtered_data['name'] == competitor]['Rating'].mean(), 1)
        average_ratings[competitor] = competitor_avg_rating
        colors[competitor] = color_list[idx % len(color_list)]

    # Reverse the order of the selections for the bar chart
    average_ratings = dict(reversed(list(average_ratings.items())))

    # Prepare data for the horizontal bar chart
    bar_chart = go.Figure()
    bar_chart.add_trace(go.Bar(
        x=list(average_ratings.values()),
        y=list(average_ratings.keys()),
        orientation='h',
        marker=dict(color=[colors[key] for key in average_ratings.keys()]),
        text=list(average_ratings.values()),  # Display the average rating on the bars
        textposition='auto'
    ))

    bar_chart.update_layout(
        font=dict(family='Roboto Condensed, sans-serif', size=14),
        xaxis=dict(
            title='Durchschnittliches Rating',
            range=[1, 5]
        ),
        yaxis=dict(
            title=''
        ),
        margin=dict(l=40, r=20, t=20, b=40),  # Adjust margins to remove the title space
        plot_bgcolor='white',  # Set background color to white
        xaxis_showgrid=False,  # Remove grid lines
        yaxis_showgrid=False   # Remove grid lines
    )

    # Calculate the number of respondents
    respondent_count = len(main_data1) if not main_data1.empty else 0
    
    # Create the line chart for overall satisfaction trend
    traces_line = []
    filtered_data['quarter'] = filtered_data['date'].dt.to_period('Q')
    
    # Ensure quarters are sorted in the correct order
    quarters_order = pd.period_range(start='2018Q1', end='2024Q2', freq='Q')
    filtered_data['quarter'] = pd.Categorical(filtered_data['quarter'], categories=quarters_order, ordered=True)
    
    window_size = 4  # Set the window size for the moving average
    
    # Plot the main standort 1 as a single line
    if not main_data1.empty:
        main_trend_data1 = main_data1.groupby('quarter', observed=True)['Rating'].mean().reindex(quarters_order).reset_index()
        main_trend_data1.columns = ['quarter', 'Rating']  # Renaming columns after reindex
        main_trend_data1['Rating'] = main_trend_data1['Rating'].interpolate(method='linear')  # Interpolating missing values
        main_trend_data1['Moving_Avg'] = main_trend_data1['Rating'].rolling(window=window_size, min_periods=1).mean()  # Calculate the moving average
        traces_line.append(go.Scatter(
            x=main_trend_data1['quarter'].astype(str),
            y=main_trend_data1['Moving_Avg'],
            mode='lines+markers',
            line_shape='spline',
            name='Selektion A',
            line=dict(color=colors['Selektion A'])
        ))

    # Plot the main standort 2 as a single line
    if not main_data2.empty:
        main_trend_data2 = main_data2.groupby('quarter', observed=True)['Rating'].mean().reindex(quarters_order).reset_index()
        main_trend_data2.columns = ['quarter', 'Rating']  # Renaming columns after reindex
        main_trend_data2['Rating'] = main_trend_data2['Rating'].interpolate(method='linear')  # Interpolating missing values
        main_trend_data2['Moving_Avg'] = main_trend_data2['Rating'].rolling(window=window_size, min_periods=1).mean()  # Calculate the moving average
        traces_line.append(go.Scatter(
            x=main_trend_data2['quarter'].astype(str),
            y=main_trend_data2['Moving_Avg'],
            mode='lines+markers',
            line_shape='spline',
            name='Selektion B',
            line=dict(color=colors['Selektion B'])
        ))

    # Plot competitors as separate lines
    for i, name in enumerate(competitors):
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
            line=dict(color=colors[name])
        ))

    figure_line = {
    'data': traces_line,
    'layout': go.Layout(
        font=dict(family='Roboto Condensed, sans-serif', size=14),
        yaxis={
            'title': 'Durchschnittliches Rating',
            'range': [1, 5],
            'tickmode': 'array',
            'tickvals': [1, 2, 3, 4, 5]
        },
        xaxis={'title': 'Quartal'},
        legend=dict(
            orientation="h",  # This makes the legend horizontal
            x=0.5,            # Position the legend in the center
            y=1.15,           # Position the legend above the chart
            xanchor='center', # Anchor the center of the legend box to the x coordinate
            yanchor='bottom', # Anchor the bottom of the legend box to the y coordinate
            font=dict(
                size=15        # Increase the font size of the legend
            )
        ),
        margin=dict(
            l=60, r=20, t=60, b=60  # Adjust margins to provide space for the y-axis labels and the legend
        ),
        
    )
}
    
    # Create the data for the topic heatmap/datatable
    topic_data = []
    for topic in topics:
        row = {'Topic': topic}
        total_count = filtered_data[topic].sum()
        overall_total = len(filtered_data)
        row['Total'] = round((total_count / overall_total * 100), 1) if overall_total > 0 else 0
        main_count1 = main_data1[topic].sum()
        main_total1 = len(main_data1)
        row['Selektion A'] = round((main_count1 / main_total1 * 100), 1) if main_total1 > 0 else 0
        main_count2 = main_data2[topic].sum()
        main_total2 = len(main_data2)
        row['Selektion B'] = round((main_count2 / main_total2 * 100), 1) if main_total2 > 0 else 0
        for standort in competitors:
            count = filtered_data[filtered_data['name'] == standort][topic].sum()
            total = len(filtered_data[filtered_data['name'] == standort])
            row[standort] = round((count / total * 100), 1) if total > 0 else 0
        topic_data.append(row)
    
    # Define the columns for the DataTable
    columns = [{'name': 'Topic', 'id': 'Topic'}, {'name': 'Total', 'id': 'Total'}, {'name': 'Selektion A', 'id': 'Selektion A'}, {'name': 'Selektion B', 'id': 'Selektion B'}] + [{'name': name, 'id': name} for name in competitors]
    
    # Sort topic_data by 'Total' column in descending order
    topic_data = sorted(topic_data, key=lambda x: x['Total'], reverse=True)
    
    # Create style_data_conditional for conditional formatting
    style_data_conditional = []
    for i, row in enumerate(topic_data):
        total_value = row['Total']
        row_styles = {
            'if': {'row_index': i},
            'backgroundColor': '#F5F4EF' if i % 2 == 1 else 'white'
        }
        style_data_conditional.append(row_styles)
        for standort in competitors + ['Selektion A', 'Selektion B']:
            if row[standort] > total_value + threshold:
                style_data_conditional.append({
                    'if': {
                        'filter_query': '{{{}}} = {}'.format(standort, row[standort]),
                        'column_id': standort,
                        'row_index': i
                    },
                    'backgroundColor': 'green',
                    'color': 'white'
                })
            elif row[standort] < total_value - threshold:
                style_data_conditional.append({
                    'if': {
                        'filter_query': '{{{}}} = {}'.format(standort, row[standort]),
                        'column_id': standort,
                        'row_index': i
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
        main_avg_rating1 = main_data1[main_data1[topic] == 1]['Rating'].mean()
        row['Selektion A'] = round(main_avg_rating1, 1) if not np.isnan(main_avg_rating1) else 'N/A'
        main_avg_rating2 = main_data2[main_data2[topic] == 1]['Rating'].mean()
        row['Selektion B'] = round(main_avg_rating2, 1) if not np.isnan(main_avg_rating2) else 'N/A'
        for standort in competitors:
            filtered_reviews = filtered_data[(filtered_data['name'] == standort) & (filtered_data[topic] == 1)]
            avg_rating = filtered_reviews['Rating'].mean()
            row[standort] = round(avg_rating, 1) if not np.isnan(avg_rating) else 'N/A'
        average_rating_data.append(row)
    
    # Define the columns for the average rating DataTable
    average_rating_columns = [{'name': 'Topic', 'id': 'Topic'}, {'name': 'Total', 'id': 'Total'}, {'name': 'Selektion A', 'id': 'Selektion A'}, {'name': 'Selektion B', 'id': 'Selektion B'}] + [{'name': name, 'id': name} for name in competitors]
    
    # Sort average_rating_data by 'Total' column in descending order
    average_rating_data = sorted(average_rating_data, key=lambda x: x['Total'] if x['Total'] != 'N/A' else float('-inf'), reverse=True)
    
    # Create style_data_conditional for conditional formatting for average rating table
    rating_style_data_conditional = []
    for i, row in enumerate(average_rating_data):
        total_value = row['Total']
        row_styles = {
            'if': {'row_index': i},
            'backgroundColor': '#F5F4EF' if i % 2 == 1 else 'white'
        }
        rating_style_data_conditional.append(row_styles)
        for standort in competitors + ['Selektion A', 'Selektion B']:
            if row[standort] != 'N/A':
                if row[standort] > total_value + rating_threshold:
                    rating_style_data_conditional.append({
                        'if': {
                            'filter_query': '{{{}}} = {}'.format(standort, row[standort]),
                            'column_id': standort,
                            'row_index': i
                        },
                        'backgroundColor': 'green',
                        'color': 'white'
                    })
                elif row[standort] < total_value - rating_threshold:
                    rating_style_data_conditional.append({
                        'if': {
                            'filter_query': '{{{}}} = {}'.format(standort, row[standort]),
                            'column_id': standort,
                            'row_index': i
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
        (data['Rating'] >= review_rating[0]) &
        (data['Rating'] <= review_rating[1])
    ]

    if search_term:
        reviews_filtered = reviews_filtered[reviews_filtered['Review'].str.contains(search_term, case=False, na=False)]
    
    # Create the data for the filtered reviews table
    reviews_data = reviews_filtered[['date', 'Review', 'Rating', selected_topic]].to_dict('records')
    
    # Define the columns for the filtered reviews table
    reviews_columns = [{'name': col, 'id': col} for col in ['date', 'Review', 'Rating', selected_topic]]
    
    return (bar_chart, str(respondent_count), figure_line, topic_data, columns, style_data_conditional, 
            average_rating_data, average_rating_columns, rating_style_data_conditional, reviews_data, reviews_columns)

if __name__ == '__main__':
    app.run_server(debug=True)
