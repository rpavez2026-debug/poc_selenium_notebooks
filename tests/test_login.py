import pytest

from utils.config import PASSWORD, USERS


@pytest.mark.smoke
def test_login_exitoso_lleva_a_productos(login_page):
    inventory = login_page.login_as(USERS["standard"])
    assert inventory.title() == "Products"
    assert "inventory.html" in inventory.current_url


@pytest.mark.regression
@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        (USERS["locked_out"], PASSWORD, "Sorry, this user has been locked out."),
        (USERS["standard"], "clave_incorrecta", "Username and password do not match any user in this service"),
        ("", PASSWORD, "Username is required"),
        (USERS["standard"], "", "Password is required"),
    ],
    ids=["usuario_bloqueado", "password_incorrecta", "sin_usuario", "sin_password"],
)
def test_login_fallido_muestra_error(login_page, username, password, expected_error):
    login_page.login(username, password)
    assert expected_error in login_page.error_message()
    assert "inventory.html" not in login_page.current_url


@pytest.mark.smoke
def test_logout_vuelve_al_login(inventory):
    login_page = inventory.logout()
    assert login_page.is_displayed()


@pytest.mark.regression
def test_inventario_protegido_sin_sesion(login_page):
    login_page.open("inventory.html")
    assert "You can only access '/inventory.html' when you are logged in." in login_page.error_message()
