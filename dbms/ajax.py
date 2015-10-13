from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register


def multiply(request, a, b):
    dajax = Dajax()
    result = int(a) * int(b)
    dajax.assign('#result','value',str(result))
    return dajax.json()

def say_hello(req):
    dajax = Dajax()
    dajax.alert("Hello World!")
    return dajax.json()

    
