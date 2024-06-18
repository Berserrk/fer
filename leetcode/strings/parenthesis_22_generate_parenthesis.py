def generate_parenthesis(n):
    def rec_gp(left, right, s):
        if len(s)==n*2:
            output.append(s)  
            return  output 

        if left<n:
            rec_gp(left+1, right, s + "(")
        if right<left:
            rec_gp(left, right+1, s + ")")
    
    output = []
    rec_gp(0, 0, "")
    return output
print(generate_parenthesis(3))

