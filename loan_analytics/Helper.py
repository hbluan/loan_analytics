from prettytable import PrettyTable
import matplotlib.pyplot as plt
import plotly.io as pio
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import decimal


class Helper:
    """ Helper class for printing and plotting of loan schedules.
    """
    @staticmethod
    def display(value, digits=2):
        """ Return a displayable value with a specified number of digits.
        :param value: value to display
        :param digits: number of digits right of the decimal place
        :return: formatted displayable value
        """
        value = float(value)
        return '%.{}f'.format(digits) % value

    #%% Plots for individual loan
    @staticmethod
    def bar_plot_loan_cashflow(schedule_individual, width=800, height=400):
        
        schedule_individual_flow = schedule_individual.loc[:,['Month','Applied_Principal','Applied_Interest']]
        schedule_individual_cashflow_unpivot = pd.melt(schedule_individual_flow, id_vars=['Month'], var_name='type', value_name='value')
        
        barchart = px.bar(
            data_frame= schedule_individual_cashflow_unpivot,
            x="Month",
            y="value",
            color="type",               # differentiate color of marks
            opacity=0.9,                  # set opacity of markers (from 0 to 1)
            orientation="v",              # 'v','h': orientation of the marks
            barmode='relative',           # in 'overlay' mode, bars are top of one another.
                                          # in 'group' mode, bars are placed beside each other.
                                          # in 'relative' mode, bars are stacked above (+) or below (-) zero.
            #----------------------------------------------------------------------------------------------
            # facet_row='caste',          # assign marks to subplots in the vertical direction
            # facet_col='caste',          # assigns marks to subplots in the horizontal direction
            # facet_col_wrap=2,           # maximum number of subplot columns. Do not set facet_row!
        
            color_discrete_map={"Applied_Principal": "royalblue" ,"Applied_Interest":"red"},
            #----------------------------------------------------------------------------------------------
            # text='value',            # values appear in figure as text labels
            # hover_name='value',   # values appear in bold in the hover tooltip
            # hover_data=['value'],    # values appear as extra data in the hover tooltip
            # custom_data=['value'],     # invisible values that are extra data to be used in Dash callbacks or widgets
        
            labels={"Month":"Month",
                    "value":"Monthly Payment",
                    "type": "Category",
                    "Applied_Principal":"Applied Principal",
                    'Applied_Interest':'Applied Interest'},           # map the labels of the figure
            title='Individual Loan Schedule: Cashflow Split', # figure title
            width=width,                   # figure width in pixels
            height=height,                   # figure height in pixels
            template='gridon'            # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
        
        )
        
        return barchart

    @staticmethod
    def bar_plot_loan_balance_and_interest(schedule_individual, height=400, width=800):
        schedule_individual_balance = schedule_individual.loc[:,['Month','Begin_Principal','Accumulated_Interest']]
        schedule_individual_balance_unpivot = pd.melt(schedule_individual_balance, id_vars=['Month'], var_name='type', value_name='value')
        
        # Create figure with secondary y-axis
        subfig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Define first plot:
        barchart = px.bar(
            data_frame= schedule_individual_balance_unpivot[schedule_individual_balance_unpivot['type'] == 'Begin_Principal'],
            x="Month",
            y="value",
            color="type",               # differentiate color of marks
            opacity=0.9,                  # set opacity of markers (from 0 to 1)
            orientation="v",              # 'v','h': orientation of the marks
            barmode='relative',           # in 'overlay' mode, bars are top of one another.
                                          # in 'group' mode, bars are placed beside each other.
                                          # in 'relative' mode, bars are stacked above (+) or below (-) zero.
            #----------------------------------------------------------------------------------------------
            # facet_row='caste',          # assign marks to subplots in the vertical direction
            # facet_col='caste',          # assigns marks to subplots in the horizontal direction
            # facet_col_wrap=2,           # maximum number of subplot columns. Do not set facet_row!
        
            color_discrete_map={"Begin_Principal": "royalblue"},
            #----------------------------------------------------------------------------------------------
            # text='value',            # values appear in figure as text labels
            # hover_name='value',   # values appear in bold in the hover tooltip
            # hover_data=['value'],    # values appear as extra data in the hover tooltip
            # custom_data=['value'],     # invisible values that are extra data to be used in Dash callbacks or widgets
        
            labels={"Month":"Month",
                    "value":"Remaining Principal"},           # map the labels of the figure
            title= 'Individual Loan Schedule: Remaining Balance and Accumulated Interest', # figure title
            width=width,                   # figure width in pixels
            height=height,                   # figure height in pixels
            template='gridon'            # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
        
        )
        
        # Define the second chart
        
        linechart = px.line(
            data_frame= schedule_individual_balance_unpivot[schedule_individual_balance_unpivot['type'] == 'Accumulated_Interest'],
            x="Month", 
            y="value",
            color = 'type',
            labels={"Month":"Month",
                    "value":"Accumulated Interest"},        
            color_discrete_map={"Accumulated_Interest": "red"})
        
        
        
        # create two independent figures with px.line each containing data from multiple columns
        #fig = px.line(df, y=df.filter(regex="Linear").columns, render_mode="webgl",)
        #fig2 = px.line(df, y=df.filter(regex="Log").columns, render_mode="webgl",)
        
        linechart.update_traces(yaxis="y2")
        
        subfig.add_traces(barchart.data + linechart.data)
        subfig.layout.xaxis.title="Month"
        subfig.layout.yaxis.title="Remaining Principal"
        subfig.layout.yaxis.color="royalblue"
        subfig.layout.yaxis2.type="linear"
        subfig.layout.yaxis2.color="red"
        subfig.layout.yaxis2.title="Accumulated Interest"
        # recoloring is necessary otherwise lines from fig und fig2 would share each color
        # e.g. Linear-, Log- = blue; Linear+, Log+ = red... we don't want this
        # subfig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))
        subfig.update_layout(height=height, width=width, title_text="Individual Loan Schedule: Remaining Balance and Accumulated Interest")
        
        return subfig

    @staticmethod
    def pie_loan(schedule_individual, i, height=400, width=400):
        schedule_individual_pie = schedule_individual.loc[:,['Month','Applied_Principal','Applied_Interest']].loc[i].to_frame().T
        schedule_individual_pie_unpivot = pd.melt(schedule_individual_pie, id_vars=['Month'], var_name='type', value_name='value')
        
        fig = px.pie(schedule_individual_pie_unpivot, 
             values='value', 
             names='type', 
             title='Loan Payment Snapshot: Month #{}'.format(i)          
             )
        fig.update_layout(height=height, width=width)
        
        return fig

    #%% Plots for loan portfolio
    
    # schedule_by_loan = pd.concat([loan a, loan b], axis=1)
    
    @staticmethod
    def bar_plot_portfolio_cashflow(schedule_by_loan, width = 800, height = 400):
        schedule_by_loan_flow = schedule_by_loan.loc[:,['Month','Applied_Principal','Applied_Interest','Loan_ID']]
        schedule_by_loan_flow_unpivot = pd.melt(schedule_by_loan_flow, id_vars=['Month','Loan_ID'], var_name='type', value_name='value')
        schedule_by_loan_flow_unpivot['type_by_loan'] = schedule_by_loan_flow_unpivot['type'] + ' (Loan '+ schedule_by_loan_flow_unpivot['Loan_ID']+')'
        
        barchart = px.bar(
            data_frame= schedule_by_loan_flow_unpivot,
            x="Month",
            y="value",
            color='type_by_loan',               # differentiate color of marks
            opacity=0.9,                  # set opacity of markers (from 0 to 1)
            orientation="v",              # 'v','h': orientation of the marks
            barmode='relative',           # in 'overlay' mode, bars are top of one another.
                                          # in 'group' mode, bars are placed beside each other.
                                          # in 'relative' mode, bars are stacked above (+) or below (-) zero.
            #----------------------------------------------------------------------------------------------
            # facet_row='caste',          # assign marks to subplots in the vertical direction
            # facet_col='caste',          # assigns marks to subplots in the horizontal direction
            # facet_col_wrap=2,           # maximum number of subplot columns. Do not set facet_row!
        
            color_discrete_map={"Applied_Principal (Loan A)": "royalblue",
                                "Applied_Principal (Loan B)": "darkorange",
                                "Applied_Principal (Loan C)": "darkorchid",
                                "Applied_Interest (Loan A)": "red",
                                "Applied_Interest (Loan B)": "darkgreen",
                                "Applied_Interest (Loan C)": "deepskyblue"},
            #----------------------------------------------------------------------------------------------
            # text='value',            # values appear in figure as text labels
            # hover_name='value',   # values appear in bold in the hover tooltip
            # hover_data=['value'],    # values appear as extra data in the hover tooltip
            # custom_data=['value'],     # invisible values that are extra data to be used in Dash callbacks or widgets
        
            labels={"Month":"Month",
                    "value":"Monthly Payment",
                   'type_by_loan':'Category'},           # map the labels of the figure
            title='Schedule Breakdown By Loan: Cashflow Split', # figure title
            width=width,                   # figure width in pixels
            height=height,                   # figure height in pixels
            template='gridon'            # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
        )
        
        return barchart
    
 
    @staticmethod
    def bar_plot_portfolio_balance_and_interest(schedule_by_loan, portfolio_schedule, height=400, width=800):

        # Create figure with secondary y-axis
        subfig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Define first plot:
        schedule_by_loan_balance = schedule_by_loan.loc[:,['Month','Begin_Principal','Accumulated_Interest','Loan_ID']]
        schedule_by_loan_balance_unpivot = pd.melt(schedule_by_loan_balance, id_vars=['Month','Loan_ID'], var_name='type', value_name='value')
        
        barchart = px.bar(
            data_frame= schedule_by_loan_balance_unpivot[schedule_by_loan_balance_unpivot['type'] == 'Begin_Principal'],
            x="Month",
            y="value",
            color="Loan_ID",               # differentiate color of marks
            opacity=0.9,                  # set opacity of markers (from 0 to 1)
            orientation="v",              # 'v','h': orientation of the marks
            barmode='relative',           # in 'overlay' mode, bars are top of one another.
                                          # in 'group' mode, bars are placed beside each other.
                                          # in 'relative' mode, bars are stacked above (+) or below (-) zero.
            #----------------------------------------------------------------------------------------------
            # facet_row='caste',          # assign marks to subplots in the vertical direction
            # facet_col='caste',          # assigns marks to subplots in the horizontal direction
            # facet_col_wrap=2,           # maximum number of subplot columns. Do not set facet_row!
        
            color_discrete_map={"A": "royalblue",
                               "B": "darkorange",
                               "C": "darkorchid"},
            #----------------------------------------------------------------------------------------------
            # text='value',            # values appear in figure as text labels
            # hover_name='value',   # values appear in bold in the hover tooltip
            # hover_data=['value'],    # values appear as extra data in the hover tooltip
            # custom_data=['value'],     # invisible values that are extra data to be used in Dash callbacks or widgets
        
            labels={"Month":"Month",
                    "value":"Remaining Principal",
                   'Loan_ID': 'Loan'},           # map the labels of the figure
            title= 'Loan Portfolio Schedule: Remaining Balance and Accumulated Interest', # figure title
            width=width,                   # figure width in pixels
            height=height,                   # figure height in pixels
            template='gridon'            # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
        
        )
        
        # Define the second chart
        portfolio_schedule_interest = portfolio_schedule.loc[:,['Month','Accumulated_Interest']]
        
        linechart = px.line(
            data_frame= portfolio_schedule_interest,
            x="Month", 
            y="Accumulated_Interest",
            # color = 'Loan_ID',
            labels={"Month":"Month",
                    "value":"Accumulated Interest"},        
            color_discrete_map={"Accumulated_Interest": "red"})
        
        
        
        # create two independent figures with px.line each containing data from multiple columns
        #fig = px.line(df, y=df.filter(regex="Linear").columns, render_mode="webgl",)
        #fig2 = px.line(df, y=df.filter(regex="Log").columns, render_mode="webgl",)
        
        linechart.update_traces(yaxis="y2")
        
        subfig.add_traces(barchart.data + linechart.data)
        subfig.layout.barmode='relative'
        subfig.layout.xaxis.title="Month"
        subfig.layout.yaxis.title="Remaining Principal"
        subfig.layout.yaxis.color="royalblue"
        subfig.layout.yaxis2.type="linear"
        subfig.layout.yaxis2.color="red"
        subfig.layout.yaxis2.title="Accumulated Interest"
        # recoloring is necessary otherwise lines from fig und fig2 would share each color
        # e.g. Linear-, Log- = blue; Linear+, Log+ = red... we don't want this
        # subfig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))
        subfig.update_layout(height=height, width=width, title_text="Loan Portfolio Schedule: Remaining Balance and Accumulated Interest")
        
        return subfig
        
        
    @staticmethod
    def pie_portfolio(schedule_by_loan, i, height=400, width=450):
        schedule_by_loan_flow = schedule_by_loan.loc[:,['Month','Applied_Principal','Applied_Interest','Loan_ID']]
        schedule_by_loan_flow_unpivot = pd.melt(schedule_by_loan_flow, id_vars=['Month','Loan_ID'], var_name='type', value_name='value')
        schedule_by_loan_flow_unpivot['type_by_loan'] = schedule_by_loan_flow_unpivot['type'] + ' (Loan '+ schedule_by_loan_flow_unpivot['Loan_ID']+')'
        
        schedule_by_loan_flow_unpivot_month = schedule_by_loan_flow_unpivot[schedule_by_loan_flow_unpivot['Month'] == i]
                
        fig = px.pie(schedule_by_loan_flow_unpivot_month, 
             values='value', 
             names='type_by_loan', 
             color_discrete_map = {"Applied_Principal (Loan A)": "royalblue",
                                        "Applied_Principal (Loan B)": "darkorange",
                                        "Applied_Principal (Loan C)": "darkorchid",
                                        "Applied_Interest (Loan A)": "red",
                                        "Applied_Interest (Loan B)": "darkgreen",
                                        "Applied_Interest (Loan C)": "deepskyblue"},
             title='Loan Portfolio Payment Snapshot: Month #{}'.format(i)        
             )
        fig.update_layout(height=height, width=width)
        
        return fig
    
    #%% Contribution Analysis
    
    @staticmethod
    def bar_plot_duration_interest(impact_df, height = 400, width = 600):
        subfig = make_subplots(specs=[[{"secondary_y": True}]])

        # Adjust impact_df
        impact_df['Case'] = ['All Help','No Help','A Quit','B Quit','C Quit']
        
        impact_df_interest = impact_df.loc[:,['Case','Interest_Paid']]
        impact_df_duration = impact_df.loc[:,['Case','Duration']]
        
        # Define first plot:
        barchart = px.bar(
            data_frame= impact_df_interest,
            x= 'Case',
            y= "Interest_Paid",
            #color="Loan_ID",               # differentiate color of marks
            opacity=0.9,                  # set opacity of markers (from 0 to 1)
            orientation="v",              # 'v','h': orientation of the marks
            barmode='relative',           # in 'overlay' mode, bars are top of one another.
                                          # in 'group' mode, bars are placed beside each other.
                                          # in 'relative' mode, bars are stacked above (+) or below (-) zero.
            #----------------------------------------------------------------------------------------------
            # facet_row='caste',          # assign marks to subplots in the vertical direction
            # facet_col='caste',          # assigns marks to subplots in the horizontal direction
            # facet_col_wrap=2,           # maximum number of subplot columns. Do not set facet_row!
        
            #color_discrete_map={"A": "royalblue",
            #                   "B": "darkorange",
            #                   "C": "darkorchid"},
            #----------------------------------------------------------------------------------------------
            # text='value',            # values appear in figure as text labels
            # hover_name='value',   # values appear in bold in the hover tooltip
            # hover_data=['value'],    # values appear as extra data in the hover tooltip
            # custom_data=['value'],     # invisible values that are extra data to be used in Dash callbacks or widgets
        
            labels={"Case":"Scenario",
                    "Interest_Paid":"Total Interest Paid"},           # map the labels of the figure
            title= 'Contribution Impact Analysis: Interest Paid & Duration', # figure title
            width=800,                   # figure width in pixels
            height=400,                   # figure height in pixels
            template='gridon'            # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
        )
        
        # Define the second chart
        linechart = px.line(
            data_frame= impact_df_duration,
            x="Case", 
            y="Duration",
            # color = 'Loan_ID',
            labels={"Case":"Scenario",
                    "Duration":"Duration"},        
            color_discrete_map={"Duration": "red"})
        
        
        # create two independent figures with px.line each containing data from multiple columns
        #fig = px.line(df, y=df.filter(regex="Linear").columns, render_mode="webgl",)
        #fig2 = px.line(df, y=df.filter(regex="Log").columns, render_mode="webgl",)
        
        linechart.update_traces(yaxis="y2")
        
        subfig.add_traces(barchart.data + linechart.data)
        subfig.layout.barmode='relative'
        subfig.layout.xaxis.title="Scenario"
        subfig.layout.yaxis.title="Total Interest Paid"
        subfig.layout.yaxis.color="royalblue"
        subfig.layout.yaxis2.type="linear"
        subfig.layout.yaxis2.color="red"
        subfig.layout.yaxis2.title="Duration"
        # recoloring is necessary otherwise lines from fig und fig2 would share each color
        # e.g. Linear-, Log- = blue; Linear+, Log+ = red... we don't want this
        # subfig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))
        subfig.update_layout(height=height, width=width, title_text="Contribution Impact Analysis: Interest Paid & Duration")
        
        return subfig
            
    
    
    @staticmethod
    def pie_interest(impact_df, height=400, width=450):
        # impact_df['Case'] = ['All Help','No Help','A Quit','B Quit','C Quit']
        impact_df_mi_interest = impact_df.loc[:,['Case','MIInterest']].iloc[2:,:]
        
        fig = px.pie(impact_df_mi_interest, 
             values='MIInterest', 
             names='Case', 
             color_discrete_map = {"A Quit": "royalblue",
                                    "B Quit": "red",
                                    "C Quit": "darkorange"},
             title='Contribution Impact Analysis: Interest Reduction Split'        
             )
        fig.update_layout(height=height, width=width)
        
        return fig

    @staticmethod
    def pie_duration(impact_df, height=400, width=450):
        # impact_df['Case'] = ['All Help','No Help','A Quit','B Quit','C Quit']
        impact_df_mi_duration = impact_df.loc[:,['Case','MIDuration']].iloc[2:,:]
        
        fig = px.pie(impact_df_mi_duration, 
             values='MIDuration', 
             names='Case', 
             color_discrete_map = {"A Quit": "royalblue",
                                    "B Quit": "red",
                                    "C Quit": "darkorange"},
             title='Contribution Impact Analysis: Duration Reduction Split'        
             )
        fig.update_layout(height=height, width=width)
        
        return fig
        
    #%%

    @staticmethod
    def print(loan):
        x = PrettyTable()
        x.field_names = ['Payment Number', 'Begin Principal', 'Payment', 'Extra Payment',
                         'Applied Principal', 'Applied Interest', 'End Principal']
        for field_name in x.field_names:
            x.align[field_name] = "r"
        for pay in loan.schedule.values():
            x.add_row([pay[0],
                       Helper.display(pay[1]),
                       Helper.display(pay[2]),
                       Helper.display(pay[3]),
                       Helper.display(pay[4]),
                       Helper.display(pay[5]),
                       Helper.display(pay[6])])
        print(x)


        
        
        