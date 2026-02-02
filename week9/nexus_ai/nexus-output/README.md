# Add Two Numbers Utility

This repository contains a small Python script that provides:

- An `add(a, b)` function that returns the sum of two numbers.
- A command‑line interface using `argparse` to add two numbers supplied as arguments.
- A unit test suite using `unittest` that validates the function for positive numbers, negative numbers, and zero values.

## Prerequisites

- Python 3.8 or higher installed on your system.
- No external dependencies are required; the script uses only the Python standard library.

## Installation

1. Clone the repository or copy the files to a directory of your choice.
2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies (there are none, but the command is provided for completeness):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script from the command line, passing the two numbers you want to add:
```bash
python main.py 3 4.5
```
Output:
```
3.0 + 4.5 = 7.5
```

## Running the Tests

Execute the unit tests with:
```bash
python -m unittest main.py
```
All tests should pass.

## License

This code is provided under the MIT License.
