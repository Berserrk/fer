def factoriel_number(n):
    # Base case: to escape the recursive f
    if n<=1:
        return 1
    # recursive case 
    else: 
        print(n*factoriel_number(n-1))
        return n*factoriel_number(n-1)



print(factoriel_number(5))

                