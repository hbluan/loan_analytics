import pytest

from loan_analytics.Helper import *
from loan_analytics.Loan import *
from loan_analytics.LoanImpacts import LoanImpacts
from loan_analytics.LoanPortfolio import *

loans = LoanPortfolio()


@pytest.mark.parametrize('principal, rate, payment, extra_payment',
                         [
                             (5000.0, 6.0, 96.66, 0.0),
                             (10000.0, 8.0, 121.33, 0.0),
                             (7000.0, 7.0, 167.62, 0.0),
                         ])
def test_loan(principal, rate, payment, extra_payment):
    loan = None
    try:
        loan = Loan(principal=principal, rate=rate, payment=payment, extra_payment=extra_payment)
        loan.check_loan_parameters()
        print('Parameters are valid')
        return 1,'All Parameters are valid'
        
    except ValueError as ex:
        print(ex)
        return ValueError, ex
        

    assert True


@pytest.mark.parametrize('principal, rate, payment, extra_payment, ' +
                         'total_principal_paid, total_interest_paid, time_to_loan_termination',
                         [
                             (27000.0, 4.0, 150.0, 0.0, 27000.0, 14303.0, 22 * 12.0 + 11.0),
                             (27000.0, 4.0, 150.0, 25.0, 27000.0, 10975.0, 18 * 12.0 + 2.0)
                         ])
def test_loan_with_extra_payment(principal, rate, payment, extra_payment,
                                 total_principal_paid, total_interest_paid,
                                 time_to_loan_termination):
    tolerance_for_cash = 5.0
    tolerance_for_time = 1.0

    loan = None
    try:
        loan = Loan(principal=principal, rate=rate, payment=payment, extra_payment=extra_payment)
        loan.check_loan_parameters()
        loan.compute_schedule()
    except ValueError as ex:
        print(ex)
    loans.add_loan(loan)
    Helper.plot(loan)

    print(round(loan.total_principal_paid, 2), round(loan.total_interest_paid, 2),
          round(loan.time_to_loan_termination, 0))

    assert abs(loan.total_principal_paid - total_principal_paid) <= tolerance_for_cash
    assert abs(loan.total_interest_paid - total_interest_paid) <= tolerance_for_cash
    assert abs(loan.time_to_loan_termination - time_to_loan_termination) <= tolerance_for_time

    if loans.get_loan_count() == 2:
        loans.aggregate()
        Helper.plot(loans)


@pytest.mark.parametrize('principal, rate, payment, extra_payment, contributions',
                         [
                             (68000.0, 4.0, 899.0, 0, [10, 100, 1000])
                         ])
def test_loan_contribution_1(principal, rate, payment, extra_payment, contributions):
    loan_impacts = LoanImpacts(principal=principal, rate=rate, payment=payment,
                               extra_payment=extra_payment, contributions=contributions)
    loan_impacts.compute_impacts()

    assert True
