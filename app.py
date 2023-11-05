import budget
from budget import create_spend_chart
import os
import sys
import random
from datetime import datetime, timedelta

# Define ANSI color codes
GREEN, YELLOW, BLUE, RED, RESET = '\033[92m', '\033[93m', '\033[94m', '\033[91m', '\033[0m'


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def cprint(msg, color):
    print(f"{color}{msg}{RESET}")


def input_colored(prompt, color):
    return input(f"{color}{prompt}{RESET}").strip()


def print_menu(options, color=BLUE):
    clear()
    cprint("Budget App\n-----------", color)
    [cprint(f"{i}. {option}", color) for i, option in enumerate(options, 1)]
    print()


def get_choice(options):
    while True:
        try:
            choice = int(input_colored("Choice: ", BLUE))
            if 1 <= choice <= len(options): return choice
            else: cprint(f"Enter 1-{len(options)}.", RED)
        except ValueError:
            cprint("Enter a number.", RED)


def overview(categories):
    total_balance = sum(c.get_balance() for c in categories)
    cprint("Budget Overview\n---------------", YELLOW)
    for c in categories:
        pct = (c.get_balance() / total_balance * 100) if total_balance else 0
        color = GREEN if pct > 50 else RED if pct < 25 else YELLOW
        cprint(f"{c.name}: ${c.get_balance():.2f} ({pct:.1f}%)", color)
    cprint(f"Total: ${total_balance:.2f}", GREEN)


def add_trans(categories, type):
    category_name = input_colored("Category: ", YELLOW).lower()
    category = next((c for c in categories if c.name.lower() == category_name),
                    None)
    if category:
        amount = float(input_colored(f"Amount for {type}: ", YELLOW))
        description = input_colored("Description: ", YELLOW)
        if type == 'income':
            category.deposit(amount, description)
        else:
            category.withdraw(amount, description)
        cprint(
            f"{type.capitalize()} of ${amount:.2f} added to '{category_name}'.",
            GREEN)
    else:
        cprint(f"'{category_name}' not found.", RED)


def view_ledger(categories):
    name = input_colored("Category: ", YELLOW)
    cat = next((c for c in categories if c.name == name), None)
    cprint(cat if cat else f"'{name}' not found.", GREEN if cat else RED)


def list_categories(categories):
    return ["Categories:"] + [f"- {c.name}"
                              for c in categories] if categories else [
                                  "No categories."
                              ]


def add_category(categories):
    name = input_colored("Name: ", YELLOW)
    if name:
        categories.append(budget.Category(name))
        cprint(f"Added '{name}'.", GREEN)
    else:
        cprint("Empty name.", RED)


def edit_category(categories):
    current_name = input_colored("Current name: ", YELLOW)
    cat = next((c for c in categories if c.name == current_name), None)
    if cat:
        new_name = input_colored("New name: ", YELLOW)
        if new_name:
            cat.name = new_name
            cprint(f"'{current_name}' updated to '{new_name}'.", GREEN)
        else:
            cprint("Empty name.", RED)
    else:
        cprint(f"'{current_name}' not found.", RED)


def delete_category(categories):
    name = input_colored("Name: ", YELLOW)
    cat = next((c for c in categories if c.name == name), None)
    if cat:
        categories.remove(cat)
        cprint(f"Deleted '{name}'.", GREEN)
    else:
        cprint(f"'{name}' not found.", RED)


def manage_categories(categories):
    actions = [
        add_category,
        lambda _: cprint("\n".join(list_categories(categories)), YELLOW),
        edit_category, delete_category
    ]
    options = ["Add", "List", "Edit", "Delete", "Back"]
    while True:
        print_menu(options)
        choice = get_choice(options)
        if choice == len(options): break
        actions[choice -
                1](categories) if choice != 2 else actions[choice -
                                                           1](categories)
        input_colored("Enter to continue...", YELLOW)


def quit_app(*args):
    _ = args
    cprint("Goodbye!", RED)
    sys.exit()


def generate_random_date(start_date, end_date):
    """Generate a random date between two dates."""
    delta = end_date - start_date
    random_days = random.randrange(delta.days)
    return start_date + timedelta(days=random_days)


def run_demo(categories):
    needs = budget.Category('Needs')
    wants = budget.Category('Wants')
    savings = budget.Category('Savings')
    categories.extend([needs, wants, savings])

    base_monthly_income = 5000
    monthly_income_variation = random.uniform(-0.1, 0.1)
    monthly_income = base_monthly_income * (1 + monthly_income_variation)

    needs_allocation = random.uniform(0.45, 0.55)
    wants_allocation = random.uniform(0.20, 0.30)
    savings_allocation = 1 - (needs_allocation + wants_allocation)

    for category, allocation, purpose in zip(
        [needs, wants, savings],
        [needs_allocation, wants_allocation, savings_allocation],
        ['Needs', 'Wants', 'Savings'],
            strict=True):
        deposit_amount = monthly_income * allocation
        category.deposit(deposit_amount, f'Monthly salary - {purpose}')
        print(f"Deposited ${deposit_amount:.2f} to {purpose} category.")

    descriptions = {
        'needs':
        ['Rent', 'Groceries', 'Utilities', 'Insurance', 'Gas', 'Phone Bill'],
        'wants': [
            'Dining Out', 'Entertainment', 'Hobbies', 'Shopping',
            'Subscriptions'
        ],
        'savings': ['Emergency Fund', 'Investment', 'Retirement']
    }

    start_date = datetime.now() - timedelta(days=365)
    end_date = datetime.now()

    terminal_width = os.get_terminal_size().columns

    header = f"{BLUE}{'Type':<10}{'Category':<12}{'Amount':>10}{'Date':>15}{'Description':<30}{RESET}"
    cprint(header, YELLOW)
    cprint('-' * terminal_width, YELLOW)

    for _ in range(100):
        trans_type = random.choices(['needs', 'wants', 'savings'],
                                    weights=[50, 30, 20],
                                    k=1)[0]

        amount = random.uniform(5, 500)
        trans_date = generate_random_date(start_date,
                                          end_date).strftime("%Y-%m-%d")
        description = random.choice(descriptions[trans_type])
        line = f"{description} - {trans_date}"

        if trans_type == 'needs':
            needs.withdraw(amount, line)
        elif trans_type == 'wants':
            wants.withdraw(amount, line)
        else:
            savings.deposit(amount, line)

        action = "Deposited" if trans_type == 'savings' else "Withdrew"
        category_cap = trans_type.capitalize()

        print_line = (f"{GREEN if action == 'Deposited' else RED}{action:<10}"
                      f"{category_cap:<12}"
                      f"${amount:>10.2f}"
                      f"{trans_date:>15}"
                      f"{description:<30}{RESET}")
        print(print_line[:terminal_width])

    return categories


def main():
    has_run_demo = False
    budget_categories = []
    menu_options = [
        "Run Demo", "Manage categories", "Add income", "Add expense",
        "View category ledger", "View percentage spent by category", "Quit"
    ]
    actions = {
        1: run_demo,
        2: manage_categories,
        3: lambda: add_trans(budget_categories, 'income'),
        4: lambda: add_trans(budget_categories, 'expense'),
        5: view_ledger,
        6: create_spend_chart,
        7: quit_app
    }

    while True:
        overview(budget_categories)
        print_menu(menu_options)
        choice = get_choice(menu_options)
        action = actions.get(choice)
        if action:
            if choice == 1 and not has_run_demo:
                budget_categories = action(budget_categories)
                has_run_demo = True
            elif choice == 6:
                print(create_spend_chart(budget_categories))
            else:
                action(budget_categories)
        else:
            print(f"{RED}Invalid choice.{RESET}")
        input(f"{YELLOW}Press Enter to continue...{RESET}")


if __name__ == "__main__":
    main()
