import math
from sqrt import sqrt, Fix16

for i in range(2,10) + [123]:
    print i, sqrt(i), '%4.2f' % sqrt(float(i)), \
          '%4.2f' % float(sqrt(Fix16(i))), '%4.2f' % math.sqrt(i)
