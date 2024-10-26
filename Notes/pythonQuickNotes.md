# Python Quick Notes

## Basics
- **Data Types**: `int`, `float`, `str`, `list`, `tuple`, `dict`, `set`, `bool`, `NoneType`.
- **Type Casting**: Use `int()`, `float()`, `str()`, `list()`, etc., to convert between types.
- **Basic Operators**: 
  - Arithmetic: `+`, `-`, `*`, `/`, `//` (floor division), `%` (modulus), `**` (exponent).
  - Comparison: `==`, `!=`, `>`, `<`, `>=`, `<=`.
  - Logical: `and`, `or`, `not`.

## Control Flow
- **If Statements**: `if`, `elif`, `else`.
- **Loops**:
  - `for` loop: Used to iterate over sequences (e.g., `for i in range(10):`).
  - `while` loop: Repeats as long as a condition is `True`.

## Functions
- **Defining Functions**: `def function_name(params):` 
- **Return Statement**: `return` to exit and return a result from a function.
- **Lambda Functions**: Anonymous functions with `lambda` syntax (e.g., `lambda x: x + 1`).

## Data Structures
- **Lists**: Ordered, mutable, indexed by positions, created with `[]` (e.g., `my_list = [1, 2, 3]`).
  - List methods: `.append()`, `.extend()`, `.insert()`, `.remove()`, `.pop()`, `.sort()`, `.reverse()`.
- **Tuples**: Ordered, immutable, created with `()` (e.g., `my_tuple = (1, 2, 3)`).
- **Dictionaries**: Key-value pairs, unordered, mutable, created with `{}` (e.g., `my_dict = {'key': 'value'}`).
  - Dict methods: `.get()`, `.keys()`, `.values()`, `.items()`, `.update()`, `.pop()`.
- **Sets**: Unordered, unique elements, created with `{}` (e.g., `my_set = {1, 2, 3}`).
  - Set operations: `.add()`, `.remove()`, `.union()`, `.intersection()`, `.difference()`.

## Object-Oriented Programming (OOP)
- **Classes**: Created with `class ClassName:`.
- **Constructor**: `__init__(self)` method initializes the instance.
- **Instance Variables**: Defined using `self.variable_name`.
- **Inheritance**: Use `class SubClass(ParentClass):`.
- **Encapsulation**: Private variables and methods start with `_` or `__`.
- **Polymorphism**: Methods in a derived class override methods in the base class.

## Modules and Packages
- **Importing Modules**: Use `import module_name` or `from module_name import function_name`.
- **Common Modules**: `math`, `os`, `sys`, `re` (regex), `datetime`, `json`, `random`.

## Exception Handling
- **Try-Except**: 
  ```python
  try:
      # code
  except Exception as e:
      # handle exception
  else:
      # executes if no exception
  finally:
      # always executes
