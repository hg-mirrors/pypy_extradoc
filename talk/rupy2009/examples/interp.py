






[x, y]
# LOAD_FAST
frame.valuestack.push(frame.locals[0])
# LOAD_FAST
frame.valuestack.push(frame.locals[1])
# BINARY_ADD
v1 = frame.valuestack.pop()
v0 = frame.valuestack.pop()
v2 = v0.add(v1)
  return IntObject(self.value + other.value) 
frame.valustack.push(v2)
# RETURN_VALUE
return frame.valuestack[-1]















[x, y]
v0 = IntObject(x.value + y.value)
return v0
























[x, y]
return x + y



