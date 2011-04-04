\begin{lstlisting}[language=Python]
def interp_eval_abs(args):
    v0 = args[0]          # stack = [v0]
    v1 = IntObj(0)        #         [v0, v1]
    a, b = v0, v1         #         []
    v0 = IntObj(b.lt(a))) #         [v0]
    cond = v0             #         []
    if cond.istrue():
        v0 = args[0]      #         [v0]
        return v0
    else:
        v0 = IntObj(0)    #         [v0]
        v1 = args[0]      #         [v0, v1]
        a, b = v0, v1     #         []
        v0 = b.sub(a)     #         [v0]
        return v0
\end{lstlisting}
