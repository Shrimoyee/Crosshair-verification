from typing import List
import coverage
import subprocess
# Start coverage tracking
cov = coverage.Coverage()
cov.start()

class ParenthesesChecker:
    def __init__(self, expression: str) -> None:
        assert isinstance(expression, str) and expression != "", "Precondition: Input must be a non-empty string"

        self.expression = expression

    def is_balanced(self) -> bool:
        '''
        Checks if the given parentheses string is balanced.

        Invariant:
        - The input string contains only paranthesis '(', ')', '{', '}', '[' or ']'.
        
        Postconditions:
        - The function returns True if the string is balanced, otherwise False.
        
        '''
        stack: List[str] = []
        matching_bracket = {')': '(', '}': '{', ']': '['}

        for char in self.expression:
            assert char in "({[]})", "Invariant: Expression contains only valid parentheses"
            if char in "({[":
                stack.append(char)
            else:
                if not stack or stack[-1] != matching_bracket[char]:
                    return False
                stack.pop()
        # Postcondition: The stack should be empty for a balanced expression
        # assert (len(stack) == 0) == (self.expression.count("(") == self.expression.count(")")), "Postcondition: Stack should be empty if expression is balanced" #intentional
        # assert isinstance(len(stack),int), "Postcondition: Length of stack must be an integer" #intentional
        
        assert (len(stack)>=0), "Postcondition: Length of stack must be greater than or equal to zero"
        
        if(len(stack) == 0): 
            return True
        else: 
            return False
        # return len(stack) == 0


if __name__ == "__main__":
    # Manual test cases
    expressions = ["()", "(())", "({[]})", "({[)]}", "(((", "))", "{[()()]}", "{[(])}", "{{{{{{{{{{{{{]]]]()()()}}}}}"]
    #, "agdjgdgduygyhfdf{}{}", "75427547254gdhjfdhw}}", "65526{}", ""
    for expr in expressions:
        checker = ParenthesesChecker(expr)
        print(f"Expression: {expr}, Balanced: {checker.is_balanced()}")

    #the empty string "" gives Balanced true therefore added as precondition
     # Run CrossHair analysis
    print("\nRunning CrossHair verification...")
    try:
        subprocess.run(["crosshair", "check", "--analysis_kind=asserts", "parenthesis_checker.py", "-v"], check=True)
    except subprocess.CalledProcessError as e:
        print("CrossHair encountered an error:", e)

    # Stop coverage tracking and generate reports
    cov.stop()
    cov.save()
    cov.report()
    cov.html_report(directory="coverage_report")

    print("\nCoverage report generated! Open coverage_report/index_pc.html to view.")
