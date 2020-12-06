#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 23:06:50 2020

@author: simon
"""

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from plotly.tools import mpl_to_plotly
import dash_table

from loan_analytics.main import *
from loan_analytics.Helper import *
from loan_analytics.Loan import Loan
from loan_analytics.LoanPortfolio import LoanPortfolio
from loan_analytics.LoanImpacts import LoanImpacts
from loan_analytics.Test_Loans import *

import pandas as pd
import numpy as np
# from matplotlib import pyplot as plt


#%%

# Index
# Page 1: Individual Loan
# Page 2: Loan Portfolio
# Page 3: Contribution Impact


app = dash.Dash(__name__, suppress_callback_exceptions=True)


layout = dict(
    title_align_style = 'center'
    )

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

#%%

index_page = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Loan Calculation", style={'text-align': layout.get('title_align_style')})
            )
        ),
        html.Div([
            dcc.Link('Go to Individual Loan Analysis', href='/page-1'),
            html.Br(),
            dcc.Link('Go to Loan Portfolio Analysis', href='/page-2'),
            html.Br(),
            dcc.Link('Go to Contribution Impact Analysis', href='/page-3')
        ])
    ],
    id="main-container",
    style={"display": "flex", "flex-direction": "column"},
    fluid=True)



page_1_layout = html.Div([
    html.H1('Individual Loan Analysis', style={'text-align': layout.get('title_align_style')}),
    
    html.Br(),
    dcc.Link('Go to Loan Portfolio Analysis', href='/page-2'),
    html.Br(),
    dcc.Link('Go to Contribution Impact Analysis', href='/page-3'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
    html.Br(),
    
    dbc.Row(
        children = 
            [
            dbc.Col(
                children = 
                    [
                        html.Div('Principal'),
                        dcc.Input(
                            id='page-1-loan_principal',
                            placeholder='Principal',
                            type='number',
                            min=1,
                            value=1000
                        )
                    ]
                ),
            dbc.Col(
                children = 
                    [
                        html.Div('Annual Interest Rate'),
                        dcc.Input(
                            id='page-1-interest',
                            placeholder='Annual Interest (%)',
                            type='number',
                            min=0,
                            value=12
                        )
                    ]
                ),
            dbc.Col(
                children = 
                    [
                        html.Div('Monthly Payment'),
                        dcc.Input(
                            id='page-1-payment',
                            placeholder='Monthly Payment',
                            type='number',
                            min=1,
                            value=100
                        )
                    ]
                ),
            dbc.Col(
                children = 
                    [
                        html.Div('Monthly Extra Payment'),
                        dcc.Input(
                            id='page-1-extra-payment',
                            placeholder='Monthly Extra Payment',
                            type='number',
                            min=0,
                            value=0
                        )
                    ]
                )
            ]
            ),
    dbc.Button(id = 'submit-loan-1',n_clicks = 0, children = "Submit", outline=True, color="primary", className="mr-1"),
    
    html.Div(id='page-1-parameter-check', children = ""),
    
    dbc.Row(
        children = 
        [
            dbc.Col([dcc.Graph(id = 'bar_plot_loan_cashflow')]),
            dbc.Col([dcc.Graph(id = 'bar_plot_loan_balance_and_interest')])     
            ]
        ),
    
    dbc.Col(
                children = 
                    [
                        html.Div('Please enter the month for the pie chart below'),
                        dcc.Dropdown(
                            id='page-1-pie-month',
                            options=[
                                {'label': month, 'value': month} for month in range(1,2)],
                            placeholder='Month you want to see',
                            value=1
                        )
                    ],
                width = 3
                ),
    dbc.Button(id = 'submit-loan-2',n_clicks = 0, children = "Update Pie Chart", outline=True, color="primary", className="mr-1"),
    
    dcc.Graph(id = 'pie_loan'),
    
    html.Br(),
    html.H3('Payback Schedule Details'),
    
    dash_table.DataTable(id='loan-table')
])

@app.callback([dash.dependencies.Output('page-1-parameter-check', 'children'),
               dash.dependencies.Output('bar_plot_loan_cashflow', 'figure'),
               dash.dependencies.Output('bar_plot_loan_balance_and_interest', 'figure'),
               dash.dependencies.Output('page-1-pie-month', 'options'),
               dash.dependencies.Output('pie_loan', 'figure'),
               dash.dependencies.Output('loan-table', 'columns'),
               dash.dependencies.Output('loan-table', 'data')],
              
              [Input(component_id='submit-loan-1',component_property='n_clicks'),
               Input(component_id='submit-loan-2',component_property='n_clicks')],
              
              [dash.dependencies.State('page-1-loan_principal', 'value'),
               dash.dependencies.State('page-1-interest', 'value'),
               dash.dependencies.State('page-1-payment', 'value'),
               dash.dependencies.State('page-1-extra-payment', 'value'),
               dash.dependencies.State('page-1-pie-month', 'value')])
def loan_func(n_clicks_1,n_clicks_2, principal, rate, payment, extra_payment, i):
    # See if the parameters are valid
    test_result = test_loan(principal, rate, payment, extra_payment)
    
    if test_result[0] != 1:
        # Use parameters below to make plot if parameters are not valid
        principal = 1
        rate = 0
        payment = 1
        extra_payment = 0
    
    # Start calculation
    current_loan = Loan(principal, rate, payment, extra_payment)
    current_loan.compute_schedule()
    current_loan_schedule = current_loan.return_loan_schedule()
    
    bar_plot_loan_cashflow = Helper.bar_plot_loan_cashflow(current_loan_schedule)
    
    bar_plot_loan_balance_and_interest = Helper.bar_plot_loan_balance_and_interest(current_loan_schedule)
    
    pie_loan = Helper.pie_loan(current_loan_schedule, i)
    
    return str(test_result[1]), bar_plot_loan_cashflow, bar_plot_loan_balance_and_interest,[{'label': month, 'value': month} for month in range(1,current_loan_schedule.shape[0] + 1)], pie_loan, [{"name": i, "id": i} for i in current_loan_schedule.columns], current_loan_schedule.to_dict('records')

#%%

page_2_layout = html.Div([
    html.H1('Loan Portfolio Analysis', style={'text-align': layout.get('title_align_style')}),
    dcc.Link('Go to Individual Loan Analysis', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Contribution Impact Analysis', href='/page-3'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
    
    html.H3('Select number of stocks in your portfolio'),
    
    dcc.RadioItems(
        id = 'loan-count',
        options=[{'label': num, 'value': num} for num in [2,3]],
        value=3
    ),
    
    html.H3('If you have two loans, please ignore all parameters for loan C'),
    html.Br(),
    
    dbc.Row(
        children = 
            [
            dbc.Col(
                children = 
                    [
                        html.Div('Principal (Loan A)'),
                        dcc.Input(
                            id='page-2-loan-principal-a',
                            placeholder='Principal (Loan A)',
                            type='number',
                            min=1,
                            value=1000
                        )
                    ]
                ),
            dbc.Col(
                children = 
                    [
                        html.Div('Annual Interest Rate (Loan A)'),
                        dcc.Input(
                            id='page-2-interest-a',
                            placeholder='Annual Interest (%) (Loan A)',
                            type='number',
                            min=0,
                            value=12
                        )
                    ]
                ),
            dbc.Col(
                children = 
                    [
                        html.Div('Monthly Payment (Loan A)'),
                        dcc.Input(
                            id='page-2-payment-a',
                            placeholder='Monthly Payment (Loan A)',
                            type='number',
                            min=1,
                            value=100
                        )
                    ]
                ),
            dbc.Col(
                children = 
                    [
                        html.Div('Monthly Extra Payment (Loan A)'),
                        dcc.Input(
                            id='page-2-extra-payment-a',
                            placeholder='Monthly Extra Payment (Loan A)',
                            type='number',
                            min=0,
                            value=0
                        )
                    ]
                )
            ]
        ),
    html.Div(id='page-2-parameter-check-a', children = ""),
    
    html.Br(),
    
    dbc.Row(
        children = 
            [
            dbc.Col(
                children = 
                    [
                        html.Div('Principal (Loan B)'),
                        dcc.Input(
                            id='page-2-loan-principal-b',
                            placeholder='Principal (Loan B)',
                            type='number',
                            min=1,
                            value=1000
                        )
                    ]
                ),
            dbc.Col(
                children = 
                    [
                        html.Div('Annual Interest Rate (Loan B)'),
                        dcc.Input(
                            id='page-2-interest-b',
                            placeholder='Annual Interest (%) (Loan B)',
                            type='number',
                            min=0,
                            value=12
                        )
                    ]
                ),
            dbc.Col(
                children = 
                    [
                        html.Div('Monthly Payment (Loan B)'),
                        dcc.Input(
                            id='page-2-payment-b',
                            placeholder='Monthly Payment (Loan B)',
                            type='number',
                            min=1,
                            value=100
                        )
                    ]
                ),
            dbc.Col(
                children = 
                    [
                        html.Div('Monthly Extra Payment (Loan B)'),
                        dcc.Input(
                            id='page-2-extra-payment-b',
                            placeholder='Monthly Extra Payment (Loan B)',
                            type='number',
                            min=0,
                            value=0
                        )
                    ]
                )
            ]
        ),
    
    html.Div(id='page-2-parameter-check-b', children = ""),
    
    html.Br(),
    
    dbc.Row(
        children = 
            [
            dbc.Col(
                children = 
                    [
                        html.Div('Principal (Loan C)'),
                        dcc.Input(
                            id='page-2-loan-principal-c',
                            placeholder='Principal (Loan C)',
                            type='number',
                            min=0.02,
                            value=1000
                        )
                    ]
                ),
            dbc.Col(
                children = 
                    [
                        html.Div('Annual Interest Rate (Loan C)'),
                        dcc.Input(
                            id='page-2-interest-c',
                            placeholder='Annual Interest (%) (Loan C)',
                            type='number',
                            min=0,
                            value=12
                        )
                    ]
                ),
            dbc.Col(
                children = 
                    [
                        html.Div('Monthly Payment (Loan C)'),
                        dcc.Input(
                            id='page-2-payment-c',
                            placeholder='Monthly Payment (Loan C)',
                            type='number',
                            min=0.02,
                            value=100
                        )
                    ]
                ),
            dbc.Col(
                children = 
                    [
                        html.Div('Monthly Extra Payment (Loan C)'),
                        dcc.Input(
                            id='page-2-extra-payment-c',
                            placeholder='Monthly Extra Payment (Loan C)',
                            type='number',
                            min=0,
                            value=0
                        )
                    ]
                )
            ]
        ),
    
    html.Div(id='page-2-parameter-check-c', children = ""),
    
    dbc.Button(id = 'submit-portfolio-1',n_clicks = 0, children = "Submit", outline=True, color="primary", className="mr-1"),
    
    dbc.Row(
        children = 
        [
            dbc.Col([dcc.Graph(id = 'bar_plot_portfolio_cashflow')]),
            dbc.Col([dcc.Graph(id = 'bar_plot_portfolio_balance_and_interest')])     
            ]
        ),
    
    dbc.Col(
                children = 
                    [
                        html.H3('Please select the month for the pie chart below, and click Update Pie Chart button'),
                        dcc.Dropdown(
                            id='page-2-pie-month',
                            options=[
                                {'label': month, 'value': month} for month in range(1,2)],
                            placeholder='Month you want to see',
                            value=1
                        )
                    ],
                width = 3
                ),
    dbc.Button(id = 'submit-portfolio-2',n_clicks = 0, children = "Update Pie Chart", outline=True, color="primary", className="mr-1"),
    
    dcc.Graph(id = 'pie_portfolio'),
    
    html.Br(),
    html.H3('Payback Schedule Details'),
    
    dash_table.DataTable(id='portfolio-table')
    
])

@app.callback([dash.dependencies.Output('page-2-parameter-check-a', 'children'),
               dash.dependencies.Output('page-2-parameter-check-b', 'children'),
               dash.dependencies.Output('page-2-parameter-check-c', 'children'),
               
               dash.dependencies.Output('page-2-loan-principal-c', 'disabled'),
               dash.dependencies.Output('page-2-interest-c', 'disabled'),
               dash.dependencies.Output('page-2-payment-c', 'disabled'),
               dash.dependencies.Output('page-2-extra-payment-c', 'disabled'),
               
               dash.dependencies.Output('page-2-pie-month', 'options'),
               
               dash.dependencies.Output('bar_plot_portfolio_cashflow', 'figure'),
               dash.dependencies.Output('bar_plot_portfolio_balance_and_interest', 'figure'),
               dash.dependencies.Output('pie_portfolio', 'figure'),
               
               dash.dependencies.Output('portfolio-table', 'columns'),
               dash.dependencies.Output('portfolio-table', 'data')],
              
              [dash.dependencies.Input('submit-portfolio-1', 'n_clicks'),
               dash.dependencies.Input('submit-portfolio-2', 'n_clicks'),
               dash.dependencies.Input('loan-count', 'value')],
              
              [dash.dependencies.State('page-2-loan-principal-a', 'value'),
               dash.dependencies.State('page-2-interest-a', 'value'),
               dash.dependencies.State('page-2-payment-a', 'value'),
               dash.dependencies.State('page-2-extra-payment-a', 'value'),
               
               dash.dependencies.State('page-2-loan-principal-b', 'value'),
               dash.dependencies.State('page-2-interest-b', 'value'),
               dash.dependencies.State('page-2-payment-b', 'value'),
               dash.dependencies.State('page-2-extra-payment-b', 'value'),
               
               dash.dependencies.State('page-2-loan-principal-c', 'value'),
               dash.dependencies.State('page-2-interest-c', 'value'),
               dash.dependencies.State('page-2-payment-c', 'value'),
               dash.dependencies.State('page-2-extra-payment-c', 'value'),
               
               dash.dependencies.State('page-2-pie-month', 'value')])
def portfolio_func(n_clicks_1, n_clicks_2, loan_count, principal_a, rate_a, payment_a, extra_payment_a, principal_b, rate_b, payment_b, extra_payment_b,principal_c, rate_c, payment_c, extra_payment_c, i):
    #%% Test each loan
    # Test for loan A
    test_result_a = test_loan(principal_a, rate_a, payment_a, extra_payment_a)
    
    if test_result_a[0] != 1:
        # Use parameters below to make plot if parameters are not valid
        principal_a = 1
        rate_a = 0
        payment_a = 1
        extra_payment_a = 0
    
    # Start calculation
    loan_a = Loan(principal_a, rate_a, payment_a, extra_payment_a)
    loan_a.compute_schedule()
    loan_a_schedule = loan_a.return_loan_schedule()
    
    # Test for loan B
    test_result_b = test_loan(principal_b, rate_b, payment_b, extra_payment_b)
    
    if test_result_b[0] != 1:
        # Use parameters below to make plot if parameters are not valid
        principal_b = 1
        rate_b = 0
        payment_b = 1
        extra_payment_b = 0
        
    # Start calculation
    loan_b = Loan(principal_b, rate_b, payment_b, extra_payment_b)
    loan_b.compute_schedule()
    loan_b_schedule = loan_b.return_loan_schedule()
    
    # Test for loan C
    test_result_c = test_loan(principal_c, rate_c, payment_c, extra_payment_c)
    
    if test_result_c[0] != 1:
        # Use parameters below to make plot if parameters are not valid
        principal_c = 1
        rate_c = 0
        payment_c = 1
        extra_payment_c = 0
    
    # Start calculation
    loan_c = Loan(principal_c, rate_c, payment_c, extra_payment_c)
    loan_c.compute_schedule()
    loan_c_schedule = loan_c.return_loan_schedule()
    
    #%% Calculate loan matrix
    
    loan_a_schedule['Loan_ID'] = 'A'
    loan_b_schedule['Loan_ID'] = 'B'
    loan_c_schedule['Loan_ID'] = 'C'

    schedule_by_loan = loan_a_schedule.append(loan_b_schedule).append(loan_c_schedule).reset_index().drop('index', axis=1)
    
    #%% Calculate portfolio matrix
    loans = LoanPortfolio()
    
    disable_factor = False
    
    if loan_count == 2:
        disable_factor = True
        
# =============================================================================
#         # Need to calculate laon C matrix again, in case user have changed defalut settings
#         loan_c = Loan(0.02, 0, 0.02, 0)
#         loan_c.compute_schedule()
#         loan_c_schedule = loan_c.return_loan_schedule()
#         
#         #%% Calculate loan matrix
#         
#         loan_a_schedule['Loan_ID'] = 'A'
#         loan_b_schedule['Loan_ID'] = 'B'
#         loan_c_schedule['Loan_ID'] = 'C'
# =============================================================================
    
        schedule_by_loan = loan_a_schedule.append(loan_b_schedule).reset_index().drop('index', axis=1)
        
        if test_result_a[0] == 1 and test_result_b[0] == 1:
            loans = add_and_compute_schedule(principal_a, rate_a, payment_a, extra_payment_a)
            loans= add_and_compute_schedule(principal_b, rate_b, payment_b, extra_payment_b)
            
        else:
            loans = add_and_compute_schedule(1, 0, 1, 0)
            loans= add_and_compute_schedule(1, 0, 1, 0)
            
    else:
        if test_result_a[0] == 1 and test_result_b[0] == 1 and test_result_c[0] == 1:
            loans = add_and_compute_schedule(principal_a, rate_a, payment_a, extra_payment_a)
            loans= add_and_compute_schedule(principal_b, rate_b, payment_b, extra_payment_b)
            loans= add_and_compute_schedule(principal_c, rate_c, payment_c, extra_payment_c)
            
        else:
            loans = add_and_compute_schedule(1, 0, 1, 0)
            loans= add_and_compute_schedule(1, 0, 1, 0)
            loans= add_and_compute_schedule(1, 0, 1, 0)
            
    loans.aggregate()
    
    portfolio_schedule = loans.return_portfolio_schedule()
    portfolio_schedule['Accumulated_Interest'] = round(portfolio_schedule['Accumulated_Interest'],2)
    
    #%% make plots
    bar_plot_portfolio_cashflow = Helper.bar_plot_portfolio_cashflow(schedule_by_loan)
    
    bar_plot_portfolio_balance_and_interest = Helper.bar_plot_portfolio_balance_and_interest(schedule_by_loan, portfolio_schedule)
    
    pie_portfolio = Helper.pie_portfolio(schedule_by_loan, i)
    #%%
    if n_clicks_1 != -1 or n_clicks_2 != -1:
        loans.reset()
    
    return str(test_result_a[1]), str(test_result_b[1]), str(test_result_c[1]), disable_factor, disable_factor, disable_factor, disable_factor, [{'label': month, 'value': month} for month in range(1,portfolio_schedule.shape[0] + 1)], bar_plot_portfolio_cashflow, bar_plot_portfolio_balance_and_interest, pie_portfolio, [{"name": i, "id": i} for i in portfolio_schedule.columns], portfolio_schedule.to_dict('records')


#%%
page_3_layout = html.Div([
    html.H1('Contribution Impact Analysis', style={'text-align': layout.get('title_align_style')}),
    dcc.Link('Go to Individual Loan Analysis', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Loan Portfolio Analysis', href='/page-2'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
    html.Br(),
    dbc.Row(
        children = 
            [
            dbc.Col(
                children = 
                    [
                        html.Div('Principal'),
                        dcc.Input(
                            id='page-3-loan_principal',
                            placeholder='Principal',
                            type='number',
                            min=1,
                            value=1000
                        )
                    ]
                ),
            dbc.Col(
                children = 
                    [
                        html.Div('Annual Interest Rate'),
                        dcc.Input(
                            id='page-3-interest',
                            placeholder='Annual Interest (%)',
                            type='number',
                            min=1,
                            value=12
                        )
                    ]
                ),
            dbc.Col(
                children = 
                    [
                        html.Div('Monthly Payment'),
                        dcc.Input(
                            id='page-3-payment',
                            placeholder='Monthly Payment',
                            type='number',
                            min=1,
                            value=100
                        )
                    ]
                ),
            dbc.Col(
                children = 
                    [
                        html.Div('Monthly Extra Payment'),
                        dcc.Input(
                            id='page-3-extra-payment',
                            placeholder='Monthly Extra Payment',
                            type='number',
                            min=0,
                            value=0
                        )
                    ]
                ),
            dbc.Col(
                children = 
                    [
                        html.Div('Monthly contribution from A'),
                        dcc.Input(
                            id='page-3-contribution-a',
                            placeholder='Enter Amount',
                            type='number',
                            min=0,
                            value=100
                        )
                    ]
                ),
            dbc.Col(
                children = 
                    [
                        html.Div('Monthly contribution from B'),
                        dcc.Input(
                            id='page-3-contribution-b',
                            placeholder='Enter Amount',
                            type='number',
                            min=0,
                            value=50
                        )
                    ]
                ),
            dbc.Col(
                children = 
                    [
                        html.Div('Monthly contribution from C'),
                        dcc.Input(
                            id='page-3-contribution-c',
                            placeholder='Enter Amount',
                            type='number',
                            min=0,
                            value=10
                        )
                    ]
                )
            ]
            ),
    dbc.Button(id = 'submit-impact',n_clicks = 0, children = "Submit", outline=True, color="primary", className="mr-1"),
    
    html.H3('Note: If there is only two contributors, please enter 0 for contributor C'),
    
    html.Div(id='page-3-parameter-check', children = ""),
    
    dbc.Row(
        children = 
        [
            dbc.Col([dcc.Graph(id = 'bar_plot_duration_interest')]),
            dbc.Col([dcc.Graph(id = 'pie_interest')]),
            dbc.Col([dcc.Graph(id = 'pie_duration')])     
        ]
    ),
    
    html.Br(),
    html.H3('Contribution Impact Details'),
    
    dash_table.DataTable(id='impact-table')
])

@app.callback([dash.dependencies.Output('page-3-parameter-check', 'children'),
               dash.dependencies.Output('bar_plot_duration_interest', 'figure'),
               dash.dependencies.Output('pie_interest', 'figure'),
               dash.dependencies.Output('pie_duration', 'figure'),
               dash.dependencies.Output('impact-table', 'columns'),
               dash.dependencies.Output('impact-table', 'data')],
              
              [dash.dependencies.Input('submit-impact', 'n_clicks')],
              
              [dash.dependencies.State('page-3-loan_principal', 'value'),
               dash.dependencies.State('page-3-interest', 'value'),
               dash.dependencies.State('page-3-payment', 'value'),
               dash.dependencies.State('page-3-extra-payment', 'value'),
               dash.dependencies.State('page-3-contribution-a', 'value'),
               dash.dependencies.State('page-3-contribution-b', 'value'),
               dash.dependencies.State('page-3-contribution-c', 'value')])
def impact_func(n_clicks, principal, rate, payment, extra_payment, a, b ,c):
    # See if the parameters are valid
    test_result = test_loan(principal, rate, payment, extra_payment)
    
    if test_result[0] != 1:
        # Use parameters below to make plot if parameters are not valid
        principal = 1
        rate = 0
        payment = 1
        extra_payment = 0
    
    # Start calculation
    impact_df = LoanImpacts(principal, rate, payment, extra_payment, [a,b,c]).compute_impacts()
    impact_df['Case'] = ['All Help','No Help','A Quit','B Quit','C Quit']
    
    impact_df_interest = impact_df.loc[:,['Case','Interest_Paid']]
    impact_df_duration = impact_df.loc[:,['Case','Duration']]

    #%% Make plots
    bar_plot_duration_interest = Helper.bar_plot_duration_interest(impact_df)
    
    pie_interest = Helper.pie_interest(impact_df)
    
    pie_duration = Helper.pie_duration(impact_df)
    
    #%% Make table
    cols = impact_df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    impact_df_adjusted = impact_df[cols]
    
    return str(test_result[1]), bar_plot_duration_interest, pie_interest, pie_duration,[{"name": i, "id": i} for i in impact_df_adjusted.columns], impact_df_adjusted.to_dict('records')

#%%
# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here
    


#%%

# Main
if __name__ == "__main__":
    app.run_server(debug=True)
    
    
    
    
    
    
    
    