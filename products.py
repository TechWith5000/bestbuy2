from abc import ABC, abstractmethod


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
        self.active = True # A Product is active by default
        self.promotion = None # Initialize without promotion,
                              # None will be replaced by a promotion instance
                              # representing the promotion applied to the product

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

    def set_promotion(self, promotion):
        '''Set a promotion for the product.
        :parameter promotion: The promotion to apply to the product.'''
        self.promotion = promotion

    def remove_promotion(self):
        '''Remove the promotion from the product.\n
        Only one kind of promotion can be applied to a single product at one time.'''
        self.promotion = None

    def show(self):
        '''Returns a string that represents the product'''
        promo_info = ""
        if self.promotion:
            promo_info = f", Promotion: {self.promotion.name}"
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, {promo_info}"

    def buy(self, quantity):
        '''Buys a given quantity of the product.
        Returns the total price (float) of the purchase.
        Updates the quantity of the product.
        In case of a problem (when? think about it), raises an Exception.'''
        if (self.quantity - quantity) < 0:
            raise ValueError ("Not enough in stock.")
        # Calculate total price considering promotions
        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = quantity * self.price
        # Adjust quantity with setter method ( equivalent to self.quantity -= quantity)
        quantity_in_stock = self.get_quantity()
        self.set_quantity(quantity_in_stock - quantity)
        return float(total_price)


class NonStockedProduct(Product):
    '''This class represents products in the store that are not physical, so we don’t need
     to keep track of their quantity. for example - a Microsoft Windows license. On these
     products, the quantity should be set to zero and always stay that way.'''
    def __init__(self, name, price):
        # instead of accepting a quantity paramenter, the class sets quantity to 0 directly
        super().__init__(name, price, quantity=0)

    def buy(self, quantity):
        '''Buys a given quantity of the product.
        Returns the total price (float) of the purchase.
        No need to update the quantity in stock for NonStockedProduct .'''
        # calculate the price
        total_price = self.price * quantity
        return float(total_price)
    def show(self):
        '''Returns a string that represents the product'''
        return f"{self.name}, Price: {self.price}, Quantity: Unlimited availability"

class LimitedProduct(Product):
    '''Some products can only be purchased X times in an order. For example - a shipping fee
     can only be added once. If an order is attempted with quantity larger than the maximum
    one, it should be refused with an exception.'''
    def __init__(self, name, price, quantity, maximum):

        super().__init__(name, price, quantity)
        self.maximum = maximum

    def show(self):
        '''Returns a string that represents the product'''
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, available once per order"

    def buy(self, quantity):
        '''Buys quantity of exact 1 item of the product, even if a greater quantity is being ordered.
        Returns the total price (float) of the purchase.
        Updates the quantity of the product.
        In case of a problem, raises an Exception.'''
        if quantity > self.maximum:
            raise ValueError ("Can only be purchased once per order")
        if (self.quantity - quantity) < 0:
            raise ValueError ("Not enough in stock.")
        # Adjust quantity with setter method ( equivalent to self.quantity -= quantity)
        quantity_in_stock = self.get_quantity()
        self.set_quantity(quantity_in_stock - quantity)
        # calculate the price
        total_price = self.price * quantity
        return float(total_price)

class Promotion(ABC):
    '''Abstract class for different kinds of promotions (supplied as child classes)'''
    def __init__(self, name):
        '''Initialization of a promotion
        :parameter name: Name of the promotion'''
        self.name = name

    @abstractmethod
    def apply_promotion(product, quantity) -> float:
        '''Apply the promotion to a certain quantity of the product
        :parameter product: The product to which the promotion applies.
        :parameter quantity: The purchased quantity of the product.
        :return: The total price after applying the promotion.'''
        pass

class PercentageDiscount(Promotion):
    '''Represents a percentage discount promotion.'''

    def __init__(self, name: str, percent: float):
        """
        Initialize a percentage discount promotion.
        :parameter name: The name of the promotion.
        :parameter percent: The discount percentage.
        """
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity) -> float:
        '''
        Apply the percentage discount to the product.
        :parameter product: The product to which the promotion applies.
        :parameter quantity: The purchased quantity of the product.
        :return: The total price after applying the discount.
        '''
        total_price = product.price * quantity
        discount_amount = total_price * (self.percent / 100)
        return total_price - discount_amount


class SecondItemHalfPrice(Promotion):
    '''Represents a promotion where the second item is half price.'''

    def __init__(self):
        '''Initialize the second item half price promotion.'''
        super().__init__("Second Item at Half Price")

    def apply_promotion(self, product, quantity) -> float:
        '''
        Apply the second item half price promotion to the product.
        :parameter product: The product to which the promotion applies.
        :parameter quantity: The quantity of the product being purchased.
        :return: The total price after applying the promotion.
        '''
        if quantity < 1:
            return product.price * quantity

        pairs = quantity // 2 # Calculate how often the second item discount applies
        total_price = pairs * (product.price + (product.price / 2))
        remainder = quantity % 2
        total_price += remainder * product.price

        return total_price


class BuyTwoGetOneFree(Promotion):
    '''Represents a promotion where every third item is free.'''

    def __init__(self):
        '''Initialize the buy two, get one free promotion.'''
        super().__init__("Buy 2, Get 1 Free")

    def apply_promotion(self, product, quantity) -> float:
        '''
        Apply the buy two, get one free promotion to the product.
        :parameter product: The product to which the promotion applies.
        :parameter quantity: The quantity of the product being purchased.
        :return: The total price after applying the promotion.
        '''
        if quantity < 1:
            return product.price * quantity

        free_items = quantity // 3
        payable_items = quantity - free_items

        return product.price * payable_items