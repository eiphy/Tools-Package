# This is the wrapper for the tool.
import add_self
import del_event
import stdize as std
import secollect


# For standardization
def stdize(filer, filew):
    error = std.stdize(filer, filew)

# For adding selfloop
def selfloop(statec, eventc, filew, mode=0, filer='None'):
    error = add_self.add_self(statec, eventc, filew, mode, filer)

# For delete event
def delevent(eventc, filename):
    del_event.del_event(eventc, filename)

# For collect the states and events
def stateEcollect(filename, filew='None', mode=0):
    secollect.secolle(filename, filew, mode)