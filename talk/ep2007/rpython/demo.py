import clr
clr.AddReferenceToFile('mylib.dll')

import func
import mylib

N = 10**7
print func.fn(N)
print mylib.fn(N)
