from typing import List, Dict
from pprint import pprint

class Loan:
    def __init__(
        self,
        principal: float,
        annual_rate: float,
        term_years: int,
        payments_per_year: int = 12,
        amortization_type: str = "standard",
    ):
        self.principal = principal
        self.annual_rate = annual_rate
        self.term_years = term_years
        self.payments_per_year = payments_per_year
        self.amortization_type = amortization_type

        self.periodic_rate = self.annual_rate / self.payments_per_year
        self.total_payments = self.term_years * self.payments_per_year

    def compute_payment(self) -> float:
        if self.amortization_type == "interest_only":
            return self.principal * self.periodic_rate

        if self.periodic_rate == 0:
            return self.principal / self.total_payments

        r = self.periodic_rate
        n = self.total_payments
        P = self.principal
        return P * r / (1 - (1 + r) ** -n)

    def amortization_schedule(self):
        schedule = []
        balance = self.principal
        payment = self.compute_payment()

        for period in range(1, self.total_payments + 1):
            interest = balance * self.periodic_rate

            if self.amortization_type == "interest_only":
                principal_payment = 0
                if period == self.total_payments:
                    principal_payment = balance
            else:
                principal_payment = payment - interest
                if principal_payment > balance:
                    principal_payment = balance
                    payment = interest + principal_payment  # final adjustment

            balance -= principal_payment
            balance = max(balance, 0.0)

            schedule.append({
                'Period': period,
                'Payment': round(payment, 2),
                'Principal': round(principal_payment, 2),
                'Interest': round(interest, 2),
                'Balance': round(balance, 2),
            })

            if balance <= 0.0:
                break

        return schedule

def compute_balloon_balance(principal, annual_rate, term_years, payments_per_year, periods_paid):
    """
    Computes the balloon balance and payments.
    """
    r = annual_rate / payments_per_year
    N = term_years * payments_per_year
    n = periods_paid

    payment = (r * principal) / (1 - (1 + r) ** -N)
    balloon_balance = payment * ((1 - (1 + r) ** -(N - n)) / r)

    return round(balloon_balance, 2), round(payment, 2)

def balloon_payment_loan(principal, annual_rate, term_years, balloon_years, payments_per_year=12):
    """
    Balloon loan where payments are based on a longer amortization term (e.g., 30-year loan with 15-year balloon payment).

    Returns: amortization schedule including final balloon payment.
    """
    r = annual_rate / payments_per_year
    N = term_years * payments_per_year
    n = balloon_years * payments_per_year

    # Monthly payment calculation
    payment = (r * principal) / (1 - (1 + r) ** -N)

    balance = principal
    schedule = []

    for period in range(1, n + 1):
        interest = balance * r
        principal_payment = payment - interest
        balance -= principal_payment

        schedule.append({
            'Period': period,
            'Payment': round(payment, 2),
            'Principal': round(principal_payment, 2),
            'Interest': round(interest, 2),
            'Balance': round(balance, 2)
        })

    # Final balloon payment
    final_interest = balance * r
    final_payment = balance + final_interest

    schedule.append({
        'Period': n + 1,
        'Payment': round(final_payment, 2),
        'Principal': round(balance, 2),
        'Interest': round(final_interest, 2),
        'Balance': 0.0
    })

    return schedule

"""
Test Loan class
"""
loan = Loan(
    principal=1_000_000,
    annual_rate=0.076,
    term_years=3,
    payments_per_year=12
)

schedule = loan.amortization_schedule()
for row in schedule[:3]:  # preview first 3 payments
    print(row)


"""
Test and verify balloon payment loan
"""
balloon_loan = balloon_payment_loan(
    principal=1_000_000,
    annual_rate=0.06,
    term_years=30,
    balloon_years=15
)

print(balloon_loan[-1])
#$710,488.44

schedule = balloon_payment_loan(
    principal=1_000_000,
    annual_rate=0.06,
    term_years=30,
    balloon_years=5
)

# Show final payment
print("Balloon Payment after 5")
print(schedule[-1])
#$930,543.57