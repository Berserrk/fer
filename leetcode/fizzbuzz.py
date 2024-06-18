for i in range(20):
    input = ''
    if i%3 == 0:
        input += "fizz"
    if i%5 == 0: 
        input += "buzz"
    if input == "":
        input = str(i)
    
print(input)