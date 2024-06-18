# need to use Breadth-First Search to find the minimum number of removals needed
from collections import deque # deque is efficient to add and remove element, memory efficiency

def removeInvalidParentheses(self, s: str) -> List[str]:
    def is_valid(s):
        count = 0
        for char in s:
            if char == '(':
                count += 1
            elif char == ')':
                count -= 1
                if count < 0:
                    return False
        return count == 0

    level = {s}
    while level:
        valid = list(filter(is_valid, level))
        if valid:
            return valid
        level = {s[:i] + s[i+1:] for s in level for i in range(len(s)) if s[i] in '()'}
    return [""]

# s = "()())()"
# First : level is transforming s to set 
# Second: is_valid is applied to all elements present in the set. so for the first : -1 : return False
# Third step : first level:  {'(())()', '()()()', '()())(', '()()))', '()))()', ')())()'}
# The code snippet uses filter() with the is_valid function to filter out valid sequences of parentheses from the level set 
# So for each sequence present in the level sequence, it will filter those respecting the is_valid condition. Then put them in a list.