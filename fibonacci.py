from typing import List

def remove_smallest(numbers: List[int]) -> None:
  ''' Removes the smallest number in the given list. '''

  # The precondition: CrossHair will assume this to be true:
  assert len(numbers) > 0

  smallest = min(numbers)

  numbers.remove(smallest)

  # The postcondition: CrossHair will find examples to make this be false:
  assert len(numbers) == 0