def diffWaysToCompute(expression):
    def is_integer(expression):
        try:
            int(expression)
            return True
        except Exception as e:
            return False 
        
    if is_integer(expression):
        return [int(expression)]
    else:
        res =[]

    
    for i in range(len(expression)):
        if expression[i] in "-+*":
            left = diffWaysToCompute(expression=[:i])
            right = diffWaysToCompute(expression=[i+1:])
            for l in left:
                for r in right: 
                    if expression[i] == "+":
                        res.append(l+r)
                    if expression[i]=="-":
                        res.append(l-r)
                    if expression[i]=="*":
                        res.append(l*r)
    return res 
