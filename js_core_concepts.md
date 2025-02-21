
# JavaScript Core Concepts for Front-End Development Interview Preparation

## 1. Currying & Partial Application

### Currying:
Currying is the process of transforming a function that takes multiple arguments into a sequence of functions, each taking one argument. In other words, currying breaks down a function that takes multiple arguments into a series of functions that each take a single argument.

#### Example:
```javascript
function add(a) {
    return function(b) {
        return a + b;
    };
}

const addFive = add(5);
console.log(addFive(3));  // Output: 8
```

Here, `add(5)` returns a new function that takes one argument and adds it to `5`. This is an example of currying.

### Partial Application:
Partial application is the process of fixing a number of arguments of a function and producing another function that takes the remaining arguments. It's similar to currying, but in partial application, the original function is invoked only once, whereas, in currying, a new function is returned at each step.

#### Example:
```javascript
function multiply(a, b, c) {
    return a * b * c;
}

const multiplyByTwo = multiply.bind(null, 2);
console.log(multiplyByTwo(3, 4));  // Output: 24
```

In this example, we fixed the first argument (`2`), creating a new function that takes the remaining two arguments.

---

## 2. Event Loop, Callbacks, Promises, Async/Await

### Event Loop:
The event loop is a fundamental part of the JavaScript runtime that handles asynchronous operations. JavaScript is single-threaded, meaning it executes one task at a time. The event loop enables JavaScript to perform non-blocking operations by using a combination of callbacks, promises, and async/await.

1. **Call Stack**: This is where JavaScript keeps track of the currently executing function.
2. **Task Queue**: This is where callback functions from asynchronous operations (e.g., `setTimeout`, network requests) wait to be executed.
3. **Event Loop**: Continuously monitors the call stack and task queue. If the call stack is empty, the event loop takes the first callback from the task queue and pushes it onto the call stack for execution.

#### Example:
```javascript
console.log('Start');

setTimeout(() => {
    console.log('Inside setTimeout');
}, 1000);

console.log('End');
```

Output:
```
Start
End
Inside setTimeout
```

### Callbacks:
A callback is a function passed as an argument to another function and is executed after some operation has been completed.

#### Example:
```javascript
function fetchData(callback) {
    setTimeout(() => {
        callback('Data received');
    }, 1000);
}

fetchData((data) => {
    console.log(data);  // Output: Data received
});
```

### Promises:
A promise is an object that represents the eventual completion (or failure) of an asynchronous operation. It has three states:
- **Pending**: Initial state, neither fulfilled nor rejected.
- **Fulfilled**: The operation completed successfully.
- **Rejected**: The operation failed.

#### Example:
```javascript
const promise = new Promise((resolve, reject) => {
    setTimeout(() => {
        resolve('Data received');
    }, 1000);
});

promise.then(data => {
    console.log(data);  // Output: Data received
});
```

### Async/Await:
`async` and `await` are syntactic sugar for working with promises in a more readable way.

#### Example:
```javascript
async function fetchData() {
    const data = await new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve('Data received');
        }, 1000);
    });
    console.log(data);
}

fetchData();  // Output: Data received
```

---

## 3. Prototype & Inheritance

### Prototype:
In JavaScript, every object has a hidden internal property called `[[Prototype]]`, which is a reference to another object. This is used for inheritance. When trying to access a property or method, JavaScript first looks at the object itself, and if it doesn't find it, it looks up the prototype chain.

#### Example:
```javascript
function Person(name) {
    this.name = name;
}

Person.prototype.greet = function() {
    console.log(`Hello, my name is ${this.name}`);
};

const person1 = new Person('Alice');
person1.greet();  // Output: Hello, my name is Alice
```

### Inheritance:
Inheritance allows one object to acquire properties and methods from another. JavaScript uses **prototypal inheritance**: objects inherit directly from other objects.

#### Example:
```javascript
function Animal(name) {
    this.name = name;
}

Animal.prototype.speak = function() {
    console.log(`${this.name} makes a noise.`);
};

function Dog(name) {
    Animal.call(this, name);  // Inherit properties
}

Dog.prototype = Object.create(Animal.prototype);  // Inherit methods
Dog.prototype.constructor = Dog;

Dog.prototype.speak = function() {
    console.log(`${this.name} barks.`);
};

const dog1 = new Dog('Rex');
dog1.speak();  // Output: Rex barks
```

---

## 4. Memory Management and Performance

### Memory Management:
JavaScript has automatic memory management through **garbage collection**, meaning it automatically frees up memory that is no longer in use. Memory management in JavaScript involves:
1. **Memory Allocation**: Memory is allocated when variables, objects, or functions are created.
2. **Memory Use**: Memory is used when the program runs and performs operations.
3. **Memory Release**: Memory is automatically released by the garbage collector when it is no longer needed.

#### Memory Leaks:
A memory leak occurs when memory that is no longer in use is not released. Common causes of memory leaks include:
- Global variables.
- Forgotten event listeners and timers.
- Closures holding on to references unnecessarily.
- Detached DOM elements that are still referenced.

#### Example:
```javascript
let element = document.getElementById('leak');
document.body.removeChild(element);  // Detached from DOM, but still in memory
console.log(element);  // Memory leak as element is still referenced
```

### Performance Optimization:
1. **Minimize Reflow and Repaint**: Reflows occur when the layout of the page changes (e.g., when adding/removing elements). Minimize DOM manipulation to avoid performance degradation.
2. **Use Debouncing and Throttling**: Use debouncing and throttling to optimize functions like scrolling or resizing that trigger multiple events.
3. **Efficient Data Structures**: Use efficient data structures like `Set`, `Map`, and avoid using large arrays when unnecessary.

---

## 5. Memory and Performance Tools

- **Chrome DevTools**: Provides tools to analyze performance and memory usage.
    - **Performance Tab**: Record and view a detailed analysis of your application’s performance over time.
    - **Memory Tab**: Analyze heap snapshots to track memory consumption and identify memory leaks.
    - **Lighthouse**: A tool for auditing the performance, accessibility, and SEO of your web app.

### Heap Snapshots:
Use Chrome DevTools to take heap snapshots to identify which objects are taking up memory.

### Flame Charts:
Use flame charts to visualize how much time is spent in various parts of the application, such as rendering, scripting, or layout recalculations.

---

This document covers key JavaScript concepts such as currying, the event loop, promises, async/await, memory management, and performance optimizations. These concepts are essential for preparing for front-end development interviews, especially when working with React, Redux, and modern JavaScript.
