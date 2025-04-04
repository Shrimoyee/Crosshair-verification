import coverage
import subprocess

# Start coverage tracking
cov = coverage.Coverage()
cov.start()

def reverse_alpha_string(s: str) -> str:
    '''
    Reverses the input string only if it contains only alphabets.
    Otherwise, returns the string unmodified.

    '''
    assert (isinstance(s, str) and len(s) > 0), "Precondition: Input must be a non-empty string"  
    
    result = ""
    if s.isalpha():
        for i in range(len(s) - 1, -1, -1):
            result += s[i]
    else:
        result = s 

    #assert (isinstance(result,str)), "Postcondition: result must be a string" #weakened the postcondition to check 
    #assert(len(result) == len(s), "Postcondition: length of the initial and resultant string should be same") #weakened the postcondition to check 
    
    assert result == s[::-1] if s.isalpha() else result == s, "Postcondition: Checks if result is correct"
   
    return result

# For Manual testing
if __name__ == "__main__":
    test_cases = [
        "hello",        # Normal case
        "world!",       # Contains punctuation, should remain unchanged
        "Python123",    # Contains numbers, should remain unchanged
        "racecar",      # Palindrome, should return same string
        "",             # Edge case: empty string (should fail precondition)
    ]
    
    for test in test_cases:
        try:
            print(f"reverse_alpha_string('{test}') -> '{reverse_alpha_string(test)}'")
        except AssertionError as e:
            print(f"AssertionError for input '{test}': {e}")

    # Run CrossHair analysis
    print("\nRunning CrossHair verification...")
    try:
        subprocess.run(["crosshair", "check", "--analysis_kind=asserts", "string_manipulation.py", "-v"], check=True)
    except subprocess.CalledProcessError as e:
        print("CrossHair encountered an error:", e)

    # Stop coverage tracking and generate reports
    cov.stop()
    cov.save()
    cov.report()
    cov.html_report(directory="coverage_report")

    print("\nCoverage report generated! Open coverage_report/index_sm.html to view.")
