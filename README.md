# functionfaker
Lightweight [Decorator to cache (memoize) function calls](https://github.com/wsijp/functionfaker) and replay responses for expensive computations and API requests.

[Pip installable](https://pypi.org/project/functionfaker/) via `pip install functionfaker`  

Functionfaker offers lightweight and easy to understand function (and method) caching, similar to some of the functionality of the [Joblib](https://joblib.readthedocs.io/en/latest/) package. A function response is recorded once and then replayed from cache from thereon. This allows for unit testing applications with API calls without actaully calling the API. It can also speed up prototyping of computationally expensive code. Functionfaker consists of simple code, and provides a single decorator for your functions and methods, as shown in the following "hello world" example.

```
from functionfaker import response_player
import os
```
Add the `response_player` decorator to an example function called `add`:

```
@response_player()
def add(x, y):
    return x + y
```

This will not affect the function `add` until you set an environment variable to `RECORD`:

```
# enter record mode, to record function responses.
os.environ['RECORD'] = "record"
```

Call the `add` function a few times:

```
# Clear the stored function responses
if os.path.exists('responses.p'):
    os.remove('responses.p')
# call the add function to record some responses.
add(1,2)
add(1,y=3)
add(1,3)
add(2,1)
```
```Recording response function "add"
Recording response function "add"
Recording response function "add"
Recording response function "add"
```
Set `replay` mode via the environment variable:

```
# enter replay mode, so that function will not run, but return stored values instead.
os.environ['RECORD'] = "replay"
```

Call the `add` function again, with arguments that it has already seen:

```
result = add(1,2)
print("The saved result of adding 1 and 2 using function 'add' is %d"%result)
```
```
Faking function "add". Response found
The saved result of adding 1 and 2 using function 'add' is 3
```

The outputs for these inputs (1,2) are now read from cache.

Some funtion arguments might be irrelevant or difficult to serialize. To ignore these arguments, provide the `args2ignore` argument as a list of integers to the `response_player` decorator, where the integers represent the index in the argument list.

Default function response storage is in a simple Pickle file `responses.p`. To use your own storage system, provide a class derived from `BaseStore` class with an `update` and `get_response` method. An object of this class is then provided as the `store` argument to the `response_player` decorator.
