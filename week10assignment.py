class BookstoreError(Exception):
    pass


class BookNotFoundError(BookstoreError):
    def __init__(self, book_title):
        self.book_title = book_title
        super().__init__(f"book not found: {book_title}")


class InsufficientCopiesError(BookstoreError):
    def __init__(self, book_title, requested, available):
        self.book_title = book_title
        self.requested = requested
        self.available = available
        self.shortage = requested - available
        super().__init__(f"cannot sell {requested} of {book_title}: "
            f"only {available} in stock, short by {self.shortage}")


class InvalidQuantityError(BookstoreError):
    def __init__(self, quantity):
        self.quantity = quantity
        super().__init__(f"invalid quantity: {quantity}. must be positive")


class Bookstore:
    def __init__(self):
        self.books = {}

    def add_book(self, title, price, quantity):
        if quantity <= 0:
            raise InvalidQuantityError(quantity)
        if title in self.books:
            self.books[title]["quantity"] += quantity
            self.books[title]["price"] = price
        else:
            self.books[title] = {"price": price, "quantity": quantity}

    def sell(self, title, quantity):
        if quantity <= 0:
            raise InvalidQuantityError(quantity)
        try:
            book = self.books[title]
        except KeyError:
            raise BookNotFoundError(title) from None
        if quantity > book["quantity"]:
            raise InsufficientCopiesError(title, quantity, book["quantity"])
        book["quantity"] -= quantity
        return round(quantity * book["price"], 2)

    def total_value(self):
        total = sum(info["price"] * info["quantity"] for info in self.books.values())
        return round(total, 2)


store = Bookstore()

store.add_book("Python Basics", 35.50, 20)
store.add_book("Data Science", 49.99, 15)
store.add_book("Algorithms", 62.00, 8)

print(f"total value: {store.total_value()}")

sale = store.sell("Python Basics", 5)
print(f"sold 5 copies for: {sale}")
print(f"total value: {store.total_value()}")

store.add_book("Data Science", 52.99, 10)
print(f"total value: {store.total_value()}")

tests = [
    lambda: store.sell("Machine Learning", 1),
    lambda: store.sell("Algorithms", 20),
    lambda: store.add_book("Web Dev", 29.99, -3),
]

for test in tests:
    try:
        test()
    except BookstoreError as e:
        print(e)
