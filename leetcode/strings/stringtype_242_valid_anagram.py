def isAnagram(s:str, t:str):
    if len(s) != len(t):
        return False 
    
    s_count = {}
    t_count = {}

    for char in s: 
        if char in s_count:
            s_count[char] += 1
        else:
            s_count[char] = 1 

    for char in t:
        if char in t_count:
            t_count[char] += 1 
        else:
            t_count[char] = 1
        
    return s_count == t_count 
# Comparing 2 dictionnaries
# for a dictionnary we can match even if it is not in the same order because python is compary the key and value.
# in a list this is not working, because list is taking into account the order