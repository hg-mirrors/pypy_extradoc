\begin{lstlisting}[language=Python]
def interp_eval_abs(args):
    stack = []
    stack.append(args[0])
    stack.append(IntObj(0))
    a, b = stack.pop(), stack.pop()
    stack.append(IntObj(b.lt(a)))
    cond = stack.pop()
    if cond.istrue():
        stack.append(args[0])
        return stack[-1]
    else:
        stack.append(IntObj(0))
        stack.append(args[0])
        a, b = stack.pop(), stack.pop()
        stack.append(b.sub(a))
        return stack[-1]
\end{lstlisting}
