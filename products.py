class Product:

    def __init__(self, name, price, quantity):
        '''Initiator (constructor) method.
        Creates the instance variables (active is set to True).
        If something is invalid (empty name / negative price or quantity), raises an exception.'''
        self.name = name
        if name == "":
            raise ValueError ("Empty name.")
        self.price = price
        if price < 0:
            raise ValueError ("Price cannot be negative.")
        self.quantity = quantity
        if quantity < 0:
            raise ValueError ("Quantity cannot be negative.")
        self.active = True

    def get_quantity(self):
        '''Getter function for quantity.
        Returns the quantity (float).'''
        return float(self.quantity)

    def set_quantity(self, quantity):
        '''
        Setter function for quantity. If quantity reaches 0, deactivates the product.
        '''
        self.quantity = quantity
        if self.quantity <= 0:
            self.deactivate()

    def is_active(self):
        '''Getter function for active.
        Returns True if the product is active, otherwise False.'''
        if self.active:
            return True
        else:
            return False

    def activate(self):
        '''Activates the product.'''
        self.active = True

    def deactivate(self):
        '''Deactivates the product.'''
        self.active = False

    def show(self):
        '''Returns a string that represents the product'''
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def buy(self, quantity):
        '''Buys a given quantity of the product.
        Returns the total price (float) of the purchase.
        Updates the quantity of the product.
        In case of a problem (when? think about it), raises an Exception.'''
        if (self.quantity - quantity) < 0:
            raise ValueError ("Not enough in stock.")
        # Adjust quantity with setter method ( equivalent to self.quantity -= quantity)
        quantity_in_stock = self.get_quantity()
        self.set_quantity(quantity_in_stock - quantity)
        # calculate the price
        total_price = self.price * quantity
        return float(total_price)