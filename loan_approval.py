import math
import coverage
import subprocess
# Start code coverage tracking
cov = coverage.Coverage()
cov.start()

class Customer:
    '''Represents a customer applying for a loan.'''

    def __init__(self, name: str, credit_score: int, income: float, dti: float):
        assert isinstance(name, str) and name.strip(), "Precondition: Name must be a non-empty string."
        assert isinstance(credit_score, int), "Precondition: Credit score must be an integer."
        assert isinstance(income, (int, float)) and income > 0, "Precondition: Income must be a positive number."
        assert isinstance(dti, float) and 0 <= dti <= 1, "Precondition: DTI must be between 0 and 1."

        self.name = name
        self.credit_score = credit_score
        self.income = income
        self.dti = dti  # Debt-to-income ratio

class LoanEvaluator:
    '''Evaluates loan eligibility and determines interest rates.'''

    def check_loan_eligibility(self, customer: Customer, loan_amount: float) -> bool:
        '''
        Determines if a customer is eligible for a loan.
        Preconditions:
        - Customer must be a valid instance of Customer.
        - Loan amount must be positive.
        Postconditions:
        - Returns True if eligible, False otherwise.
        '''
        assert isinstance(customer, Customer), "Precondition: customer must be a valid Customer object."
        assert isinstance(loan_amount, (int, float)) and loan_amount > 0, "Precondition: Loan amount must be positive."

        if customer.credit_score >= 600 and customer.income > 25000 and customer.dti < 0.4:
            return True
        return False

    def calculate_interest_rate(self, customer: Customer) -> float:
        '''
        Determines the interest rate based on credit score.
        Preconditions:
        - Customer must be a valid instance of Customer and be within a range of values.
        Postconditions:
        - Returns an interest rate between 3% and 15%.
        '''
        assert isinstance(customer, Customer), "Precondition: customer must be a valid Customer object."
        assert 300 <= customer.credit_score <= 850, "Precondition: Credit score must be between 300 and 850."

        if customer.credit_score >= 750:
            interest_rate = 3.5
        elif customer.credit_score >= 650:
            interest_rate = 7.5
        else:
            interest_rate = 12.5

        assert 3.0 <= interest_rate <= 15.0, "Postcondition: Interest rate must be between 3% and 15%."
        return interest_rate

    def simulate_loan_payments(self, loan_amount: float, interest_rate: float, years: int) -> float:
        '''
        Simulates total loan repayment using compound interest.
        Preconditions:
        - Loan amount must be positive and finite.
        - Interest rate must be between 3% and 15%.
        - Years must be at least 1.
        Postconditions:
        - Returns the total amount to be repaid which must be greater than the loan amount.
        '''
        #assert isinstance(loan_amount, (int, float)) and loan_amount > 100, "Precondition: Loan amount must be integer or float and \should be more than 100 (to avoid assertion failure)"
        assert math.isfinite(loan_amount) and loan_amount > 100, "Precondition: Loan amount must be a finite number."
        assert 3.0 <= interest_rate <= 15.0, "Precondition: Interest rate must be between 3% and 15%."
        assert isinstance(years, int) and years >= 1, "Precondition: Loan period must be at least 1 year."

        # Using compound interest
        total_repayment = loan_amount
        for year in range(years):
            assert total_repayment >= loan_amount, "Invariant: Total repayment must never be less than loan amount at any step."
            total_repayment *= max(1.01, (1 + interest_rate / 100))

        assert total_repayment > loan_amount, "Postcondition: Final repayment must be greater than initial loan amount."
        return total_repayment

if __name__ == "__main__":
    customer1 = Customer("Alice", 700, 50000, 0.3)
    evaluator = LoanEvaluator()

    if evaluator.check_loan_eligibility(customer1, 20000):
        rate = evaluator.calculate_interest_rate(customer1)
        total_payment = evaluator.simulate_loan_payments(20000, rate, 5)
        print(f"Loan approved! Interest Rate: {rate}%. Total Repayment: ${total_payment:.2f}")
    else:
        print("Loan Rejected")
    
    # Run CrossHair analysis
    print("\nRunning CrossHair verification...")
    try:
        subprocess.run(["crosshair", "check", "--analysis_kind=asserts", "loan_approval.py", "-v"], check=True)
    except subprocess.CalledProcessError as e:
        print("CrossHair encountered an error:", e)

    # Stop coverage tracking and generate reports
    cov.stop()
    cov.save()
    cov.report()
    cov.html_report(directory="coverage_report")

    print("\nCoverage report generated! Open coverage_report/index_la.html to view.")
