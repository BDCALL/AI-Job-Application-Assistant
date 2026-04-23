import numexpr as ne

def calculator(x):
    try:
        return str(ne.evaluate(x))
    except:
        return "Invalid expression"