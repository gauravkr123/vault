// const readline = require('readline');

// const rl = readline.createInterface({
//   input: process.stdin,
//   output: process.stdout
// });

// rl.question("What's your name? ", (answer) => {
//   console.log(`Hello, ${answer}!`);
//   rl.close();
// });
let inputData = [];
// rl.on("line", (input) => {
//     if(input === "END"){
//         rl.close();
//     }
//     else{
//         console.log(input);
//         inputData.push(input);
//     }
// });

// rl.on("close", () => {
//     console.log("Input closed");
//     console.log(inputData.join('\n'));
// });


// Enable input from the user
process.stdin.setEncoding('utf-8');
process.stdout.setEncoding('utf-8');
const EventEmitter = require("events");

const myEmitter = new EventEmitter;

myEmitter.on("fakeData", (data) => {
    console.log("Custom Event: fakeEvent has been triggered");
    console.log(`Fake data: ${data} detected and will not be processed!!`);
    process.stdout.write(data.replace("&", "#&"));
})


console.log('Please enter your name:');

// Read data from standard input
process.stdin.on('data', (data) => {
    if(data.trim() === "exit"){
        process.exit(); // Exit the process after receiving input
    }
    else if(data.trim().includes("&")){
        myEmitter.emit("fakeData", data.trim());
    }else{
        console.log(`Hello, ${data.trim()}!`);
    }
});

