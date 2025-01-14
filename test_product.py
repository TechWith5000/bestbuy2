import pytest
from products import Product

def test_create_product():
    # create a Product instance
    lenovo = Product("Lenovo", 550, 200)

    # verify the attributes
    assert lenovo.name == "Lenovo"
    assert lenovo.price == 550
    assert lenovo.quantity == 200

def test_empty_name():
    # test for empty name
    with pytest.raises(ValueError, match="Empty name."):
        lenovo = Product("", 550, 20)

def test_negative_price():
    # test for negative price
    with pytest.raises(ValueError, match="Price cannot be negative."):
        lenovo = Product("Lenovo", -500, 20)

def test_inactivation():
    # create Product
    lenovo = Product("Lenovo", 500, 200)
    lenovo.set_quantity(0)
    assert lenovo.active == False

def test_purchase_modifies_quantity():
    # create product
    lenovo = Product("Lenovo", 500, 200)
    # buy certain amount of product
    lenovo.buy(100)
    assert lenovo.quantity == 100

def test_quantitiy_out_of_range():
    # create product
    lenovo = Product("Lenovo", 500, 200)
    with pytest.raises(ValueError, match="Not enough in stock."):
        lenovo.buy(222)



