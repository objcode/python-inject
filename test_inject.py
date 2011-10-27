
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
    
    
@inject(a='cat')
def test_binding_order(a=6):
    assert a == 'cat'

def test_inject_works_with_exception():
    class MyException(Exception): pass
    
    @inject(bar=1)
    def foo():
        print locals()
        assert locals() == dict(bar=1, MyException=MyException)
        raise MyException('hi')

    @inject(baz=2)
    def fuz():
        return locals() == dict(baz=2, MyException=MyException)

    # if inject doesn't clean up correctly it will leak a tracefn
    try:
        foo()
        assert False, "foo() was supposed to raise an exception"
    except MyException, e:
        assert True, "foo raised an exception correctly"

    assert fuz(), "and the tracefn was cleaned up correctly"

def test_inject_cleans_up_tracefn_on_except():
    import sys
    old_trace = sys.gettrace()
    @inject(a=5)
    def foo():
        raise Exception()

    try:
        foo()
        assert False, "should have raised an exception"
    except:
        pass
    assert sys.gettrace() == old_trace
    sys.settrace(old_trace)
    
            
