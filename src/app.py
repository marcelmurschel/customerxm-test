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
app.css.append_css({"external_url": "/assets/custom_styles.css"})

app.layout = html.Div([

    html.Div([
        html.Img(src='assets/vcx_kunde.png', style={'width': '100%', 'border-radius': '10px'})
    ]),

    html.Div([
        html.Div([
            html.Div('Standort auswählen:', style={'fontFamily': 'Roboto Condensed', 'fontWeight': 'bold', 'fontSize': '20px', 'position': 'absolute', 'top': '20px', 'left': '20px', }),
            dcc.Dropdown(
                id='standort-filter',
                options=[{'label': name, 'value': name} for name in data['name'].unique()],
                value=data['name'].unique().tolist(),
                multi=True
            )
        ], style={'width': '85%', 'display': 'inline-block', 'backgroundColor': 'white', 'borderRadius': '10px', 'border': '1px solid #ccc', 'padding': '40px 10px 10px 10px', 'marginRight': '20px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'position': 'relative'}),

        html.Div([
            html.Div('Anzahl Interviews', style={'fontFamily': 'Roboto Condensed', 'fontWeight': 'bold', 'fontSize': '20px', 'position': 'absolute', 'top': '20px', 'left': '20px'}),
            html.P(id='respondent-count', style={'fontSize': '24px', 'fontFamily': 'Roboto Condensed', 'position': 'absolute', 'top': '60px', 'left': '20px'})
        ], style={'width': '25%', 'display': 'inline-block', 'backgroundColor': 'white', 'borderRadius': '10px', 'border': '1px solid #ccc', 'padding': '40px 10px 10px 10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'position': 'relative'})
    ], style={'display': 'flex', 'marginTop': '20px'}),

    html.Div([
        html.Div([
            html.Div('Status', style={
                'fontFamily': 'Roboto Condensed', 
                'fontWeight': 'bold', 
                'fontSize': '24px',  # Increased font size
                'position': 'absolute', 
                'top': '20px',  # Adjusted to align to the top
                'left': '20px',  # Adjusted to align to the left
            }),
            html.Div(id='average-rating', style={
                'fontFamily': 'Roboto Condensed', 
                'fontSize': '30px',  # Large font size
                'textAlign': 'left',
                'marginBottom': '10px',
                'position': 'relative',
                'top': '10px',  # Adjust this as necessary
                'left': '10px',  # Adjust this as necessary
            }),
            dcc.Graph(id='average-satisfaction-bar', config={'displayModeBar': False})
        ], style={
            'width': '30%', 
            'display': 'inline-block', 
            'backgroundColor': 'white', 
            'borderRadius': '10px', 
            'border': '1px solid #ccc', 
            'padding': '35px 10px 10px 10px',  # Adjusted padding to make space for the title and average rating
            'marginRight': '20px', 
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 
            'position': 'relative'
        }),

        html.Div([
            html.Div('Entwicklung', style={'fontFamily': 'Roboto Condensed', 'fontWeight': 'bold', 'fontSize': '20px', 'position': 'absolute', 'top': '20px', 'left': '20px'}),
            dcc.Graph(id='satisfaction-trend', config={'displayModeBar': False})
        ], style={'width': '70%', 'display': 'inline-block', 'backgroundColor': 'white', 'borderRadius': '10px', 'border': '1px solid #ccc', 'padding': '40px 10px 10px 10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'position': 'relative'})
    ], style={'display': 'flex', 'marginTop': '20px'}),
            
   html.Div([
    html.Div([
        html.H2('Discover Key Topics', style={'fontFamily': 'Roboto Condensed', 'fontWeight': 'bold', 'fontSize': '20px', 'color': 'white', 'marginBottom': '5px'}),
        html.P('In der Tabelle unten sehen Sie die Hauptthemen aus den Kundenbewertungen. Identifizieren Sie die wichtigsten Anliegen Ihrer Kunden und verfolgen Sie Unterschiede über Standorte / Wettbewerber hinweg.', style={'fontFamily': 'Roboto Condensed', 'fontSize': '14px', 'color': 'white'})
    ], style={
        'flex': '1', 
        'backgroundColor': '#141F52', 
        'borderRadius': '10px', 
        'border': '1px solid #ccc', 
        'padding': '10px', 
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'height': 'auto'
    }),

    html.Div([
        html.Label('Adjust Threshold Percentage:', style={'fontFamily': 'Roboto Condensed', 'fontWeight': 'bold', 'fontSize': '20px', 'color': 'black', 'marginBottom': '5px'}),
        dcc.Slider(
            id='threshold-slider',
            min=0,
            max=20,
            step=1,
            value=10,
            marks={i: f'{i}%' for i in range(0, 31, 5)}
        )
    ], style={
        'flex': '1', 
        'backgroundColor': 'white', 
        'borderRadius': '10px', 
        'border': '1px solid #ccc', 
        'padding': '10px', 
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'height': 'auto'
    })
], style={
    'display': 'flex', 
    'alignItems': 'stretch', 
    'gap': '20px', 
    'marginTop': '20px'
}),


    html.Div([
        dash_table.DataTable(
            id='topic-heatmap',
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '5px', 'fontFamily': 'Roboto Condensed'},
            style_header={
                'backgroundColor': '#D9D9D9',
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
        html.Label('Adjust Rating Threshold:', style={'fontFamily': 'Roboto Condensed', 'fontWeight': 'bold', 'fontSize': '20px', 'color': 'white', 'marginBottom': '5px'}),
        dcc.Slider(
            id='rating-threshold-slider',
            min=0.1,
            max=1.0,
            step=0.1,
            value=0.2,
            marks={i: f'{i:.1f}' for i in np.arange(0.1, 1.6, 0.1)}
        )
    ], style={
        'flex': '1', 
        'backgroundColor': 'white', 
        'borderRadius': '10px', 
        'border': '1px solid #ccc', 
        'padding': '10px', 
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'height': 'auto'
    }),

    html.Div([
        html.H2('Understand Review Sentiment', style={'fontFamily': 'Roboto Condensed', 'fontWeight': 'bold', 'fontSize': '20px', 'color': 'white', 'marginBottom': '5px'}),
        html.P('Erfassen Sie die Konnotation bestimmter Themen. Erfahren Sie ob diese positiv oder negativ von den Kunden bewertet werden.', style={'fontFamily': 'Roboto Condensed', 'fontSize': '14px', 'color': 'white'})      
    ], style={
        'flex': '1', 
        'backgroundColor': '#141F52', 
        'borderRadius': '10px', 
        'border': '1px solid #ccc', 
        'padding': '10px', 
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'height': 'auto',
        'color': 'white'
    }),
], style={
    'display': 'flex', 
    'alignItems': 'stretch', 
    'gap': '20px', 
    'marginTop': '20px'
}),



    html.Div([
        dash_table.DataTable(
            id='average-rating-table',
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '5px', 'fontFamily': 'Roboto Condensed'},
            style_header={
                'backgroundColor': '#D9D9D9',
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
            html.Label('Thema:', style={'fontFamily': 'Roboto Condensed', 'fontWeight': 'bold', 'fontSize': '16px'}),
            dcc.Dropdown(
                id='topic-dropdown',
                options=[{'label': topic, 'value': topic} for topic in topics],
                value=topics[0],
                clearable=False
            )
        ], style={'width': '19%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '0 10px'}),

        html.Div([
            html.Label('Betrieb:', style={'fontFamily': 'Roboto Condensed', 'fontWeight': 'bold', 'fontSize': '16px'}),
            dcc.Dropdown(
                id='standort-dropdown',
                options=[{'label': name, 'value': name} for name in data['name'].unique()],
                value=data['name'].unique()[0],
                clearable=False
            )
        ], style={'width': '19%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '0 10px'}),

        html.Div([
            html.Label('Zeitspanne', style={'fontFamily': 'Roboto Condensed', 'fontWeight': 'bold', 'fontSize': '16px'}),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=data['date'].min().date(),
                end_date=data['date'].max().date(),
                display_format='DD.MM.YYYY',
                month_format='DD.MM.YYYY',
                style={'fontSize': '10px', 'fontFamily': 'Roboto Condensed'}  # Adjust the font size and font family here
            )
        ], style={'width': '19%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '0 10px'}),
    
    

        html.Div([
            html.Label('Rating Threshold:', style={'fontFamily': 'Roboto Condensed', 'fontWeight': 'bold', 'fontSize': '16px'}),
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
            html.Label('Suchbegriff:', style={'fontFamily': 'Roboto Condensed', 'fontWeight': 'bold', 'fontSize': '16px'}),
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
                'backgroundColor': 'D9D9D9',
                'fontWeight': 'bold'
            },
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#F5F4EF'
                },
                {
                    'if': {'row_index': 'even'},
                    'backgroundColor': 'white'
                }
            ]
        )
    ], style={'marginTop': '20px', 'marginBottom': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'border': '1px solid #ccc', 'padding': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
    
], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '20px', 'border': '1px solid #ccc', 'boxShadow': '2px 2px 12px #aaa', 'backgroundColor': '#f7f7f7', 'fontFamily': 'Roboto Condensed'})

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
     Output('filtered-reviews-table', 'columns'),
     Output('average-rating', 'children')],
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
    
    # Create the bar chart for average satisfaction with trend arrows
    rating_counts = filtered_data['Rating'].value_counts().sort_index()
    total_ratings = rating_counts.sum()
    percentage_shares = (rating_counts / total_ratings) * 100
    
    bar_chart = go.Figure(data=[
        go.Bar(
            name='Ratings',
            y=rating_counts.index,
            x=rating_counts.values,
            marker_color=['#F4D03F', '#F4D03F', '#F4D03F', '#F4D03F', '#F4D03F'],
            orientation='h'
        )
    ])

    annotations = []
    for rating, percentage in zip(rating_counts.index, percentage_shares):
        annotations.append(dict(
            x=rating_counts[rating] + 300,  # position near the bar
            y=rating,
            text=f'{percentage:.0f}%',  # formatted percentage value
            showarrow=False,
            font=dict(color='black', size=18, family='Roboto Condensed', )
        ))

    # Add arrows behind the bars for each rating
    filtered_data['quarter'] = filtered_data['date'].dt.to_period('Q')
    quarters_order = pd.period_range(start='2018Q1', end='2024Q2', freq='Q')
    filtered_data['quarter'] = pd.Categorical(filtered_data['quarter'], categories=quarters_order, ordered=True)

    offset = 600  # Offset to move the arrows to the right

    for rating in rating_counts.index:
        rating_data = filtered_data[filtered_data['Rating'] == rating].groupby('quarter').size().reindex(quarters_order, fill_value=0)
        total_reviews = filtered_data.groupby('quarter').size().reindex(quarters_order, fill_value=0)
        
        # Calculate the share of each rating
        rating_share = (rating_data / total_reviews) * 100
        
        last_two_quarters_share = rating_share[-2:].mean()
        previous_two_quarters_share = rating_share[-4:-2].mean()
        
        if last_two_quarters_share > previous_two_quarters_share:
            arrow = "▲"
            color = "green"
        else:
            arrow = "▼"
            color = "red"
        
        bar_chart.add_trace(go.Scatter(
            x=[rating_counts[rating] + offset],
            y=[rating],
            text=[arrow],
            mode="text",
            textfont=dict(color=color, size=20),
            showlegend=False,
            xaxis='x',
            yaxis='y',
            name='',
        ))

    bar_chart.update_layout(
        annotations=annotations,
        xaxis=dict(
            title='',
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False
        ),
        yaxis=dict(
            title='',
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=True  # Keep the tick labels if you want to see the ratings
        ),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        barmode='overlay',  # Overlay mode to ensure scatter is behind the bars
        bargap=0.25,
    )

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
    for i, row in enumerate(topic_data):
        total_value = row['Total']
        row_styles = {
            'if': {'row_index': i},
            'backgroundColor': '#F5F4EF' if i % 2 == 1 else 'white'
        }
        style_data_conditional.append(row_styles)
        for standort in selected_standorte:
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
    for i, row in enumerate(average_rating_data):
        total_value = row['Total']
        row_styles = {
            'if': {'row_index': i},
            'backgroundColor': '#F5F4EF' if i % 2 == 1 else 'white'
        }
        rating_style_data_conditional.append(row_styles)
        for standort in selected_standorte:
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
        (data['Rating'] < review_rating)
    ]

    if search_term:
        reviews_filtered = reviews_filtered[reviews_filtered['Review'].str.contains(search_term, case=False, na=False)]
    
    # Create the data for the filtered reviews table
    reviews_data = reviews_filtered[['date', 'Review', 'Rating', selected_topic]].to_dict('records')
    
    # Define the columns for the filtered reviews table
    reviews_columns = [{'name': col, 'id': col} for col in ['date', 'Review', 'Rating', selected_topic]]
    
    return (bar_chart, str(respondent_count), figure_line, topic_data, columns, style_data_conditional, 
            average_rating_data, average_rating_columns, rating_style_data_conditional, reviews_data, reviews_columns, 
            f'Average Rating: {average_satisfaction:.1f}')


if __name__ == '__main__':
    app.run_server(debug=True)
