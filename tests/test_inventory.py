import pytest

from pages import InventoryPage
from utils.config import USERS

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@pytest.mark.smoke
def test_catalogo_muestra_seis_productos(inventory):
    assert len(inventory.product_names()) == 6


@pytest.mark.regression
@pytest.mark.parametrize(
    "sort_value, key, reverse",
    [
        (InventoryPage.SORT_NAME_ASC, "names", False),
        (InventoryPage.SORT_NAME_DESC, "names", True),
        (InventoryPage.SORT_PRICE_ASC, "prices", False),
        (InventoryPage.SORT_PRICE_DESC, "prices", True),
    ],
    ids=["nombre_a_z", "nombre_z_a", "precio_menor_mayor", "precio_mayor_menor"],
)
def test_ordenar_productos(inventory, sort_value, key, reverse):
    inventory.sort_by(sort_value)
    values = inventory.product_names() if key == "names" else inventory.product_prices()
    assert values == sorted(values, reverse=reverse)


@pytest.mark.smoke
def test_agregar_y_quitar_productos_actualiza_carrito(inventory):
    assert inventory.cart_count() == 0

    inventory.add_to_cart(BACKPACK, BIKE_LIGHT)
    assert inventory.cart_count() == 2
    assert inventory.button_text(BACKPACK) == "Remove"

    inventory.remove_from_cart(BACKPACK)
    assert inventory.cart_count() == 1
    assert inventory.button_text(BACKPACK) == "Add to cart"


@pytest.mark.regression
def test_carrito_contiene_productos_agregados(inventory):
    cart = inventory.add_to_cart(BACKPACK, BIKE_LIGHT).go_to_cart()
    assert sorted(cart.item_names()) == sorted([BACKPACK, BIKE_LIGHT])


@pytest.mark.known_bug
@pytest.mark.xfail(reason="problem_user tiene el orden de productos roto a propósito", strict=False)
def test_problem_user_ordenar_por_precio(login_page):
    inventory = login_page.login_as(USERS["problem"])
    inventory.sort_by(InventoryPage.SORT_PRICE_ASC)
    prices = inventory.product_prices()
    assert prices == sorted(prices)
