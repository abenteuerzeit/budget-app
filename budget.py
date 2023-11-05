"""
    budget.py is used to manage a budget using categories.
"""


class Category:
    """
    A class to represent a budget category.
    Attributes:
        name (str): The name of the category.
        ledger (list): A list of transactions.
    """

    def __init__(self, category_name):
        """
        Constructs all the necessary attributes for the category object.

        Parameters:
            category_name (str): The name of the category.
        """
        self.__overdraft_limit = 0
        self.__balance = 0
        self.name = category_name
        self.ledger = []

    def __str__(self):
        """
        Return a string representation of the category's transactions and balance.

        Output example:
        *************Food*************
        initial deposit        1000.00
        groceries               -10.15
        restaurant and more foo -15.89
        Transfer to Clothing    -50.00
        Total: 923.96
        """
        total_length = 30
        title = self.name.center(total_length, '*')
        items = "\n".join(
            f"{item['description'][:23]:23}{item['amount']:>7.2f}"
            for item in self.ledger)
        total_str = f"Total: {self.get_balance():.2f}"
        output_str = f"{title}\n{items}\n{total_str}"
        return output_str

    def deposit(self, amount, description=""):
        """
        Append a deposit to the ledger list.

        Parameters:
            amount (float): The amount of deposit.
            description (str): The description of the deposit.
        """
        self.__balance += amount
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        """
        Append a withdrawal to the ledger if there are sufficient funds.

        Parameters:
            amount (float): The amount to withdraw.
            description (str): The description of the withdrawal.

        Returns:
            bool: True if the withdrawal was added, False otherwise.
        """
        if self.check_funds(amount):
            self.__balance -= amount
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        """
        Compute and return the current balance of the budget category.

        Returns:
            float: The balance of the budget category.
        """
        return self.__balance

    def transfer(self, amount, category):
        """
        Transfer the given amount from this category to another category.

        Parameters:
            amount (float): The amount to transfer.
            category (Category): The category to transfer to.

        Returns:
            bool: True if the transfer was completed, False otherwise.
        """
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        """
        Check if there are enough funds for an operation.

        Parameters:
            amount (float): The amount to check.

        Returns:
            bool: True if there are sufficient funds, False otherwise.
        """
        return self.__balance >= amount


def create_spend_chart(categories):
    """
    Create a bar chart representing the percentage of expenses for each category.

    Parameters:
        categories (list): The list of category objects.

    Returns:
        str: A string that represents the bar chart.

    Output example:
    | LEGEND |==============================\
    | y-axis | Labels for 0% - 100%         |
    | x-axis | Categories                   |
    | 'o'    | Bar unit representing 10%    |
    |========|==============================/
    Percentage spent by category
    100|          
     90|          
     80|          
     70|          
     60| o        
     50| o        
     40| o        
     30| o        
     20| o  o     
     10| o  o  o  
      0| o  o  o  
        ----------
         F  C  A  
         o  l  u  
         o  o  t  
         d  t  o  
            h     
            i     
            n     
            g     
    """
    chart = "Percentage spent by category\n"

    spends = [
        sum(-item['amount'] for item in category.ledger if item['amount'] < 0)
        for category in categories
    ]
    total_spends = sum(spends)

    if total_spends == 0:
        return chart + "No expenses"

    percentages = [(spend / total_spends) * 100 for spend in spends]

    for percentage in range(100, -1, -10):
        chart += f"{percentage:>3}| " + "".join(
            "o  " if percent >= percentage else "   "
            for percent in percentages) + "\n"

    chart += "    -" + "---" * len(categories) + "\n"

    max_length = max(len(category.name) for category in categories)

    for i in range(max_length):
        chart += "     " + "".join(
            category.name[i] + "  " if i < len(category.name) else "   "
            for category in categories) + "\n"

    return chart.strip("\n")


if __name__ == "__main__":
    budget_categories = []
    while True:
        print("1. Create category")
        print("2. View categories")
        print("3. Add income")
        print("4. Add expense")
        print("5. View category ledger")
        print("6. View percentage spent by category")
        print("7. Quit")
        choice = input("Enter your choice: ")
        if choice == "1":
            name = input("Enter category name: ")
            category = Category(name)
            budget_categories.append(category)
            print(f"Category '{category.name}' created.")
        elif choice == "2":
            if not budget_categories:
                print("No categories created.")
            else:
                print("Categories:")
                for category in budget_categories:
                    print(f"- {category.name}")
        elif choice in ["3", "4"]:
            cat_name = input("Enter category name: ")
            found_category = None
            for category in budget_categories:
                if category.name == cat_name:
                    found_category = category
                    break
            if not found_category:
                print(f"Category '{cat_name}' does not exist.")
                continue
            amount = float(input("Enter amount: "))
            if choice == "3":
                found_category.deposit(amount)
                print(f"Income added to category '{cat_name}'.")
            else:
                found_category.withdraw(amount)
                print(f"Expense added to category '{cat_name}'.")
        elif choice == "5":
            cat_name = input("Enter category name: ")
            for category in budget_categories:
                if category.name == cat_name:
                    print(category)
                    break
            else:
                print(f"Category '{cat_name}' does not exist.")
        elif choice == "6":
            print(create_spend_chart(budget_categories))
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
