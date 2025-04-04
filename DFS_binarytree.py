import coverage
import subprocess
from typing import Optional

# Start code coverage tracking
cov = coverage.Coverage()
cov.start()

class TreeNode:
    '''Binary Tree Node Declaration '''
    def __init__(self, value: int, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.value = value
        self.left = left
        self.right = right

def tree_sum(root: Optional[TreeNode]) -> int:
    '''
    Recursively computes the sum of all values in the binary tree.
    
    Precondition: 
    - root must be a TreeNode or None.
    
    Postcondition:
    - The sum of all node values should be non-negative.
    '''
    assert root is None or root.value >=0, "Precondition: root must be None or root.value must be positive"
    
    if root is None:
        return 0
    
    left_sum = tree_sum(root.left)  # Recursive call on left subtree
    right_sum = tree_sum(root.right)  # Recursive call on right subtree

    total_sum = root.value + left_sum + right_sum

    #assert total_sum >= root.value, "Postcondition: Sum should not decrease"
    
    assert total_sum >= min(root.value, 0), "Postcondition: Sum should not decrease unexpectedly"

    #assert total_sum >=0, "Postcondition: Sum of nodes should be non-negative"
    
    return total_sum

#For manual testing
if __name__ == "__main__":
    
    root = TreeNode(10, TreeNode(5, TreeNode(2), TreeNode(3)), TreeNode(200, None, TreeNode(1)))
    print("Tree Sum:", tree_sum(root)) 
    
    # Run CrossHair analysis
    print("\nRunning CrossHair verification...")
    try:
        subprocess.run(["crosshair", "check", "--analysis_kind=asserts", "DFS_binarytree.py", "-v"], check=True)
    except subprocess.CalledProcessError as e:
        print("CrossHair encountered an error:", e)

    # Stop coverage tracking and generate reports
    cov.stop()
    cov.save()
    cov.report()
    cov.html_report(directory="coverage_report")

    print("\nCoverage report generated! Open coverage_report/index_bt.html to view.")