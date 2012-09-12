from pypy.translator.interactive import Translation
from pypy.annotation.model import SomeInteger

try:
    import rlcompleter2
    rlcompleter2.setup()
except ImportError:
    pass

import wp5_example

t = Translation(wp5_example.is_prime)
t.annotate([SomeInteger(nonneg=True)])
t.view()
t.rtype()
t.view()
t.backendopt(backend="c")
t.view()
f = t.compile()
print "value returned by the compiled function with argument 5"
print f(5)
