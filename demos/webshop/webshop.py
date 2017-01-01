""" This is the actual production code for our webshop """


class Product:
    def __init__(self, price):
        self.price = price


class Cart:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def calculate_total_price(self):
        total = sum(p.price for p in self.products)
        if total >= 20:
            total += 2
        else:
            total += 5
        return total
