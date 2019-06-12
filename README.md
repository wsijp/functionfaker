# functionfaker
Cache (memoize) and replay responses for expensive function and API calls.

[Pip installable][https://pypi.org/project/functionfaker/] via `pip install functionfaker`  

Functionfaker provides caching for functions and methods, where a function response is recorded once and then replayed from cache from thereon. This allows for unit testing applications with API calls without actaully calling the API. It can also speed up prototyping of computationally expensive code. Functionfaker consists of simple code, and provides a single decorator for your functions and methods, as shown in the following "hello world" example.

```
from functionfaker import response_player
import os
```
Add the `response_player` decorator to an example function called `add`:

```
@response_player(default_return = None)
def add(x, y):
    return x + y
```

Then set RECORD mode by setting the environment variable:

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

The results are now read from cache.
