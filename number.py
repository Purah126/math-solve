
''' module for numeric types/thing required by solve.py '''

__all__ = ['pi', 'e', 'Number', 'Polynomial', 'i', 'TrigPolyError', 'PolyValueError', 'FactorialError']

import decimal

D = decimal.Decimal

_pi = D('3.141592653589793238462643383279502884197169399375' + \
       '1058209749445923078164062862089986280348253421170679')
_e = D('2.718281828459045235360287471352662497757247093699959574966967' + \
      '6277240766303535475945713821785251664274274663919320030')
d80 = D('0.' + '0' * 80 + '1') # rounding errors at 80 digits after the decimal point
d200 = D('0.' + '0' * 200 + '1') # system basically breaks at 200 digits after the decimal point

class FactorialError(ValueError): 
    pass

class TrigPolyError(ValueError):
    pass

class PolyValueError(ValueError):
    pass

from math import factorial as _fact

def _sin(x):
    '''internal'''
    x %= 2*_pi
    v = 0
    for n in range(100):
        v += D((-1)**n)/_fact(2*n+1)*D(x**(2*n+1)) # could produce inaccurate results, not sure
    return v

def _cos(x):
    '''internal'''
    return (1-_sin(x)**D(2)).sqrt()

def _arctan(x): # i don't trust library functions
    '''internal'''
    x = D(x)
    v = D(0)
    for n in range(100):
        if abs(x) <= 1:
            v += (D(-1)**n)/(D(2)*n+1)*(x**(D(2)*n+1))
        else:
            v += (D(-1)**n)/((D(2)*n+1)*(x**(D(2)*n+1)))
    if x > 1:
        v = _pi/2 - v
    if x < -1:
        v = -_pi/2 - v
    return v
    
def _s(x):
    '''internal'''
    return -1 if x < 0 else 1

class ReversedMethods:
    
    '''internal class'''
    
    def __radd__(self, other):
        return self.__add__(other)
        
    def __rsub__(self, other):
        return self.__sub__(other)
        
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __rtruediv__(self, other):
        return self.__truediv__(other)
        
    def __rfloordiv__(self, other):
        return self.__floordiv__(other)
        
    def __rmod__(self, other):
        return self.__mod__(other)
        
    def __rpow__(self, other):
        return self.__pow__(other)
      
class Number(ReversedMethods):
    
    '''Basic numeric type'''
    
    def __init__(self, r=0, i=0):
        if type(r) == Number:
            self.r, self.i = r.r, r.i
        else:
            self.r = D(r)
            self.i = D(i)
        if self.r == 0:
            self.r = D(d200) # causes weird errors when set to 0
        if self.i == 0:
            self.i = D(d200) # same thing
    
    def __str__(self):
        if (self.r < d80 and self.r >= 0) or (self.r > 0 - d80 and self.r < 0):
            if (self.i < d80 and self.i >= 0) or (self.i > 0 - d80 and self.i < 0):
                return '0'
            elif self.i == 1:
                x = 'i'
            elif self.i == -1:
                x = '-i'
            else:
                x = f'{self.i}i'
        else:
            if (self.i < d80 and self.i >= 0) or (self.i > 0 - d80 and self.i < 0):
                x = str(self.r)
            elif self.i == 1:
                x = f'{self.r} + i'
            elif self.i == -1:
                x = f'{self.r} - i'
            elif self.i > 0:
                x = f'{self.r} + {self.i}i'
            else:
                x = f'{self.r} - {str(abs(self.i))[1:]}i'
        return x.strip('0').strip('.')
    
    def __abs__(self):
        return Number((self.r ** 2 + self.i ** 2).sqrt())
    
    def __eq__(self, other):
        other = Number(other)
        return ((self.r == other.r) and (self.i == other.i))
        
    def __ne__(self, other):
        return (not (self == other))
    
    def __gt__(self, other):
        other = Number(other)
        return (abs(self).r > abs(other).r)
    
    def __ge__(self, other):
        return ((self > other) or (self == other))
    
    def __lt__(self, other):
        return (not (self >= other))
    
    def __le__(self, other):
        return not ((self > other))
    
    def __add__(self, other):
        if type(other) == Polynomial:
            return other + self
        other = Number(other)
        return Number(self.r + other.r, self.i + other.i)
    
    def __sub__(self, other):
        if type(other) == Polynomial:
            return other + self
        other = Number(other)
        return Number(self.r - other.r, self.i - other.i)
    
    def __mul__(self, other):
        if type(other) == Polynomial:
            return other + self
        other = Number(other)
        return Number(self.r*other.r - self.i*other.i, self.r*other.i + self.i*other.r)
    
    def __truediv__(self, other):
        if type(other) == Polynomial:
            raise TypeError('Cannot divide number by polynomial')
        other = Number(other)
        a = self.r
        b = self.i
        c = other.r
        d = other.i
        cd = c*c + d*d
        e = (a*c + b*d)/cd
        f = (b*c - a*d)/cd
        return Number(e, f)
        
    def __floordiv__(self, other):
        x = self / other
        return Number(int(x.r), int(x.i))
        
    def __mod__(self, other):
        x, y = self // other, self / other
        xr, xi, yr, yi = x.r, x.i, y.r, y.i
        return Number(yr - xr, yi - xi)
        
    def __ln__(self): # magic
        r = ((self.r**D(2)+self.i**D(2)).ln())/2
        i = (-1 if self.i < 0 else 1)*_arctan(self.i/self.r)
        return Number(r, i)

    def __pow__(self, other, flag=False):
        other = Number(other)
        if other.r == 0.5 and not flag:
            if ((self.i < d80 and self.i > 0) or (self.i > 0 - d80 and self.i < 0)):
                if self.r < 0:
                    return Number(0, abs(self.r).sqrt())
                else:
                    return Number(self.r.sqrt(), True)
            else:
                return self.__pow__(Number(other))
        other = Number(other)
        if ((self.r < d80 and self.r > 0) or (self.r > 0 - d80 and self.r < 0)) and \
           ((self.i < d80 and self.i > 0) or (self.i > 0 - d80 and self.i < 0)):
               return Number()
        s = self.__ln__()
        a, b, c, d = other.r, other.i, s.r, s.i
        r, i = ((a*c) - (b*d)).exp(), ((a*d) + (b*c))
        return Number(_cos(i) * r, _sin(i) * r)
    
    def __log__(self, base=_e):
        if base == _e:
            return self.__ln__()
        return self.__ln__() / Number(base).__ln__
        
    def __round__(self):
        return Number(round(self.r), round(self.i))
        
    def __fact__(self):
        if (self.r % 1 > d80 and self.r % 1 > 0) or (self.r % 1 < 0 - d80 and self.r % 1 < 0):
            raise FactorialError('Cannot calculate fractional factorial')
        if (self.i >= d80 and self.i > 0) or (self.i <= 0 - d80 and self.i < 0):
            raise FactorialError('Cannot compute imaginary/complex factorial')
        self.r = abs(self.r)
        if self.r == 1:
            return 1
        else:
            return self * (self - Number(1, 0)).__fact__()
            
    def __neg__(self):
        return Number(0) - self
        
    __xor__ = __pow__
    __call__ = __mul__ # bypass, might integrate into solve.py soon
        
    def solve(self):
        return self


N = Number
i = N(0, 1)
e = N(_e)
pi = N(_pi)
    
def _normalize(p):
    '''required by polynomial divmod'''
    while p and p[-1] == 0:
        p.pop()
    if p == []:
        p.append(0)
    # i don't like how this dosen't return something
    return p

class Polynomial(ReversedMethods):
    
    '''Polynomial object'''
    
    def __init__(self, *ds):
        if len(ds) == 1:
            if type(ds[0]) == Polynomial:
                self.length, self.ds = len(ds[0]), ds[0].ds
            else:
                self.length = 1
                self.ds = ds
        else:
            self.length = len(ds)
            self.ds = list(ds)
        self.ext = ''
        
    def __len__(self):
        return self.length
    
    def _1do(self, other, func):
        if type(other) == Number:
            ds = self.ds
            ds[-1] = func(ds[-1], other)
            return Polynomial(*ds)
        other = Polynomial(other)
        sds = self.ds
        ods = other.ds
        while len(sds) < len(ods):
            sds = [Number(0)] + sds
        while len(ods) < len(sds):
            ods = [Number(0)] + ods
        tds = []
        for s, o in zip(sds, ods):
            tds.append(func(s, o))
        return Polynomial(*tds)
    
    def __add__(self, other):
        return self._1do(other, lambda x, y: x + y)
        
    def __sub__(self, other):
        return self._1do(other, lambda x, y: x - y)
        
    def __mul__(self, other):
        if type(other) == Number:
            return Polynomial(*[n * other for n in self.ds])
        other = Polynomial(other)
        out = [Number(0)] * (len(self) if len(self) > len(other) else len(other)) * 2
        other = Polynomial(other)
        out = [Number(0)] * (len(self) if len(self) > len(other) else len(other)) * 2
        sds, ods = self.ds, other.ds
        while len(sds) < len(ods):
            sds = [Number(0)] + sds
        while len(ods) < len(sds):
            ods = [Number(0)] + ods
        for i, m in enumerate(sds):
            for j, n in enumerate(ods):
                out[i + j] += m * n
        return Polynomial(*out)
    
    def __divmod__(self, other):
        if type(other) == Number:
            return self / other, 0
        # implemented in https://stackoverflow.com/questions/26173058/division-of-polynomials-in-python
        a, b = list(reversed(Polynomial(self).ds)), list(reversed(Polynomial(other).ds))
        a, b = _normalize(a), _normalize(b)
        if len(a) >= len(b):
            shiftlen = len(a) - len(b)
            b = [0] * shiftlen + b
        quot = []
        divisor = b[-1]
        for i in range(shiftlen + 1):
            mult = a[-1] / divisor
            quot = [mult] + quot
            if mult != 0:
                d = [mult * u for u in b]
                num = [u - v for u, v in zip(a, d)]
            a.pop()
            b.pop(0)
        a = _normalize(a)
        return Polynomial(*list(reversed(quot))), Polynomial(*list(reversed(a)))
    
    def __floordiv__(self, other):
        return self.__divmod__(other)[0]
        
    def __mod__(self, other):
        return self.__divmod__(other)[0]
       
    def __truediv__(self, other):
        if type(other) == Number:
            return self * (N(1)/other)
        elif type(other) != Polynomial:
            raise TypeError()
        elif len(other.ds) == 1 and len(self.ds) == 1:
            return Polynomial(self.ds[0] / other.ds[0])
        elif len(other.ds) == 1:
            o = Polynomial()
            for d in self.ds:
                o += Polynomial(d) / Polynomial(other.ds[0])
        else:
            o = Polynomial()
            for i, d in enumerate(other.ds):
                o += (self / Polynomial(*([0] * i + d)))
            return o
  
    def __str__(self):
        x = ''
        for j, n in enumerate(self.ds):
            i = len(self) - j - 1
            if i == 0:
                if n > 0:
                    x += f' + {n}'
                elif n < 0:
                    x += f' - {abs(n)}'
            elif i == 1:
                if n == 1:
                    x += ' + x'
                elif n > 0:
                    x += f' + {n}x'
                elif n < 0:
                    x += f' - {abs(n)}x'
            else:
                if n == 1:
                    x += f' + x^{i}'
                elif n > 0:
                    x += f' + {n}x^{i}'
                elif n < 0:
                    x += f' - {abs(n)}x^{i}'
        if x[1] == '-':
            return '-' + x[3:] + self.ext
        else:
            return x[3:] + self.ext
            
    __eq__ = __sub__
    __call__ = __mul__ # bypass, might integrate into solve.py soon
    
    def solve(self):
        ds = self.ds
        if len(self) == 1:
            return 0
        elif len(self) == 2:
            return -ds[1] / ds[0]
        elif len(self) == 3:
            a, b, c = ds[0], ds[1], ds[2]
            return (-b + (b**N(2) - N(4)*a*c)**N(0.5))/(N(2)*a)
        elif len(self) == 4:
            a, b, c, d = tuple(ds)
            t = b/(3*a)
            p = (3*a*c - b*b)/(3*a*a)
            q = (2*b**N(3) - 9*a*b*c + 27*a*a*d)/(27*a**N(3))
            C = (-q/2 + (q*q/4 + p**N(3)/27)**N(0.5))**(N(1)/N(3))
            while not (a*(C**N(3)) + b*(C**N(2)) + (c*C) + d) == 0:
                C -= p/(N(3)*C)
            return C
        else:
            raise PolyValueError()

P = Polynomial
