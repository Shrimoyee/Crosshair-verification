files
-------------------------------------------------------------------------------------------------------------
## **loan_approval system**
This program simulates a loan approval system where a customer applies for a loan. The system evaluates credit score, income, and debt-to-income (DTI) ratio, and calculates loan interest rates based on risk.

why is it chosen?
 Real-World Finance Case: Loan approval is a common business scenario.
✔ Interrelated Functions: Loan eligibility affects interest rates & repayments.
✔ Class and Loop Invariants: Ensures consistency in calculations.
✔ Weak Conditions: Allows CrossHair to find counterexamples & force modifications.

C:\Users\Dell\Desktop\coursework\validationnverfication\crosshair_project\crosshair_env\loan_approval.py:72: error: AssertionError: Invariant: Total repayment must always be greater than the initial loan amount. when calling simulate_loan_payments(LoanEvaluator(), 0.5, 3.0, 1)

I found an exception while running your function.
C:\Users\Dell\Desktop\coursework\validationnverfication\crosshair_project\crosshair_env\loan_approval.py:73:
|        total_repayment = loan_amount
|        for year in range(years):
|            total_repayment *= (1 + interest_rate / 100)
>            assert total_repayment > loan_amount, "Invariant: Total repayment must always be greater than the initial loan amount."
|
|        assert total_repayment > loan_amount, "Postcondition: Final repayment must be greater than initial loan amount."
|        return total_repayment

AssertionError: Invariant: Total repayment must always be greater than the initial loan amount.
when calling simulate_loan_payments(LoanEvaluator(), float("inf"), 3.0, 1)

removed the invariant

I found an exception while running your function.
C:\Users\Dell\Desktop\coursework\validationnverfication\crosshair_project\crosshair_env\loan_approval.py:74:
|        for year in range(years):
|            total_repayment *= (1 + interest_rate / 100)
|
>        assert total_repayment > loan_amount, "Postcondition: Final repayment must be greater than initial loan amount."
|        return total_repayment
AssertionError: Postcondition: Final repayment must be greater than initial loan amount.
when calling simulate_loan_payments(LoanEvaluator(), float("inf"), 3.0, 1)

Answers:--> Extremely small loan amounts → Floating point precision errors.
2️⃣ Low interest rates (e.g., 3%) over short terms (1 year) → The increase may not be significant.
3️⃣ Edge cases like loan_amount=float('inf') → The calculation does not handle infinity properly.

To  fix update preconditions to only accept loan_amounts>100 and added loop invariant in line 73
Why? prevents float point precision errors and ensures the amount is in a realistic range.

Still exception
I found an exception while running your function.
C:\Users\Dell\Desktop\coursework\validationnverfication\crosshair_project\crosshair_env\loan_approval.py:76:
|            assert total_repayment >= loan_amount, "Invariant: Total repayment must never be less than loan amount at any step."
|            total_repayment *= (1 + interest_rate / 100)
|
>        assert total_repayment > loan_amount, "Postcondition: Final repayment must be greater than initial loan amount."
|        return total_repayment
|
|if __name__ == "__main__":

AssertionError: Postcondition: Final repayment must be greater than initial loan amount.
when calling simulate_loan_payments(LoanEvaluator(), float("inf"), 3.0, 1)

Still the same assertion failure modified the condition to max for smaller loan amounts but still the same failure

I found an exception while running your function.
C:\Users\Dell\Desktop\coursework\validationnverfication\crosshair_project\crosshair_env\loan_approval.py:76:
|            assert total_repayment >= loan_amount, "Invariant: Total repayment must never be less than loan amount at any step."
|            total_repayment *= max(1.01, (1 + interest_rate / 100))
|
>        assert total_repayment > loan_amount, "Postcondition: Final repayment must be greater than initial loan amount."
|        return total_repayment
|
|if __name__ == "__main__":

AssertionError: Postcondition: Final repayment must be greater than initial loan amount.
when calling simulate_loan_payments(LoanEvaluator(), float("inf"), 3.0, 1)

to fix this i added precondition to avoid infinity values
assert math.isfinite(loan_amount) and loan_amount > 100
which doesnt give any counterexamples

crosshair failed to catch counterexamples for customer.creditscore which are very large
since i didnt put any precondition on that. As per FICO range it should be within 300-850
so i added that as precondition in line 45 and ran it again. ran without any failures.
max_uninteresting_path=80

Manual testing-->  python loan_approval.py
Loan approved! Interest Rate: 7.5%. Total Repayment: $28712.59
tried with invalid credit scores(900,200), invalid dti values and checked loan eligibility with various parameters. All pre and post conditions fails as expected.
---------------------------------------------------------------------------------------------
## ** fraud_detection.py **
after completion of the program and wrinting the pre,post conditions thought crosshair
will provide counterexamples for customer_id >=0 check and depth but didnt receive that.
so added depth>=0 so that negative depth values are not generated.

I found an exception while running your function.
C:\Users\Dell\Desktop\coursework\validationnverfication\crosshair_project\crosshair_env\fraud_detection.py:58:
|        if visited is None:
|            visited = set()
|
>        visited.add(customer_id)
|
|        # Base case: If this customer is a fraudster, return True
|        for neighbor_id in self.graph.get(customer_id, []):

AttributeError: 'LazyIntSymbolicStr' object has no attribute 'add'
when calling is_fraudulent_connection(TransactionNetwork(), 0, visited='', depth=0)
so added precondition for customer_id to be present in the graph in line 52.
indication-> CrossHair Struggles with Recursion – Deep recursive calls increase complexity, making it hard for CrossHair to explore all paths.
all indicates all the conditions were strong since i added loop invariants as well. 
---------------------------------------------------------------------------------------
## ** weather_evaluation.py **
predicts if it will rain tomorrow based on meteorological features.
uses RaininAustralia dataset (publicly available) added in the directory local

C:\Users\Dell\Desktop\coursework\validationnverfication\crosshair_project\crosshair_env\weather_evaluation.py:25: error: ValueError: embedded null character when calling load_dataset(WeatherMLModel(), '\x00')
so added stronger precondition for file_path to disallow string '\00' or empty spaces. also added file_path check

C:\Users\Dell\Desktop\coursework\validationnverfication\crosshair_project\crosshair_env\weather_evaluation.py:27: error: OSError: [Errno 22] Invalid argument: '\x01' when calling load_dataset(WeatherMLModel(), '\x01')
while loading the filepath for getting the dataset so added file_path check , if it exists or not added as precondition

while doing crosshair watch->
I found an exception while running your function.
C:\Users\Dell\Desktop\coursework\validationnverfication\crosshair_project\crosshair_env\weather_evaluation.py:28:
|        assert '\x00' not in file_path, "Precondition: file_path cannot contain null characters."
|        assert os.path.exists(file_path), "Precondition: File must exist."
|
>        df = pd.read_csv(file_path)

PermissionError: [Errno 13] Permission denied: '.'
when calling load_dataset(WeatherMLModel(), '.') because crosshair added current directory not a file in the 
file_path so pd.read_csv() fails so i added another precondition to check if the file_path contains a file.

After running the program, I thought crosshair will generate counterexamples for various edge cases of csv files and check if they are proper but it failed to generate any counter examples for line 30 but it seems CrossHair cannot create invalid CSV files so that will not be achieved. Manual testing was done with example csv files to check that.
Also for line 32 crosshair didnt do any check if too much data is lost in .dropna() which was expected by me. So i wrote another assert statement for postcondition to check if too much data is not lost after dropna()

Manual testing->
#assert df.shape[0] > 0.75 * initial_rows, "Postcondition: More than 75% of data lost after dropping NaN values." -> this precondition had to removed while manual testing since the dataset(weatherAUS.csv) contained a lot of NaN values.
self.labels = df["RainTomorrow"].values  # Target variable (0 or 1)
    self.data = df.drop(columns=["RainTomorrow"]).values  # Features
this was added sklearn library cant process string values - "yes"/"no" prediction was converted to boolean before training the model.
Received: Prediction: No Rain
crosshair verifies with no exception.

Limitations->
this program highlighted various limitations of crosshair
Limitation	Why It Happens?	Workaround
Struggles with file I/O & APIs	Cannot generate or modify external files	Use DataFrame inputs instead of reading from CSV
Doesn't generate complex edge cases	Doesn't understand domain-specific constraints (e.g., valid values in "RainTomorrow")	Explicit preconditions to define valid ranges
Misses semantic correctness errors	Doesn't know what "correct output" means unless explicitly told	Add postconditions to check correctness
Hard to verify loops over large data	Symbolic execution can't explore every loop iteration	Use smaller inputs and add loop invariants

in these kind of programs, manual testing is prudent along with testing of some edge cases.
----------------------------------------------------------------------------------
## ** browser_history.py **
Models backward and forward navigation in a web browser.
Ensures stack never underflows (e.g., navigating back when history is empty).
Verifies loop invariants (e.g., URLs are popped in correct order).

while manually testing this asserting failed assert len(self.back_stack) > 1, "Precondition: Must have history to go back."
so i updated the assertion to >=.
Same for this assert len(self.forward_stack) > 0, "Precondition: Must have pages in forward stack to go forward." So added check for both. commneted the assert statements for the preconditions for both go_forward() fn and go_back() function to handle those cases. --> example of the drawbacks of defensive programming
mixes application logic with assertion checks can be confusing.

Crosshair verification no assertion failure found.
Indication->
CrossHair did not catch stack underflow (calling go_back() when stack is empty)	CrossHair did not generate sequences of calls that create this scenario (e.g., visiting pages and going back multiple times).	Symbolic execution struggles with state-dependent logic (e.g., function behavior depends on past function calls).
CrossHair did not check forward stack emptiness in go_forward()	CrossHair only tests functions in isolation but doesn’t simulate sequences of real-world actions.	Stack operations often rely on previous states, but CrossHair does not track history well.
CrossHair did not generate enough real-world sequences	It does not explore how function calls interact over time.	CrossHair is better for mathematical or recursive problems, not state-dependent stack problems.