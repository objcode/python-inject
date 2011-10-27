
import sys

class inject(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, fn):
        from functools import wraps
        @wraps(fn)
        def wrapped(*args, **kwargs):
            print "doing wrap", args, kwargs
            old_trace = sys.gettrace()
            def tracefn(frame, event, arg):
                # define a new tracefn each time, since it needs to
                # call the *current* tracefn if they're in debug mode
                print 'updating locals with', self.kwargs
                frame.f_locals.update(self.kwargs)
                if old_trace:
                    return old_trace(frame, event, arg)
                else:
                    return None

            sys.settrace(tracefn)
            retval = fn(*args, **kwargs)
            sys.settrace(old_trace)
            return retval

        return wrapped

    def into(self, fn, *args, **kwargs):
        return self(fn)(*args, **kwargs)
            
