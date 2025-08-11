# A simple algebraic expression evaluator and parser

This package implements a _Pratt parser_ to parse and evaluate mathematical expressions, supporting computation in arbitary bases and a variety of operators as well as parse tree visualization. It provides a class `AlgebraEval` as well as a REPL for usage from the command line. 

## Usage

### As a Command-Line Tool
Run the evaluator interactively:

```bash
python -m pypratt [OPTIONS]
```
The allowed `OPTIONS` are
  - `-b`, `--base BASE`  : Set the numeric base (default: 10)
  - `-t`                 : Enable parse tree display
  - `-v`                 : Enable verbose mode

For example, 
```
vatsal@algebra>python -m pypratt -t 
Welcome to the Algebra Evaluator
You can enter algebraic expressions at the prompt or press enter to exit.
Parse tree display enabled.
>>> 1 + 2 * (3 + 4)
1 + 2 * (3 + 4) = 15

 [+]
  ├── 1
  └── [*]
       ├── 2
       └── [+]
            ├── 3
            └── 4

```

### As a Python Module
The class `AlgebraEval` class can be imported as:
```python
from pypratt import AlgebraEval
```
An object can be initialized with an optional argument `base`: 
```python
evaluator = AlgebraEval(base=10)
```
Expressions are then evaluated by passing them as strings to the `evaluate` method. For instance, 
```python
result = evaluator.evaluate("2 + 3 * 4")
```

## Logging
Logs are written to `pypratt.log` in the current directory.

