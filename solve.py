
from number import *
import decimal

def sigma(start, end, func):
    '''summation'''
    x = N(0)
    for n in range(int(start.r), int((end + 1).r)):
        x += func(N(n))
    return x
    
def upperpi(start, end, func):
    '''product series'''
    x = N(0)
    for n in range(int(start.r), int((end + 1).r)):
        x *= func(N(n))
    return x
    
def zeta(x): 
    '''riemann zeta function, definitely not perfect, also slow and CPU-heavy'''
    return sigma(N(1), N(1500), lambda n: N(1)/n**x) # change 1500 if you want

def ln(x):
    '''natural logarithm'''
    return x.__ln__()

def log(x, y):
    '''general logarithm'''
    return x.__log__(y)
    
def log10(x): 
    '''base 10 logarithm'''
    return log(x, N(10))

def log2(x): 
    '''base 2 logarithm'''
    return log(x, N(2))
    
def sqrt(x): 
    '''square root'''
    return x**N(0.5)

# trigonometric functions
def sin(x):
    if type(x) == Polynomial:
       raise TrigPolyError()
    x %= 2*pi
    v = 0
    for n in range(100):
        v += D((-1)**n)/fact(2*n+1)*D(x**(2*n+1))
    return v
def cos(x): return (N(1)-sin(x)**N(2))**N(0.5)
def tan(x): return N(sin(x) / cos(x))
def cot(x): return N(N(1) / tan(x))
def sec(x): return N(N(1) / cos(x))
def csc(x): return N(N(1) / sin(x))
def atan(x): return N(_arctan(x.r))
def asin(x): return N(atan(x/sqrt(N(1)-x**N(2))))
def acos(x): return N(atan(N(1)/tan(asin(x))))
def acot(x): return N(atan(N(1)/x))
def asec(x): return N(acos(N(1)/x))
def acsc(x): return N(asin(N(1)/x))

# hyperbolic trigonometric functions
def sinh(x): return (e**x - (e**-x))/2
def cosh(x): return (e**x + (e**-x))/2
def tanh(x): return sinh(x) / cosh(x)
def coth(x): return N(1) / tanh(x)
def sech(x): return N(1) / cosh(x)
def csch(x): return N(1) / sinh(x)
def asinh(x): return ln(x + (x**N(2) + N(1))**N(0.5))
def acosh(x): return ln(x + (x**N(2) - N(1))**N(0.5))
def atanh(x): return N(1/2) * ln((N(1) + x)/(N(1) - x))
def acoth(x): return N(1/2) * ln((N(1) + x)/(x - N(1)))
def asech(x): return ln((N(1) + (N(1) - x**N(2))**N(0.5))/x)
def acsch(x): return ln(N(1)/x + (N(1)/x**N(0.5) + N(1))**N(0.5))

def sign(x): 
    '''gets sign'''
    return N(-1) if x < 0 else N(1)

# operation functions
def add(x, y): return x + y
def sub(x, y): return x - y
def mul(x, y): return x * y
def div(x, y): return x / y
def floordiv(x, y): return x // y
def mod(x, y): return x % y

# gets function, pretty simple
def get_func(f, x): return lambda v: f(v, x)

def parse_query(q):
    q = q.lower()
    xls = re.findall('([0123456789i.]+)?x(\^[0123456789]+)?', q)
    xls.sort(key=lambda x: 10000-len(x))
    for xl in xls:
        x = list(xl)
        if x[0] == '':
            d = 1
        else:
            d = N(x[0])
        if x[1] == '':
            ex = 1
        else:
            ex = int(x[1][1:])
        EX = ('N(0), ' * ex)[:-2]
        p = f'P(*[N({d}), {EX}])'
        q = q.replace('x'.join(x), p)
    ns = re.findall('(?<!N.)[0123456789][0123456789i.]*', q)
    ns.sort(key=lambda x: 10000-len(x))
    for n in ns:
        an = n if 'i' not in n else '0, ' + n.replace('i', '')
        q = re.sub(f'(?<![0123456789i.])(?<!N\(){n}(?![0123456789])', f'N({an})', q)
    q = q.replace('^', '**')
    q = q.replace('true', 'B(True)')
    q = q.replace('false', 'B(False)')
    q = q.replace('=', '==')

def evaluate(q):
    try:
        return str(eval(q)).replace('True', 'true').replace('False', 'false')
    except decimal.Overflow:
        return 'Your number is too large'
    except FactorialError:
        return 'Cannot compute factorial of non-integer numbers'''
    except PolyValueError:
        return 'Cannot evaluate quartic or higher polynomials'
    except TrigPolyError:
        return 'Cannot compute trigonometry of variable expressions'
    except SyntaxError:
        return 'There is a semantic error in your equation, or you are trying non-natural powers of x'
    except TypeError:
        return 'There is something wrong with either your equation or the solver, or you are trying to ' + \
               'solve inequalites, which are not supported :(. Try changing your equation slightly. ' + \
               'If it still dosen\'t work, report it, but if you are trying non-natural powers of x,' + \
               ' those don\'t work either. Or maybe something else is doing this, the error is''' + str(e)
    except Exception as e:
        return 'The solver has encountered an unspecified error, please report this, error is:' + str(e)

if __name__ = __main__:
    query = input('Enter query:')
    query = parse_query(query)
    print('Solved/Evaluated: ' + evaluate('(' + q + ').solve()'))
    print('Simplified:' + evaluate(q))
    
