from playwright.sync_api import Page, expect
from pages.login_page import LoginPage

def test_valid_login(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("ahmadsqa.te@gmail.com", "12345678")

    # Login ke baad check karein ke login page se aage nikal gaya hai
    expect(login_page.password_input).not_to_be_visible(timeout=10000)