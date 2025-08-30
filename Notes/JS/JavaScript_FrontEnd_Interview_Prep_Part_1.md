
# Part 1: Core JavaScript Topics for Front-End Developer Interview

## 1. Currying & Partial Application

**Currying** and **Partial Application** are advanced techniques in functional programming that deal with transforming functions in a way that increases their flexibility and reuse.

### Currying:
Currying is a technique where a function is transformed into a series of functions, each accepting a single argument. Instead of a function that takes multiple arguments at once, it returns a new function that takes the next argument until all arguments are provided.

### Example:
```javascript
function add(a) {
    return function(b) {
        return a + b;
    };
}

const addFive = add(5);
console.log(addFive(3)); // Output: 8
```

In the example, `add` is curried. First, it takes the argument `a`, and then it returns another function that takes `b`.

### Benefits of Currying:
- **Reusability**: You can easily create new functions by pre-filling arguments.
- **Code Composition**: Functions can be composed by chaining smaller ones.

### Partial Application:
Partial application refers to creating a new function by fixing some (but not all) arguments of the original function. The resulting function can then be called with the remaining arguments.

### Example:
```javascript
function multiply(a, b, c) {
    return a * b * c;
}

const multiplyByTwo = multiply.bind(null, 2);
console.log(multiplyByTwo(3, 4)); // Output: 24
```

In the example, `multiplyByTwo` is a partially applied function where `a` is fixed to `2`, and `b` and `c` can be supplied later.

### Key Differences:
- **Currying**: Transforms a function so it takes one argument at a time.
- **Partial Application**: Pre-fixes some arguments but still allows multiple arguments in subsequent calls.

---

## 2. Event Loop, Callbacks, Promises, and Async/Await

### Event Loop:
JavaScript is single-threaded but has mechanisms to handle asynchronous code via an event-driven model. The **Event Loop** is at the heart of JavaScript’s concurrency model, allowing it to handle asynchronous tasks like HTTP requests, timers, or DOM events.

- **Call Stack**: Keeps track of all the function calls.
