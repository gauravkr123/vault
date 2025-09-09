# Gaurav's Tools & Scripts

This directory contains various web-based tools and utilities that are hosted on GitHub Pages.

## Available Tools

1. **[Indian Tax Calculator](tax-calculator/)**
   - Calculate gross salary from desired take-home pay
   - Takes into account tax slabs, standard deductions, and EPF
   - Updated for FY 2023-24

## Hosting Information

These tools are hosted at: [https://gauravkr123.github.io/vault/Pages/](https://gauravkr123.github.io/vault/Pages/)

## Directory Structure

```
Pages/
├── index.html          # Main landing page
├── README.md           # This file
└── tax-calculator/     # Tax calculator tool
    ├── index.html
    ├── style.css
    ├── tax-calculator.js
    └── README.md
```

## Adding New Tools

To add a new tool:

1. Create a new directory for your tool
2. Add your tool's files (HTML, CSS, JS, etc.)
3. Update the main `index.html` to include your tool in the grid
4. Update this README.md to document the new tool

## Local Development

To test locally, you can use any static file server. For example, using Python:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000` in your browser.
