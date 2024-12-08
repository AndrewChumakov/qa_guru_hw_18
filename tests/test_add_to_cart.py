import os

import allure
from selene import have, by

from tests.helpers import post_request

URL = "https://demowebshop.tricentis.com"


def test_add_to_cart_with_authorization(setup_browser):
    with allure.step("Авторизация"):
        data = {
            "Email": os.getenv("LOGIN"),
            "Password": os.getenv("PASSWORD"),
            "RememberMe": False
        }
        response = post_request(URL + "/login", data=data, allow_redirects=False)
        authorization_cookie = response.cookies.get("NOPCOMMERCE.AUTH")

    with allure.step("Добавить товар в корзину"):
        post_request(URL + "/addproducttocart/details/53/1", cookies={"NOPCOMMERCE.AUTH": authorization_cookie})

    with allure.step("Открыть корзину"):
        setup_browser.open(URL + "/cart")
        setup_browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie})
        setup_browser.driver.refresh()

    with allure.step("Проверить, что товар добавлен"):
        setup_browser.element("//a[@class='product-name']").should(have.text("3rd Album"))

    with allure.step("Очистить корзину"):
        setup_browser.element(".remove-from-cart").click()
        setup_browser.element(by.xpath("//input[@name='updatecart']")).click()
        setup_browser.element(".page-body").should(have.text("Your Shopping Cart is empty!"))


def test_add_to_cart_without_authorization(setup_browser):
    with allure.step("Добавить товар в корзину"):
        response = post_request(URL + "/addproducttocart/details/53/1")
        authorization_cookie = response.cookies.get("Nop.customer")

    with allure.step("Открыть корзину"):
        setup_browser.open(URL + "/cart")
        setup_browser.driver.add_cookie({"name": "Nop.customer", "value": authorization_cookie})
        setup_browser.driver.refresh()

    with allure.step("Проверить, что товар добавлен"):
        setup_browser.element("//a[@class='product-name']").should(have.text("3rd Album"))

    with allure.step("Очистить корзину"):
        setup_browser.element(".remove-from-cart").click()
        setup_browser.element(by.xpath("//input[@name='updatecart']")).click()
        setup_browser.element(".page-body").should(have.text("Your Shopping Cart is empty!"))
