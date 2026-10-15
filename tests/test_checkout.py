import pytest

PRODUCTS = ["Sauce Labs Backpack", "Sauce Labs Fleece Jacket"]


@pytest.mark.smoke
def test_compra_completa_e2e(inventory):
    cart = inventory.add_to_cart(*PRODUCTS).go_to_cart()
    assert sorted(cart.item_names()) == sorted(PRODUCTS)

    overview = cart.checkout().continue_to_overview("Ricardo", "Pavez", "8320000")
    assert sorted(overview.item_names()) == sorted(PRODUCTS)

    # El subtotal debe ser la suma de los precios y el total = subtotal + impuesto
    assert overview.subtotal() == pytest.approx(sum(overview.item_prices()))
    assert overview.total() == pytest.approx(overview.subtotal() + overview.tax())

    complete = overview.finish()
    assert complete.header() == "Thank you for your order!"


@pytest.mark.regression
@pytest.mark.parametrize(
    "first, last, postal, expected_error",
    [
        ("", "Pavez", "8320000", "First Name is required"),
        ("Ricardo", "", "8320000", "Last Name is required"),
        ("Ricardo", "Pavez", "", "Postal Code is required"),
    ],
    ids=["sin_nombre", "sin_apellido", "sin_codigo_postal"],
)
def test_checkout_valida_campos_obligatorios(inventory, first, last, postal, expected_error):
    info = inventory.add_to_cart(PRODUCTS[0]).go_to_cart().checkout()
    info.fill(first, last, postal)
    assert expected_error in info.error_message()
