#!/usr/bin/python
import py
from pypy.translator.translator import TranslationContext, graphof
from pypy.jit.hintannotator.annotator import HintAnnotator
from pypy.jit.hintannotator.bookkeeper import HintBookkeeper
from pypy.jit.hintannotator.model import *
from pypy.jit.timeshifter.timeshift import HintTimeshift
from pypy.jit.timeshifter import rtimeshift, rtyper as hintrtyper
from pypy.jit.llabstractinterp.test.test_llabstractinterp import annotation
from pypy.jit.llabstractinterp.test.test_llabstractinterp import summary
from pypy.rpython.lltypesystem import lltype, llmemory
from pypy.rpython.objectmodel import hint, keepalive_until_here
from pypy.rpython import rgenop
from pypy.rpython.lltypesystem import rstr
from pypy.annotation import model as annmodel
from pypy.rpython.llinterp import LLInterpreter
from pypy.objspace.flow.model import checkgraph
from pypy.annotation.policy import AnnotatorPolicy
from pypy.translator.backendopt.inline import auto_inlining
from pypy import conftest

from pypy.rpython.lltypesystem.rstr import string_repr
from pypy.jit.tl import tlr
from pypy.jit.timeshifter.test.test_vlist import P_OOPSPEC

P_NOVIRTUAL = AnnotatorPolicy()
P_NOVIRTUAL.novirtualcontainer = True

def getargtypes(annotator, values):
    return [annotation(annotator, x) for x in values]

def hannotate(func, values, policy=None, inline=None):
    # build the normal ll graphs for ll_function
    t = TranslationContext()
    a = t.buildannotator()
    argtypes = getargtypes(a, values)
    a.build_types(func, argtypes)
    rtyper = t.buildrtyper()
    rtyper.specialize()
    if inline:
        auto_inlining(t, inline)
    graph1 = graphof(t, func)
    # build hint annotator types
    hannotator = HintAnnotator(policy=policy)
    hannotator.base_translator = t
    hs = hannotator.build_types(graph1, [SomeLLAbstractConstant(v.concretetype,
                                                                {OriginFlags(): True})
                                         for v in graph1.getargs()])
    if conftest.option.view:
        hannotator.translator.view()
    return hs, hannotator, rtyper

def timeshift(ll_function, values, opt_consts=[], inline=None, policy=None):
    hs, ha, rtyper = hannotate(ll_function, values,
                               inline=inline, policy=policy)
    htshift = HintTimeshift(ha, rtyper)
    htshift.timeshift()
    t = rtyper.annotator.translator
    for graph in ha.translator.graphs:
        checkgraph(graph)
        t.graphs.append(graph)
    if conftest.option.view:
        from pypy.translator.tool.graphpage import FlowGraphPage
        FlowGraphPage(t, ha.translator.graphs).display()
    # run the time-shifted graph-producing graphs
    graph1 = ha.translator.graphs[0]
    llinterp = LLInterpreter(rtyper)
    builder = llinterp.eval_graph(htshift.ll_make_builder_graph, [])
    graph1args = [builder]
    residual_graph_args = []
    assert len(graph1.getargs()) == 1 + len(values)
    for i, (v, llvalue) in enumerate(zip(graph1.getargs()[1:], values)):
        r = htshift.hrtyper.bindingrepr(v)
        residual_v = r.residual_values(llvalue)
        if len(residual_v) == 0:
            # green
            graph1args.append(llvalue)
        else:
            # red
            assert residual_v == [llvalue], "XXX for now"
            TYPE = htshift.originalconcretetype(v)
            gv_type = rgenop.constTYPE(TYPE)
            gvar = llinterp.eval_graph(htshift.ll_geninputarg_graph, [builder,
                                                                      gv_type])
            if i in opt_consts: # XXX what should happen here interface wise is unclear
                gvar = rgenop.genconst(llvalue)
            if isinstance(lltype.typeOf(llvalue), lltype.Ptr):
                ll_box_graph = htshift.ll_addr_box_graph
            elif isinstance(llvalue, float):
                ll_box_graph = htshift.ll_double_box_graph
            else:
                ll_box_graph = htshift.ll_int_box_graph
            box = llinterp.eval_graph(ll_box_graph, [gv_type, gvar])
            graph1args.append(box)
            residual_graph_args.append(llvalue)
    startblock = llinterp.eval_graph(htshift.ll_end_setup_builder_graph, [builder])

    jitstate = llinterp.eval_graph(graph1, graph1args)
    r = htshift.hrtyper.getrepr(hs)
    llinterp.eval_graph(htshift.ll_close_jitstate_graph, [jitstate])

    # now try to run the blocks produced by the builder
    residual_graph = rgenop.buildgraph(startblock)
    insns = summary(residual_graph)
    fn = lltype.functionptr(lltype.FuncType([lltype.Signed], lltype.Signed),
                            'fn', graph=residual_graph)
    return fn

class CompilationTestCase:
    def annotatefunc(self, func):
        t = TranslationContext(simplifying=True)
        # builds starting-types from func_defs 
        argstypelist = []
        if func.func_defaults:
            for spec in func.func_defaults:
                if isinstance(spec, tuple):
                    spec = spec[0] # use the first type only for the tests
                argstypelist.append(spec)
        a = t.buildannotator()
        a.build_types(func, argstypelist)
        a.simplify()
        return t

    def compilefunc(self, t, func):
        from pypy.translator.c import genc
        builder = genc.CExtModuleBuilder(t, func)
        builder.generate_source()
        builder.compile()
        builder.import_module()
        return builder.get_entry_point()

    def getcompiled(self, func, view=False):
        from pypy.translator.transform import insert_ll_stackcheck
        t = self.annotatefunc(func)
        self.process(t)
        if view or conftest.option.view:
            t.view()
        t.checkgraphs()
        insert_ll_stackcheck(t)
        return self.compilefunc(t, func)

    def process(self, t):
        t.buildrtyper().specialize()
        #raisingop2direct_call(t)

def measure(f, arg, repeat=10000):
    from time import time
    start = time()
    f(arg, repeat)
    return (time() - start) / repeat

def compiled():
    ctc = CompilationTestCase()
    def f(code=str, n=int, repeat=int):
        while repeat >= 0:
            res = tlr.interpret(code, n)
            repeat -= 1
        return res
    
    fc = ctc.getcompiled(f)
    def f(n, repeat):
        return fc(tlr.SQUARE, n ,repeat)
    return fc

def Xtest_tlr():
    bytecode = string_repr.convert_const(tlr.SQUARE)
    fn = timeshift(tlr.interpret, [bytecode, 9], [0], policy=P_OOPSPEC)
    
import math
if __name__ == '__main__':
    ctc = CompilationTestCase()
    def _f(code=str, n=int, repeat=int):
        res = 0
        while repeat >= 0:
            res = tlr.interpret(code, n)
            repeat -= 1
        return res
    
    _fc = ctc.getcompiled(_f)
    def fc(n, repeat):
        return _fc(tlr.SQUARE, n ,repeat)
    def f(n, repeat):
        return _f(tlr.SQUARE, n ,repeat)

    bytecode = string_repr.convert_const(tlr.SQUARE)
    conftest.option.view = True
    fn = timeshift(tlr.interpret, [bytecode, 9], [0], policy=P_OOPSPEC)
    def _fj(n=int, repeat=int):
        res = 0
        while repeat >= 0:
            res = fn(n)
            repeat -= 1
        return res
    fjc = ctc.getcompiled(_fj)
    timings = []
    print '%-20s  %12s %12s' %('', '', 'magnitudes')
    print '%-20s  %12s %12s' %('', 'us/call', 'speedup')
    for name, fn, repeat in (#('Python interpreter', f, 1000),
                             #('RPython interpreter', fc, 100000),
                             ('Compiled', fjc, 1)):
        timings.append(measure(fn, 99999999, repeat))
        print '%-20s: %12f %12f'%(name, timings[-1]*10**6,
                                  math.log10(timings[0] / timings[-1]))
