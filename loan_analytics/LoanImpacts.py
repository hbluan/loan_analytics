from loan_analytics.Loan import Loan
from loan_analytics.LoanPortfolio import LoanPortfolio


class LoanImpacts:
    """ Contributor Impacts to Loan class
    """

    def __init__(self, principal, rate, payment, extra_payment, contributions):
        self.principal = principal
        self.rate = rate
        self.payment = payment
        self.extra_payment = extra_payment
        self.contributions = contributions

    def compute_impacts(self):
        # setup a loan portfolio
        # loan_portfolio = LoanPortfolio()
        
        import pandas as pd
        
        impact_matrix = []

        # loan with all contributions (mi)_all
        #
        loan_all = Loan(principal=self.principal, rate=self.rate,
                        payment=self.payment, extra_payment=self.extra_payment + sum(self.contributions))
        loan_all.check_loan_parameters()
        loan_all.compute_schedule()

        # loan with no contributions (mi)_0
        #
        loan_none = Loan(principal=self.principal, rate=self.rate,
                         payment=self.payment, extra_payment=self.extra_payment)
        loan_none.check_loan_parameters()
        loan_none.compute_schedule()

        micro_impact_interest_paid_all = \
            (loan_none.total_interest_paid - loan_all.total_interest_paid) / loan_all.total_interest_paid
        micro_impact_duration_all = -\
            (loan_none.time_to_loan_termination - loan_all.time_to_loan_termination) / loan_all.time_to_loan_termination

        # micro_impact_interest_paid_all = loan_none.total_interest_paid / loan_all.total_interest_paid
        # micro_impact_duration_all = loan_none.time_to_loan_termination / loan_all.time_to_loan_termination

        print(f'\nIndex\tInterestPaid\tDuration\tMIInterest\tMIDuration')
        print(f'ALL \t\t',
              round(loan_all.total_interest_paid, 2), f'\t\t', loan_all.time_to_loan_termination)
        print(f'0\t\t\t',
              round(loan_none.total_interest_paid, 2), f'\t\t', loan_none.time_to_loan_termination, f'\t\t',
              round(micro_impact_interest_paid_all, 4), f'\t', round(micro_impact_duration_all, 4))
        
        impact_all = [round(loan_all.total_interest_paid, 2),
                      loan_all.time_to_loan_termination,0,0]
        
        impact_matrix.append(impact_all)
        
        impact_none = [round(loan_none.total_interest_paid, 2),
                       loan_none.time_to_loan_termination,
                       round(micro_impact_interest_paid_all, 4),
                       round(micro_impact_duration_all, 4)]

        impact_matrix.append(impact_none)
        
        # iterate over each contribution (mi)_index
        #
        for index, contribution in enumerate(self.contributions):
            loan_index = Loan(principal=self.principal, rate=self.rate, payment=self.payment,
                              extra_payment=self.extra_payment + sum(self.contributions) - contribution)
            loan_index.check_loan_parameters()
            loan_index.compute_schedule()

            micro_impact_interest_paid = \
                (loan_index.total_interest_paid - loan_all.total_interest_paid) / loan_all.total_interest_paid
            micro_impact_duration = \
                (loan_index.time_to_loan_termination - loan_all.time_to_loan_termination) / loan_all.time_to_loan_termination

            # micro_impact_interest_paid = loan.total_interest_paid / loan_all.total_interest_paid
            # micro_impact_duration = loan.time_to_loan_termination / loan_all.time_to_loan_termination

            print(index+1, f'\t\t\t',
                  round(loan_index.total_interest_paid, 2), f'\t\t', loan_index.time_to_loan_termination, f'\t\t',
                  round(micro_impact_interest_paid, 4), f'\t', round(micro_impact_duration, 4))

            impact_without_k = [round(loan_index.total_interest_paid, 2),
                                loan_index.time_to_loan_termination,
                                round(micro_impact_interest_paid, 4),
                                round(micro_impact_duration, 4)]
            
            impact_matrix.append(impact_without_k)
            
        impact_df = pd.DataFrame(impact_matrix,
                                 columns=['Interest_Paid', 'Duration', 'MIInterest','MIDuration'])
            
        return impact_df









