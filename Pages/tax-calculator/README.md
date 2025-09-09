# Indian Tax Calculator

A simple, browser-based Indian tax calculator that helps estimate gross salary based on desired take-home pay. The calculator takes into account:
- Standard deduction
- Tax slabs
- Surcharge rates
- Education cess
- EPF deductions

## Features

- Calculate estimated annual gross income from desired monthly take-home salary
- Real-time calculations without server requirements
- Responsive design that works on all devices
- Detailed breakdown of:
  - Annual and monthly gross income
  - Tax calculations
  - EPF deductions

## Live Demo

Visit [https://gauravkr123.github.io/vault/Pages/tax-calculator](https://gauravkr123.github.io/vault/Pages/tax-calculator)

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/gauravkr123/vault.git
```

2. Navigate to the tax calculator directory:
```bash
cd vault/Pages/tax-calculator
```

3. Open `index.html` in your web browser or use a local development server.

## Deployment to GitHub Pages

1. Ensure all files are in the correct directory structure:
   ```
   vault/
   └── Pages/
       └── tax-calculator/
           ├── index.html
           ├── style.css
           ├── tax-calculator.js
           └── README.md
   ```

2. Commit your changes:
   ```bash
   git add .
   git commit -m "Add tax calculator"
   git push origin main
   ```

3. Configure GitHub Pages:
   - Go to your repository settings on GitHub
   - Navigate to the "Pages" section
   - Select the `main` branch as the source
   - Save the settings

Your site will be published at `https://gauravkr123.github.io/vault/Pages/tax-calculator/`

## How it Works

The calculator uses a binary search algorithm to estimate the gross income that would result in your desired take-home pay. It takes into account:

1. The latest tax slabs for India (as of 2023-24)
2. Standard deduction of ₹75,000
3. Surcharge rates based on income levels
4. Education and health cess (4%)
5. EPF deductions based on Basic + DA percentage

## Technologies Used

- HTML5
- CSS3 with Bootstrap 5
- Vanilla JavaScript
- Indian Currency formatting using `Intl.NumberFormat`

## Contributing

Feel free to open issues or submit pull requests if you find any bugs or have suggestions for improvements.

## License

This project is open source and available under the MIT License.
