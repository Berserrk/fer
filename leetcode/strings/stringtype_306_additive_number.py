# additive number is a string whose digits can form an additive sequences 
# sum of any two adjacent numbers equals the next number in the sequence
# task is to write a function that checks if a given string represent an additive number 
# use BACKTRACKING algorithm 

num = "112358"
def is_additive_number(num:str):
    def backtrack(start, path):
        if start = len(num) and len(path) >= 3:
            return True 
        