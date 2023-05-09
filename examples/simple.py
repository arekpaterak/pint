import pickle

def random_function() -> int:
    # nested function
    def nested_function() -> int:
        j: int = 1 
        # returns j
        return j
    
    # comment
    i: int = 1 
    while i < 5:
        i = i + 1
    
    # returns i
    return i
