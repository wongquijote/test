def multiply(m, n):
    """
    >>> multiply(5, 3)
    15
    """
    high, low = max(m, n), min(m, n)
    if low == 0:
        return 0
    else:
        return multiply(high, low - 1) + high



def rec(x, y):
    if y > 0:
        return x * rec(x, y - 1)
    return 1
rec(3, 2)
"""global frame:
rec func rec(x, y) p = g

f1: rec p = g
x = 3
y = 2
rv = x * 2 = 9
f2: rec p = g
x = 3
y = 1
rv = x * 1 = 3
f3: rec p = g
x = 3
y = 0
rv = 1
"""

def hailstone(n):
    """Print out the hailstone sequence starting at n, and return the
    number of elements in the sequence.

    >>> a = hailstone(10)
    10
    5
    16
    8
    4
    2
    1
    >>> a
    7
    """
    print(n)
    if n == 1:
        return n
    elif n % 2 == 0:
        return 1 + hailstone(n//2)
    else:
        return 1 + hailstone(n * 3 + 1)


def merge(n1, n2):
    """ Merges two numbers
    >>> merge(31, 42)
    4321
    >>> merge(21, 0)
    21
    >>> merge (21, 31)
    3211
    """
    if n1 % 10 < n2 % 10:
        return merge(n1 // 10, n2) * 10 + n1 % 10
    elif n1 % 10 >= n2 % 10:
        return merge(n1, n2 % 10) * 10 + n2 % 10
    elif n1 == 0:
        return n2
    elif n2 == 0:
        return n1
    


def make_func_repeater(f, x):
    """
    >>> incr_1 = make_func_repeater(lambda x: x + 1, 1)
    >>> incr_1(2) #same as f(f(x))
    3
    >>> incr_1(5)
    6
    """

    def repeat(___________________):

        if _______________________:

           return __________________

        else:

           return __________________

    return _________________________




def is_prime(n):
    """
    >>> is_prime(7)
    True
    >>> is_prime(10)
    False
    >>> is_prime(1)
    False
    """
    def prime_helper(____________________):
        if ________________________:
            ________________________
        elif ________________________:
            ________________________
        else:
            ________________________
    return __________________________


