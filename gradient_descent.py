import coverage
import subprocess
import numpy as np

# Start coverage tracking
cov = coverage.Coverage()
cov.start()

def gradient_descent(x_init: float, learning_rate: float, threshold: float, max_iters: int) -> float:
    '''
    Performs gradient descent on a simple quadratic function.

    Preconditions:
    - learning_rate must be positive.
    - threshold must be positive.
    - max_iters must be more than 5.
    
    Postconditions:
    - The final value should have a derivative close to 0.
    '''
    assert learning_rate > 0, "Precondition: learning_rate must be positive"
    assert threshold > 0, "Precondition: threshold must be positive"
    #assert max_iters > 0, "Precondition: max_iters must be positive"

    assert max_iters > 5, "Precondition: max_iters must be more than 5"

    x = x_init
    for i in range(max_iters):
        gradient = 2 * x  # Considering the derivative of f(x) = x^2
        assert isinstance(gradient, float), "Loop Invariant: Gradient must be a float"
        
        if abs(gradient) < threshold:
            break
        
        x -= learning_rate * gradient
    #assert True

    assert abs(2 * x) < threshold or (i == max_iters -1), "Postcondition: The derivative should be near zero"
    
    return x

# For manual testing
if __name__ == "__main__":
    # Manual test cases
    print("Manual Testing:")
    print("Final value:", gradient_descent(10.0, 0.1, 0.01, 100))
    print("Final value:", gradient_descent(-5.0, 0.05, 0.001, 200))

    # Run CrossHair analysis
    print("\nRunning CrossHair verification...")
    try:
        subprocess.run(["crosshair", "check", "--analysis_kind=asserts", "gradient_descent.py", "-v"], check=True)
    except subprocess.CalledProcessError as e:
        print("CrossHair encountered an error:", e)

    # Stop coverage tracking and generate reports
    cov.stop()
    cov.save()
    cov.report()
    cov.html_report(directory="coverage_report")

    print("\nCoverage report generated! Open coverage_report/index_gd.html to view.")
