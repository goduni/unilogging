# Contributing

`unilogging` is a little library, but i'm welcome to new developers to join me.

1) Clone project:

```bash
git clone https://github.com/goduni/unilogging
```

2) Create and activate virtual environment:

```bash
uv venv
source .venv/bin/activate
```

3) Install development dependencies and project itself:

```bash
uv sync --group dev
```



### Running linters and type checking

```bash
just lint
```


### Running tests

To run the tests in your current environment, run the following command:

```bash
just test
```

To run the tests in all supported versions of python, run the following command:

```bash
just test-all
```