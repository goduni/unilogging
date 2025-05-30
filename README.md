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
