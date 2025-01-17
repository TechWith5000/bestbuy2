from products import Product, LimitedProduct, NonStockedProduct

class Store:
    ''' Holds a class variable as a list of all products that exist in a store'''

    def __init__(self, list):
        self.product_list = list

    def add_product(self, product):
        '''Adds a product to the store'''
        self.product_list.append(product)

    def remove_product(self, product):
        '''Removes a product from store'''
        if product in self.product_list:
            self.product_list.remove(product)

    def get_total_quantity(self):
        '''Returns how many items are in the store in total'''
        total_quantity = 0
        for product in self.product_list:
            product_quantity = Product.get_quantity(product)
            total_quantity += product_quantity
        return int(round(total_quantity))

    def get_all_products(self):
        '''Returns all products in the store that are active'''
        active_products = []
        for product in self.product_list:
            if product.is_active():
                active_products.append(product)
        return active_products


    def order(self, shopping_list):
        '''Gets a list of tuples, where each tuple has 2 items:
        Product (Product class) and quantity (int).
        Buys the products and returns the total price of the order.'''
        order_price = 0.0
        for tuple in shopping_list:
            product, quantity = tuple
            price = product.buy(quantity)
            order_price += price
        return order_price
