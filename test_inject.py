
from inject import inject

@inject(a=5)
def test_inject():
    print locals()
    assert locals() == {'a': 5}

@inject(cat='foo', whatever=15)
def test_inject2():
    print locals()
    assert locals() == {'cat': 'foo', 'whatever': 15}

def test_inject_keeps_old_trace_behavior():
    import sys
    events = []
    def tracefn(frame, event, arg):
        # only grab the events for our function
        if frame.f_code.co_name == 'foo':
            events.append(event)
        return tracefn

    @inject(a=5)
    def foo():
        assert locals() == {'a': 5}

    # be a good citizen and reset our tracefn
    old_trace = sys.gettrace()
    sys.settrace(tracefn)
    foo()
    assert sys.gettrace() == tracefn
    sys.settrace(old_trace)
    assert events == ['call', 'line', 'return']


def test_inject_apply():

    def foo():
        return locals()

    assert inject(a=5).into(foo) == {'a': 5}
    
    
