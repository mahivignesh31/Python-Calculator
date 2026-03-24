# Python Calculator

A command-line calculator built in Python that supports basic and advanced math operations.

## Features

- **Basic operations** — Add, Subtract, Multiply, Divide, Modulus
- **Multi-number support** — Add or multiply 3, 4, 5... as many numbers as you want at once
- **Chain calculation** — Mix different operators in one expression (e.g. `5 + 3 * 2 - 1`) with correct precedence
- **Advanced operations** — Power, Square Root, Logarithm (base 10, natural, custom), Trigonometry (sin/cos/tan), Factorial
- **Step-by-step breakdown** — Chain mode shows each calculation step
- **History** — View your last 10 calculations or clear them anytime

## Requirements

- Python 3.x
- No external libraries needed (uses built-in `math` and `os` only)

## How to Run

```bash
python "Python Calculator.py"
```

## Usage

When you run the script, a menu appears with all available operations. Just enter the number for the operation you want, then follow the prompts to enter your numbers.

**Example — Chain calculation:**
```
How many numbers? 4
1st number: 10
Operator: +
2nd number: 5
Operator: *
3rd number: 3
Operator: -
4th number: 2

Steps:
1. 5 * 3 = 15
2. 10 + 15 = 25
3. 25 - 2 = 23

Result: 23
```

## Operations Menu

| No. | Operation       |
|-----|----------------|
| 1   | Add            |
| 2   | Subtract       |
| 3   | Multiply       |
| 4   | Divide         |
| 5   | Modulus        |
| 6   | Chain Calc     |
| 7   | Power          |
| 8   | Square Root    |
| 9   | Logarithm      |
| 10  | Trigonometry   |
| 11  | Factorial      |
| 12  | View History   |
| 13  | Clear History  |
| 0   | Exit           |
