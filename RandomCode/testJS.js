// Partial application
const multiply = (a, b, c) => a * b * c;
const multiplyByTwo = multiply.bind(null, 2);
// console.log(multiplyByTwo(3, 4)); // Output: 24

// Currying
const curriedMultiply = a => b => c => a * b * c;
const multiplyByTwoCurried = curriedMultiply(2);
// console.log(multiplyByTwoCurried(3)(4)); // Output: 24

function testPromise(testValue) {
        return new Promise((resolve, reject) => {
            if(testValue === "value1"){
                resolve("Hi this test was a success!");
            }
            else{
                reject("Failed for the given value: " + testValue);
            }
        });
}

const refToPromise = (value) => testPromise(value)
    .then((response)=> {
        console.log(response);
    })
    .catch((error) => {
        console.log(error);
    });

// refToPromise("value1");

// refToPromise("value2");


let arr = new Array(10).fill().map((count = 1, idx) => Array(idx).fill().map(() => count = count*2));
// arr.forEach(a => console.log(a));


class Person {
    constructor(name, age){
        this.name = name;
        this.age = age;
        this.gender = "NA";
    }

    setGender(gender){
        this.gender = gender;
    }

    showDetails(){
        console.log("Name:" + this.name +"\nAge: " + this.age + "\nGender: "+ this.gender);
    }
}

let p1 = new Person("Tenku", 23);
// p1.showDetails();
// p1.setGender("Male");
// p1.showDetails();

class Man extends Person{
    #ego;
    constructor(name, age){
        super(name, age);
        this.#ego = 100;
        this.setGender("Male");
    }

    getEgoValue(){
        return this.#ego;
    }
}

let m1 = new Man("Kaku", 26);
let m2 = new Person("Luna", 32);
m1.showDetails();
Man.prototype.sayHello = function (){
    console.log(`Hi my name is ${this.name}!`);
}

m1.sayHello();
// m2.sayHello(); //this fails because the prototype isset only to Man not to person 
console.log(m1.getEgoValue());


// script.js
const args = process.argv.slice(2); // Skip first two arguments (node and script path)
console.log(`Hello, ${args[0]}!`);

// Run with: node script.js YourName
