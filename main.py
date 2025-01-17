import products
import store
from products import Product, NonStockedProduct, LimitedProduct, PercentDiscount, SecondHalfPrice, ThirdOneFree
from store import Store

def start():
    '''Shows the menu to the user'''
    print("     Store menu\n"
          "     __________")
    print("1. List all products in store\n"
          "2. Show total amount in store\n"
          "3. Make an order\n"
          "4. Quit")

def show_products(products):
    print("------")
    for i, product in enumerate(products, start=1):
        print(f" {i}. {product.show()}")
    print("------\n")

def index_not_in_range(products, product_choice):
    if int(product_choice) > len(products) or int(product_choice) < 1:
        print(f"# {product_choice} is not a valid product")
        return True

def product_amount_is_available(product_choice, products, product_amount, shopping_list):
    # convert user input to an index
    selected_product_index = int(product_choice) - 1
    selected_product = products[selected_product_index]
    product_amount = int(product_amount)

    # check for unlimited availability
    if type(selected_product) == type(NonStockedProduct("Windows License", price=125)):
        shopping_list.append((selected_product, product_amount))
        print("Product added to list!")
        return True

    if type(selected_product) == type(LimitedProduct("Shipping", price=10, quantity=250, maximum=1)):
        if product_amount > selected_product.maximum:
            raise ValueError (f"Can be purchased only {selected_product.maximum} times per order.")
        shopping_list.append((selected_product, product_amount))
        print("Product added to list!")
        return True
# add tuple (product, amount) to shopping list, if amount available
    if product_amount <= selected_product.get_quantity():
        shopping_list.append((selected_product, product_amount))
        print("Product added to list!")
        return True
    else:
        print(f"Only {selected_product.get_quantity()} available")
        return False

def main():
    '''Runs the program, handles user input'''
    # setup initial stock of inventory
    product_list = [Product("MacBook Air M2", price=1450, quantity=100),
                    Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    Product("Google Pixel 7", price=500, quantity=250),
                    NonStockedProduct("Windows License", price=125),
                    LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
                    ]

    # Create promotion catalog
    second_half_price = SecondHalfPrice("Second Half price!")
    third_one_free = ThirdOneFree("Third One Free!")
    thirty_percent = PercentDiscount("30% off!", percent=30)

    # Add promotions to products
    product_list[0].set_promotion(second_half_price)
    product_list[1].set_promotion(third_one_free)
    product_list[3].set_promotion(thirty_percent)

    best_buy = Store(product_list)
    products_var = best_buy.get_all_products()


    while True:
        start()
        user_choice = input("Please enter a number: ")

        if user_choice == "1":
            show_products(products_var)

        if user_choice == "2":
            print(best_buy.get_total_quantity())

        if user_choice == "3":
            shopping_list = []
            order_running = True
            while order_running:
                show_products(products_var)
                print("When you want to finish order, enter empty text.")

                while True:
                    product_choice = input("Which product # do you want?")
                    # check whether user quits the order
                    if product_choice == "":
                        order_running = False
                        break # break the inner while loop
                    # check whether index is in the range of available products_var
                    if index_not_in_range(products_var, product_choice):
                        continue

                    product_amount = input("What amount do you want?")
                    # check whether user quits the order
                    if product_amount == "":
                        order_running = False
                        break # break the inner while loop


                    try:
                        if not product_amount_is_available(product_choice, products_var, product_amount, shopping_list):
                            continue

                    except ValueError as e: # ensure exceptions retain their specific message
                        print(f"Error adding product: {e}")
                        continue

                # check if the outer loop terminates and the inner loop therefore should terminate as well
                if not order_running:
                    break

            try:
                total_price = best_buy.order(shopping_list)
                print(f"***********\n Order made! Total payment: {total_price}")

            except ValueError:
                print("Not enough products_var in stock, please make your order again with a smaller amount.")
                continue

            # update the product list after each order
            products_var = best_buy.get_all_products()

        if user_choice == "4":
            break



if __name__ == "__main__":
    main()