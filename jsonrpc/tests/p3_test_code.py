# Python3-only code
# This won't even parse in python2, so it's kept in a separate file and imported
# when needed.

def distance(a: float, b: float) -> float:
    return (a**2 + b**2)**0.5
