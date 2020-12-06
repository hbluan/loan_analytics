from loan_analytics.Helper import *
from loan_analytics.Loan import *
from loan_analytics.LoanPortfolio import *
from loan_analytics.LoanImpacts import *

import pandas as pd
import numpy as np

loans = LoanPortfolio()


def add_and_compute_schedule(principal, rate, payment, extra_payment):

    loan = None
    try:
        loan = Loan(principal=principal, rate=rate, payment=payment, extra_payment=extra_payment)
        loan.check_loan_parameters()
        loan.compute_schedule()
    except ValueError as ex:
        print(ex)
    loans.add_loan(loan)
    # Helper.plot(loan)
    # Helper.print(loan)
    loans.return_portfolio_schedule

    print(round(loan.total_principal_paid, 2), round(loan.total_interest_paid, 2),
          round(loan.time_to_loan_termination, 0))
    
    return loans

def aggregate_loan_portfolio_and_plot(loans):   
    loans.aggregate()
    #Helper.plot(loans)
    #Helper.print(loans)


# =============================================================================
# if __name__ == '__main__':
#     add_and_compute_schedule(12000.0, 4.0, 70.0, 12.0)
#     add_and_compute_schedule(5000.0, 2.0, 20.0, 6.0)
#     #add_and_compute_schedule(10000.0, 3.0, 60.0, 7.0)
#     #add_and_compute_schedule(100.0, 3.0, 60.0, 7.0)
# =============================================================================






