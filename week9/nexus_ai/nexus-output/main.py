import argparse
import unittest


def add(a, b):
    """Return the sum of a and b."""
    return a + b


def _parse_number(value):
    try:
        return float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid number: {value}")


def main():
    parser = argparse.ArgumentParser(description="Add two numbers.")
    parser.add_argument("a", type=_parse_number, help="First number")
    parser.add_argument("b", type=_parse_number, help="Second number")
    args = parser.parse_args()
    result = add(args.a, args.b)
    print(f"{args.a} + {args.b} = {result}")


class TestAddFunction(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(10.5, 4.5), 15.0)

    def test_negative_numbers(self):
        self.assertEqual(add(-2, -3), -5)
        self.assertEqual(add(-10, 5), -5)

    def test_zero_values(self):
        self.assertEqual(add(0, 0), 0)
        self.assertEqual(add(0, 5), 5)
        self.assertEqual(add(5, 0), 5)


if __name__ == "__main__":
    main()
