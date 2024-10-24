
# Part 2: Core JavaScript Topics for Front-End Developer Interview

## 2. Event Loop, Callbacks, Promises, and Async/Await (Continued)

### Callbacks:
A **callback** is a function passed as an argument to another function, which is executed once an operation has finished. Callbacks are commonly used in asynchronous code, such as handling HTTP requests or file I/O.

#### Example:
```javascript
function fetchData(callback) {
    setTimeout(() => {
        const data = { name: 'John', age: 30 };
        callback(data);
    }, 1000);
}

fetchData((result) => {
    console.log('Data:', result);
});
```

In the example, `fetchData` accepts a callback function, which is executed after 1 second when the data is ready.

#### Issues with Callbacks:
While callbacks are effective, they can lead to a problem known as **callback hell**, where nested callbacks become difficult to read and maintain.

### Promises:
**Promises** are an improvement over callbacks, designed to handle asynchronous operations in a cleaner, more structured way. A promise represents a value that may be available now, in the future, or never.

- **Pending**: The initial state; the operation is not complete.
- **Fulfilled**: The operation completed successfully.
- **Rejected**: The operation failed.

#### Example:
```javascript
const fetchData = new Promise((resolve, reject) => {
    setTimeout(() => {
        const data = { name: 'John', age: 30 };
        resolve(data);
    }, 1000);
});

fetchData.then((result) => {
    console.log('Data:', result);
}).catch((error) => {
    console.error('Error:', error);
});
```

#### Chaining Promises:
Promises can be chained to avoid deeply nested callbacks.

```javascript
fetchData
    .then((result) => {
        console.log('Data:', result);
        return new Promise((resolve) => setTimeout(() => resolve('Processed Data'), 1000));
    })
    .then((processedData) => {
        console.log('Processed:', processedData);
    });
```

### Async/Await:
**Async/Await** is built on top of promises and provides a cleaner syntax for handling asynchronous code. It allows you to write asynchronous code that looks synchronous.

- **`async`**: Marks a function as asynchronous.
- **`await`**: Pauses execution of the function until the promise is resolved.

#### Example:
```javascript
async function fetchData() {
    const result = await new Promise((resolve) => {
        setTimeout(() => resolve({ name: 'John', age: 30 }), 1000);
    });
    console.log('Data:', result);
}

fetchData();
```

In this example, `await` pauses the function execution until the promise resolves.

---

## 3. Prototype & Inheritance

JavaScript is a prototype-based language, meaning that inheritance is achieved through prototypes. Every object in JavaScript has a prototype, which is another object it inherits properties and methods from.

### Prototypes:
When you access a property or method on an object, JavaScript first checks the object itself. If the property doesn't exist, it looks at the object's **prototype**. This continues up the prototype chain.

#### Example:
```javascript
const animal = {
    eats: true
};

const dog = Object.create(animal);
console.log(dog.eats); // Output: true
```

Here, `dog` inherits the `eats` property from `animal` through its prototype.

### Constructor Functions and Prototypes:
In traditional object-oriented languages, inheritance is handled via classes. In JavaScript, you can achieve a similar effect using **constructor functions** and prototypes.

#### Example:
```javascript
function Animal(name) {
    this.name = name;
}

Animal.prototype.speak = function() {
    console.log(`${this.name} makes a sound.`);
};

const dog = new Animal('Dog');
dog.speak(); // Output: Dog makes a sound.
```

In this example, `Animal` is a constructor function, and its prototype has a `speak` method. The `dog` object inherits this method.

### Class Syntax (ES6):
With ES6, JavaScript introduced the `class` syntax to simplify working with prototypes and inheritance.

#### Example:
```javascript
class Animal {
    constructor(name) {
        this.name = name;
    }

    speak() {
        console.log(`${this.name} makes a sound.`);
    }
}

class Dog extends Animal {
    speak() {
        console.log(`${this.name} barks.`);
    }
}

const dog = new Dog('Dog');
dog.speak(); // Output: Dog barks.
```

In this example, `Dog` extends `Animal`, inheriting its properties and methods, while overriding the `speak` method.

---
