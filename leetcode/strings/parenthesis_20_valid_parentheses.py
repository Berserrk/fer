def valid_parentheses(s:str):
    valid_p_list = {
        ")":"(",
        "]":"[",
        "}":"{"
    }
    stack = []
    
    for p in s:
        if p in valid_p_list.values():
            stack.append(p)
        elif stack and stack[-1]==valid_p_list[p]:
            stack.pop()
        else:
            return False 
    return stack == []

s = "()[]{"

valid_parentheses(s)

