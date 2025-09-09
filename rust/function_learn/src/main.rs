fn main() {
    println!("Hello, world!");
    // data_type();
    for i in 1..100 {
        if i % 2 == 0 {
            println!("add(1 + {}): {}", i, add(1, i));
        }
    }
}

// fn data_type() {
//     let a: i32 = 42;
//     let b: f64 = 3.14;
//     let c: bool = true;
//     let d: char = 'R';
//     let e: &str = "Hello";      // string slice
//     let f: String = String::from("World"); // heap string
//     println!("{} {} {} {} {} {}", a, b, c, d, e, f);
// }

// fn loop_iteration() {
//     if n % 2 == 0 {
//         println!("Even");
//     } else {
//         println!("Odd");
//     }

//     let mut count = 0;
//     while count < 3 {
//         println!("count = {}", count);
//         count += 1;
//     }

//     for i in 1..4 {  // range 1 to 3
//         println!("for loop i = {}", i);
//     }

//     let mut x = 0;
//     loop {
//         x += 1;
//         if x == 3 {
//             println!("Breaking at {}", x);
//             break;
//         }
//     }
// }

fn add(x: i32, y: i32) -> i32 {
    x + y  // last expression = return
}