    def minRemoveToMakeValid(self, s: str) -> str:
        stack = []
        index_to_remove = set()

        for i, char in enumerate(s):
            if char == "(":
                stack.append(i)
            elif char == ")":
                if not stack:
                    index_to_remove.add(i)# to add to a set, use add not append 
                else:
                    stack.pop()
            
        index_to_remove = index_to_remove.union(set(stack))

        return "".join([char for i,char in enumerate(s) if i not in index_to_remove])
        
        # a union is used for set generally in order to merge both of them and remove duplicates