# unilogging

A simple library for working with the context of logs.

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/unilogging)
![PyPI - Downloads](https://img.shields.io/pypi/dm/unilogging)
![GitHub License](https://img.shields.io/github/license/goduni/unilogging)
![GitHub Repo stars](https://img.shields.io/github/stars/goduni/unilogging)
[![Telegram](https://img.shields.io/badge/💬-Telegram-blue)](https://t.me/+TvprI2G1o7FmYzRi)

## Quickstart

```bash
pip install unilogging
```

## What Problem Does It Solve?

Many modern Python applications use Dependency Injection (DI), but logging has traditionally relied on using a global logger (e.g., `logging.getLogger(__name__)`). While this simplifies the use of logging, it also introduces a number of complications.

If you're developing a web application, there are situations where you need to understand what happened during a specific request (for example, when an error occurs during that request). To do this, it's common to introduce a concept like `request_id`—a unique identifier assigned to an HTTP request, which allows you to trace all logs related to that request.

This creates a problem: you now need a way to propagate the request_id throughout your application – especially if your application has multiple architectural layers (e.g., infrastructure, service, presentation). Passing request_id (and other context data like `user_id`) explicitly everywhere is problematic, as it leads to a lot of boilerplate and argument duplication in your code, all just to enable proper logging.



### How does Unilogging solve this?

Unilogging helps structure the logging process using Dependency Injection (DI).

For each request to your web application, a separate context is created. You can populate this context with data regardless of the application layer – using DI is all you need.

For example, consider this scenario:

* You generate a `request_id` in a FastAPI middleware (or any other framework you’re using).
* You write a log entry indicating that a certain action was performed, including relevant data (depending on your use case).

Here’s an example using Unilogging:

```python
@app.middleware("http")
async def request_id_middleware(request, call_next):
    logger = await request.state.dishka_container.get(Logger)
    with logger.begin_scope(request_id=uuid.uuid4()):
        response = await call_next(request)
        return response

@app.post("/order")
@inject
async def create_order(
        data: CreateOrderAPIRequest,
        interactor: FromDishka[CreateOrderInteractor]
):
    order_id = await interactor(data)
    return order_id

class CreateOrderInteractor:
    def __init__(self, logger: Logger['CreateOrderInteractor']):
        self.logger = logger
    
    async def __call__(self, data: CreateOrderAPIRequest):
        order = ...
        self.logger.info("Created order", order_id=order.id)
```

```json
{"message": "Created order", "logger_name": "module.path.CreateOrderInteractor", "request_id": "15c71f84-d0ed-49a6-a36e-ea179f0f62ef", "order_id": "15c71f84-d0ed-49a6-a36e-ea179f0f62ef"}
```

You don’t need to pass all this data between the layers of your application – you simply store it in a context that’s accessible throughout the entire application wherever DI is available.



### How do other libraries solve this?

Here we’ll look at how other libraries propose to solve this problem.



### logging (standard library)

Does not support context, and the only way to pass additional data to logs is:

```python
logging.info("user logged in", extra={"user_id": user_id})
```

The problem here is that you have to pass all the required data explicitly – meaning that every function that logs something must accept all necessary data as arguments.

### loguru

This is addressed by creating a new logger object that contains the context:

```python
from loguru import logger

logger_with_request_id = logger.bind(request_id=str(uuid.uuid4))
logger_with_request_and_user_id = logger_with_request_id.bind(user_id=user.id)
```

However, you can’t use this in a Dependency Injection approach – it recreates the logger and doesn’t function as a true logging context in the full sense.



### structlog

This library handles context using `contextvars`, but there are significant issues with this approach.
Implementing context via `contextvars` is not entirely safe, as it relies on thread-local storage.

* Context can leak into other requests if you forget to clear all the context variables used during a request.
* You can lose the request context if you launch an operation in a separate thread within that request.

For synchronous applications, this may be acceptable, but you still need to manually clear the entire context at the start of each new request. In asynchronous applications, the context must remain within the boundaries of `await`, since coroutines execute within a single thread.

Working with context looks like this:


```python
log = structlog.get_logger()

clear_contextvars()
bind_contextvars(a=1, b=2)
log.info("hello")
```
```
event='hello' a=1 b=2
```



## Features

### Logging Contexts and Integration with Dishka

One of the main features of Unilogging is the ability to conveniently pass values into a context, the data from which can later be used by your formatter. This is similar to the extra argument in Python's standard logging.

Unilogging offers new possibilities with a more convenient API. You can populate the context with data at various stages of your application's execution, and logger classes below will pick up this context at any level of the application. This works within the REQUEST-scope. 

Here’s an example to illustrate – a middleware in a FastAPI application that generates a request_id and adds it to the context.

```python
@app.middleware("http")
async def request_id_middleware(request, call_next):
    logger = await request.state.dishka_container.get(Logger)
    with logger.begin_scope(request_id=uuid.uuid4()):
        response = await call_next(request)
        return response
```



### Generic logger name or your own factory (Integration with Dishka)

You can retrieve a logger from the DI container as follows:

```python
class SomeClass:
    def __init__(self, logger: Logger['SomeClass']):
        ...
```

In this case, when using the standard integration with Dishka, a new logger will be created with the name `your_module.path_to_class.SomeClass`. If you don’t need this, you can avoid using a generic logger – in that case, the logger name will be `unilogging.Logger`, or you can pass your own factory into the integration.

The default logger factory in the provider is used so that you can supply your own factory with custom logic for creating standard loggers – for example, if you want logger names to be generated based on different criteria. However, your factory must conform to the `StdLoggerFactory` protocol.

Your factory should follow the protocol below:

```python
class StdLoggerFactory(Protocol):
    def __call__(self, generic_type: type, default_name: str = ...) -> logging.Logger:
        ...
```

Then you can pass it like this:

```python
UniloggingProvider(std_logger_factory=your_factory)
```



### Templating – Injecting values from the context

You can use the built-in log record formatting provided by the library. At the stage of passing the record to the standard logger, it formats the message using `format_map`, injecting the entire current context. This feature is typically used when your logs are output in JSON format.

```python
with logger.begin_context(user_id=user.id):
    logger.info("User {user_id} logged in using {auth_method} auth method", auth_method="telegram")
```
```
INFO:unilogging.Logger:User 15c71f84-d0ed-49a6-a36e-ea179f0f62ef logged in using telegram auth method
```
