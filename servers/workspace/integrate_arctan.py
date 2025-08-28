
import sympy

x = sympy.Symbol('x')
f = 1/(1 + x**2)

integral = sympy.integrate(f, (x, 0, 1))

print(f"The definite integral of 1/(1+x^2) from 0 to 1 is: {integral}")
print(f"Numerical value: {integral.evalf()}")
