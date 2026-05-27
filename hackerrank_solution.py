def stepping_cycle(iterable, step):
    """
    Generator that yields tuples (idx, pass_num, elem) from a circular iterable.
    
    Args:
        iterable: An iterable of integers
        step: Integer, number of positions to move within the iterable at each step
    
    Yields:
        tuple: (idx, pass_num, elem) where:
            - idx: number of elements generated so far
            - pass_num: current pass over iterable (starting from 1)
            - elem: current generated element
    """
    # Convert iterable to a list to handle circular access
    elements = list(iterable)
    n = len(elements)
    
    if n == 0:
        return
    
    idx = 0  # Count of elements generated
    current_pos = 0  # Current position in the list
    
    while True:
        # Calculate pass_num based on how many times we've wrapped around
        pass_num = (current_pos // n) + 1
        
        # Get the current element
        elem = elements[current_pos % n]
        
        # Yield the tuple
        yield (idx, pass_num, elem)
        
        # Update counters
        idx += 1
        current_pos += step
