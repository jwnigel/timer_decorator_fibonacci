def timer(fn, n:int = 10):
    """
    A decorator which runs the decorated function n times.
    Prints the average run time.
    Returns the result of the function as it would run without the decorator.
    """
    from functools import wraps
    from time import perf_counter

    @wraps(fn)  #to maintain function docstring, name, etc when inspecting
    def inner(*args, **kwargs):
        elapsed_total = 0
        elapsed_count = 0

        for i in range(n):
            # print(f'Running iteration {i}... ')    ## uncomment if you want to see progress
            start = perf_counter()
            result = fn(*args, **kwargs)
            end = perf_counter()
            elapsed = start - end
            elapsed_total += elapsed
            elapsed_count += 1

        args_ = [str(a) for a in args]
        kwargs_ = [str(kw) for kw in kwargs]
        all_args = args_ + kwargs_
        args_str = ','.join(all_args)

        elapsed_avg = elapsed_total / elapsed_count

        print(f'Function {fn.__name__}({args_str}) averaged {elapsed_avg:.7f} seconds to run.')
        
        return result
    return inner


### Three functions to calculate the fibonacci numbers. Timed using timer decorator.

# Recursive Function
def fib_rec(n):
    if n <= 2:
        return 1
    else:
        return fib_rec(n-1) + fib_rec(n-2)

@timer    
def calc_fib_rec(n):
    """
    Passing the fibonacci recursive function in so as to only time the total it takes to run, not each recursive calculation
    """
    return fib_rec(n)

# Loop
@timer
def fib_loop(n):
    fib_1 = 1
    fib_2 = 1
    for i in range(3, n):
        fib_1, fib_2 = fib_2, fib_2 + fib_1
    return fib_1 + fib_2

# Built-in reduce function
from functools import reduce
@timer
def fib_reduce(n):
    initial = (0, 1)
    dummy = range(n-1)
    result = reduce(lambda prev, next: (prev[1], prev[0] + prev[1]), 
                    dummy, 
                    initial)
    return result[1]


# The recursive function is clearly the slowest so we'll compare only loop and reduce
print(fib_loop(5000))
print()
print(fib_reduce(5000))

# The two functions are very similar but it seems the loop is a bit faster!