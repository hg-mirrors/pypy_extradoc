\begin{lstlisting}[language=Python]
def interp_eval(code, pc, args, pool):
    code_len = len(code)
    stack = []
    while pc < code_len:
        opcode = ord(code[pc])
        pc += 1

        if opcode == PUSH:
            stack.append(IntObj(char2int(code[pc])))
            pc += 1
        elif opcode == PUSHARG:
            stack.append(args[0])
        elif opcode == SUB:
            a, b = stack.pop(), stack.pop()
            stack.append(b.sub(a))
        elif opcode == LT:
            a, b = stack.pop(), stack.pop()
            stack.append(IntObj(b.lt(a)))
        elif opcode == BR_COND:
            cond = stack.pop()
            if cond.istrue():
                pc += char2int(code[pc])
            pc += 1
        elif opcode == RETURN:
            break
        ...
    return stack[-1]
\end{lstlisting}
