class Loan:
    """ Single Loan class
    With input principal, rate, payment, and extra payment, compute the amortization schedule, as well as
    overall metrics such as time to loan termination, total principal paid, and total interest paid.
    """
    def __init__(self, principal, rate, payment, extra_payment=0.0):
        """ Constructor to setup a single loan.
            :param principal:  principal amount left on the loan
            :param rate: annualized interest rate as a percentage
            :param payment: minimum expected payment
            :param extra_payment: additional payment applied to the interest
        """
        self.principal = principal
        self.rate = rate
        self.payment = payment
        self.extra_payment = extra_payment
        self.schedule = {}
        self.time_to_loan_termination = None
        self.total_principal_paid = 0.0
        self.total_interest_paid = 0.0
        self.return_schedule = 0

    def check_loan_parameters(self):
        if self.principal < 0.01:
            raise ValueError('Warning: Principal must be greater than 0.01')
        if self.rate < 0.0:
            raise ValueError('Warning: Interest rate must be greater than or equal to 0.0')
        if self.payment < 0.01:
            raise ValueError('Warning: Payment must be greater than 0.01')
        if self.extra_payment < 0.0:
            raise ValueError('Warning: Extra payment must be greater than or equal to 0.0')

        payment_critical = round(self.principal * self.rate/12.0/100,2)+0.01
        if self.payment < payment_critical + 0.01:
            raise ValueError(f'Warning: Payment (excluding extra payment) must be greater than {payment_critical}')

    def compute_schedule(self):
        """ Compute the loan schedule.
            :return: None, the schedule is stored in an instance dictionary
        """
        begin_principal = self.principal
        payment = self.payment
        payment_number = 0

        while begin_principal > 0.0:
            payment_number += 1
            applied_interest = begin_principal * self.rate / 12.0 / 100.0
            applied_principal = payment - applied_interest + self.extra_payment
            if applied_principal > begin_principal:
                payment = begin_principal + applied_interest
                extra_payment = 0.0
                applied_principal = payment - applied_interest + extra_payment
            end_principal = begin_principal - applied_principal
            self.schedule[payment_number] = (payment_number, begin_principal, payment,
                                             self.extra_payment, applied_principal,
                                             applied_interest, end_principal)
            begin_principal = end_principal

        self.time_to_loan_termination = max(self.schedule.keys()) if len(self.schedule.keys()) > 0 else None
        self.total_interest_paid = 0.0
        self.total_principal_paid = 0.0
        for pay in self.schedule.values():
            self.total_interest_paid += pay[5]
            self.total_principal_paid += pay[4]
            
    def return_loan_schedule(self):
        """ Return the schedule in a dataframe
        """
        import pandas as pd
        loan_schedule =  pd.DataFrame.from_dict(self.schedule,
                                                orient='index',
                                                columns=['Month', 'Begin_Principal', 'Payment', 'Extra_Payment',
                                                         'Applied_Principal','Applied_Interest','End_Principal ']).round(2)
        
        Accumulated_Interest = 0
        loan_schedule['Accumulated_Interest'] = 0
        
        for i in range(loan_schedule.shape[0]):
            Accumulated_Interest += loan_schedule['Applied_Interest'].values[i]
            loan_schedule.iloc[i,7] = round(Accumulated_Interest,2)
            
        return loan_schedule
        
    
        
        
        
        
        