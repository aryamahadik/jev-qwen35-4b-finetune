"""L-C shared code for T42c, T57 and T56g (C2.1, clean-room, code only, no rows).

One module generator, one IR, one set of renderers, one mutator and one transform library are shared by the three
families (the G0-lites say the builder owns one module generator; seed spaces are disjoint per family).
Nothing in this package executes generated code. The IR interpreter evaluates our own IR tree (not rendered source);
rendered source only ever runs in the signed-off sandbox (od-sbx1) through the executor job lines.
"""
