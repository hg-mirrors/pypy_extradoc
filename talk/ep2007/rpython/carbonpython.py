import sys

if sys.platform == 'cli':
    # on IronPython, export does nothing
    def export(*args, **kwds):
        if len(args) == 1 and isinstance(args[0], type(export)):
            return args[0]
        else:
            return lambda fn: fn
else:
    # import carbonpython's export
    from pypy.translator.cli.carbonpython import export

