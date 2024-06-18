# Two strings s and t are considered isomorphic if every character in string s can be replaced by a unique character in string t while preserving the order.

# Task is to determine if two gien strings s and t are isomorphic

# Approach to solve: using dictionaries to map characters from string 
s="egg"
t="add"
def isIsomorphic(s:string, t:string):
    s_map, t_map = {}, {}

    for s_char, t_char in zip(s, t):
        if (s_char in s_map and s_map[s_char] != t_char) or (t_char in t_map and t_map[t_char] != s_char ):
            return False 
        s_map[s_char] = t_char
        t_map[t_char] = s_char 

    return True 
