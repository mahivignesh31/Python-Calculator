import math
import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_banner():
    print("=" * 45)
    print("          Python Calculator")
    print("=" * 45)


def show_menu():
    print("\nWhat do you want to do?")
    print("  1. Add")
    print("  2. Subtract")
    print("  3. Multiply")
    print("  4. Divide")
    print("  5. Modulus (remainder)")
    print("  6. Chain calculation  (e.g. 5 + 3 * 2 - 1)")
    print("  7. Power")
    print("  8. Square root")
    print("  9. Logarithm")
    print(" 10. Trigonometry (sin, cos, tan)")
    print(" 11. Factorial")
    print(" 12. View history")
    print(" 13. Clear history")
    print("  0. Exit")
    print()


# ----- input helpers -----

def ask_number(label):
    while True:
        raw = input(f"  {label}: ").strip()
        try:
            return float(raw)
        except ValueError:
            print("  That doesn't look like a number. Try again.")


def ask_int(label, minimum=1):
    while True:
        raw = input(f"  {label}: ").strip()
        try:
            val = int(raw)
            if val < minimum:
                print(f"  Needs to be at least {minimum}.")
            else:
                return val
        except ValueError:
            print("  Enter a whole number.")


def ask_operator(after_which):
    while True:
        op = input(f"  Operator after {after_which} number (+  -  *  /): ").strip()
        if op in ('+', '-', '*', '/'):
            return op
        print("  Use one of: +  -  *  /")


def ordinal(n):
    if 11 <= n <= 13:
        return f"{n}th"
    return f"{n}{['th','st','nd','rd','th','th','th','th','th','th'][n % 10]}"


def get_numbers(label, count):
    nums = []
    for i in range(1, count + 1):
        nums.append(ask_number(f"  Enter {ordinal(i)} number"))
    return nums


# ----- math helpers -----

def safe_divide(a, b):
    """Low-level division helper used by apply() and do_divide()."""
    if b == 0:
        raise ZeroDivisionError("Can't divide by zero.")
    return a / b


def do_mod(a, b):
    if b == 0:
        raise ZeroDivisionError("Can't mod by zero.")
    return a % b


def apply(a, op, b):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/': return safe_divide(a, b)


def evaluate(numbers, ops):
    # respect precedence: * and / before + and -
    nums = list(numbers)
    operators = list(ops)

    i = 0
    while i < len(operators):
        if operators[i] in ('*', '/'):
            result = apply(nums[i], operators[i], nums[i + 1])
            nums[i] = result
            del nums[i + 1]
            del operators[i]
        else:
            i += 1

    total = nums[0]
    for op, n in zip(operators, nums[1:]):
        total = apply(total, op, n)
    return total


def fmt(n):
    if isinstance(n, float) and n.is_integer():
        return str(int(n))
    return f"{n:.10g}"


# ----- history -----

history = []

def save(expr, result):
    history.append(f"{expr} = {fmt(result)}")

def print_history():
    print()
    if not history:
        print("  No calculations yet.")
        return
    print("  Last 10 calculations:")
    for i, entry in enumerate(history[-10:], 1):
        print(f"  {i}. {entry}")
    print()


# ----- print result -----

def show(expr, result):
    print(f"\n  {expr} = {fmt(result)}\n")


# ----- operations -----

def do_add():
    count = ask_int("How many numbers do you want to add? (min 2)", minimum=2)
    nums = get_numbers("add", count)
    result = sum(nums)
    expr = " + ".join(fmt(n) for n in nums)
    show(expr, result)
    save(expr, result)


def do_subtract():
    count = ask_int("How many numbers? (min 2)", minimum=2)
    nums = get_numbers("subtract", count)
    result = nums[0]
    for n in nums[1:]:
        result -= n
    expr = " - ".join(fmt(n) for n in nums)
    show(expr, result)
    save(expr, result)


def do_multiply():
    count = ask_int("How many numbers? (min 2)", minimum=2)
    nums = get_numbers("multiply", count)
    result = 1
    for n in nums:
        result *= n
    expr = " * ".join(fmt(n) for n in nums)
    show(expr, result)
    save(expr, result)


def do_divide():
    count = ask_int("How many numbers (chain divide)? (min 2)", minimum=2)
    nums = get_numbers("divide", count)
    result = nums[0]
    for n in nums[1:]:
        result = safe_divide(result, n)  # fixed: was do_divide(result, n)
    expr = " / ".join(fmt(n) for n in nums)
    show(expr, result)
    save(expr, result)


def do_modulus():
    a = ask_number("Enter number")
    b = ask_number("Enter divisor")
    result = do_mod(a, b)
    expr = f"{fmt(a)} % {fmt(b)}"
    show(expr, result)
    save(expr, result)


def do_chain():
    print("\n  Chain mode: enter numbers and operators one by one.")
    print("  Precedence is respected (* and / before + and -).\n")
    count = ask_int("How many numbers in your expression? (min 2)", minimum=2)

    numbers = []
    ops = []

    for i in range(1, count + 1):
        numbers.append(ask_number(f"  Enter {ordinal(i)} number"))
        if i < count:
            ops.append(ask_operator(ordinal(i)))

    result = evaluate(numbers, ops)

    # build display string with symbols
    sym = {'*': '*', '/': '/', '+': '+', '-': '-'}
    parts = [fmt(numbers[0])]
    for op, n in zip(ops, numbers[1:]):
        parts.append(sym[op])
        parts.append(fmt(n))
    expr = " ".join(parts)

    # show steps
    print("\n  Steps:")
    nums2 = list(numbers)
    ops2 = list(ops)
    step = 1
    i = 0
    while i < len(ops2):
        if ops2[i] in ('*', '/'):
            r = apply(nums2[i], ops2[i], nums2[i+1])
            print(f"  {step}. {fmt(nums2[i])} {ops2[i]} {fmt(nums2[i+1])} = {fmt(r)}")
            nums2[i] = r
            del nums2[i+1]
            del ops2[i]
            step += 1
        else:
            i += 1
    total = nums2[0]
    for op, n in zip(ops2, nums2[1:]):
        r = apply(total, op, n)
        print(f"  {step}. {fmt(total)} {op} {fmt(n)} = {fmt(r)}")
        total = r
        step += 1

    show(expr, result)
    save(expr, result)


def do_power():
    base = ask_number("Base")
    exp = ask_number("Exponent")
    result = base ** exp
    expr = f"{fmt(base)} ^ {fmt(exp)}"
    show(expr, result)
    save(expr, result)


def do_sqrt():
    a = ask_number("Number")
    if a < 0:
        raise ValueError("Can't take square root of a negative number.")
    result = math.sqrt(a)
    expr = f"sqrt({fmt(a)})"
    show(expr, result)
    save(expr, result)


def do_log():
    a = ask_number("Number")
    if a <= 0:
        raise ValueError("Number must be positive for log.")
    print("  Base options: press Enter for base 10, type 'e' for natural log, or enter any number.")
    raw = input("  Base: ").strip()
    if raw == '' or raw == '10':
        base = 10
        expr = f"log10({fmt(a)})"
    elif raw.lower() == 'e':
        base = math.e
        expr = f"ln({fmt(a)})"
    else:
        base = float(raw)
        if base <= 0 or base == 1:
            raise ValueError("Base must be positive and not 1.")
        expr = f"log_{fmt(base)}({fmt(a)})"
    result = math.log(a, base)
    show(expr, result)
    save(expr, result)


def do_trig():
    print("  Functions: sin, cos, tan")
    func = input("  Choose function: ").strip().lower()
    if func not in ('sin', 'cos', 'tan'):
        raise ValueError("Pick sin, cos, or tan.")
    angle = ask_number("Angle value")
    unit = input("  Unit (deg or rad): ").strip().lower()
    if unit not in ('deg', 'rad'):
        raise ValueError("Unit must be deg or rad.")
    rad = math.radians(angle) if unit == 'deg' else angle
    if func == 'tan' and math.isclose(math.cos(rad), 0):
        raise ValueError("tan is undefined at this angle.")
    funcs = {'sin': math.sin, 'cos': math.cos, 'tan': math.tan}
    result = funcs[func](rad)
    label = f"{angle}°" if unit == 'deg' else f"{angle} rad"
    expr = f"{func}({label})"
    show(expr, result)
    save(expr, result)


def do_factorial():
    a = ask_number("Enter a whole number")
    if a < 0 or not float(a).is_integer():
        raise ValueError("Factorial needs a non-negative whole number.")
    result = math.factorial(int(a))
    expr = f"{int(a)}!"
    show(expr, result)
    save(expr, result)


# ----- main -----

def main():
    clear_screen()
    show_banner()

    actions = {
        '1': do_add,
        '2': do_subtract,
        '3': do_multiply,
        '4': do_divide,
        '5': do_modulus,
        '6': do_chain,
        '7': do_power,
        '8': do_sqrt,
        '9': do_log,
        '10': do_trig,
        '11': do_factorial,
    }

    while True:
        show_menu()
        choice = input("Your choice: ").strip()
        print()

        if choice == '0':
            print("Bye!")
            break
        elif choice == '12':
            print_history()
        elif choice == '13':
            history.clear()
            print("  History cleared.")
        elif choice in actions:
            try:
                actions[choice]()
            except (ZeroDivisionError, ValueError) as e:
                print(f"\n  Error: {e}\n")
        else:
            print("  Invalid choice. Pick a number from the menu.")

        input("  Press Enter to continue...")
        clear_screen()
        show_banner()


if __name__ == "__main__":
    main()
