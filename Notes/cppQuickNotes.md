# C++ Quick Notes

## Basics
- **Data Types**: `int`, `float`, `double`, `char`, `bool`, `void`
- **Modifiers**: `signed`, `unsigned`, `short`, `long`
- **Constants**: `const`, `constexpr` (evaluated at compile-time)

## Operators
- **Arithmetic**: `+`, `-`, `*`, `/`, `%`
- **Relational**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Logical**: `&&`, `||`, `!`
- **Bitwise**: `&`, `|`, `^`, `~`, `<<`, `>>`
- **Assignment**: `=`, `+=`, `-=`, `*=`, `/=`, `%=`, `<<=`, `>>=`, `&=`, `|=`, `^=`
- **Ternary**: `condition ? expr1 : expr2`

## Control Structures
- **Conditionals**: `if`, `else if`, `else`, `switch`
- **Loops**: `for`, `while`, `do-while`
- **Loop Control**: `break`, `continue`

## Functions
- **Syntax**: `return_type function_name(parameters) { /* code */ }`
- **Default Arguments**: Defined in function prototype, e.g., `void foo(int x = 10)`
- **Function Overloading**: Functions with the same name but different parameters
- **Inline Functions**: `inline` keyword for small, frequently called functions
- **Lambda Expressions**: `[capture](parameters) { /* code */ };`

## Pointers and References
- **Pointers**: `int* ptr = &var;` // Holds address of a variable
- **Dereferencing**: `*ptr` to access the value at the address
- **Reference**: `int& ref = var;` // Alias for a variable
- **`nullptr`**: Used to initialize pointers with null

## Memory Management
- **Dynamic Allocation**: `new` and `delete` for single objects; `new[]` and `delete[]` for arrays
- **Smart Pointers**: `std::unique_ptr`, `std::shared_ptr`, `std::weak_ptr` (C++11)

## Object-Oriented Programming (OOP)
- **Classes**: Define with `class ClassName { public: /* methods & attributes */ };`
- **Access Specifiers**: `public`, `protected`, `private`
- **Constructors & Destructors**: `ClassName()` and `~ClassName()`
- **Copy Constructor**: `ClassName(const ClassName &obj)`
- **Operator Overloading**: Define operators for custom classes, e.g., `operator+`
- **Inheritance**: `class Derived : public Base { /* ... */ };`
- **Polymorphism**: Use `virtual` functions and `override` (C++11)
- **Abstract Classes**: Contain pure virtual functions, `virtual void func() = 0;`

## Standard Template Library (STL)
- **Containers**: `vector`, `list`, `deque`, `stack`, `queue`, `map`, `set`, etc.
- **Iterators**: `begin()`, `end()`, `rbegin()`, `rend()`
- **Algorithms**: `sort`, `find`, `reverse`, `count`, `accumulate`, `binary_search`
- **Function Objects (Functors)**: Objects that act like functions, often used with STL algorithms

## Exception Handling
- **Syntax**:
  ```cpp
  try { /* code that may throw */ }
  catch (const std::exception &e) { /* handle error */ }
