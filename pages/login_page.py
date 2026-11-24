from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        # Step 1: Email screen locators
        self.email_input = page.get_by_placeholder("you@company.com")
        self.continue_btn = page.get_by_role("button", name="Continue")
        # Step 2: Password screen locator
        self.password_input = page.get_by_placeholder("Password")

    def open(self):
        self.page.goto("https://aimarketinghub.ae")

    def login(self, email: str, password: str):
        # Email enter karke Continue click karein
        self.email_input.fill(email)
        self.continue_btn.click()

        # Password field aane ka wait karke fill karein aur Continue click karein
        self.password_input.wait_for(state="visible")
        self.password_input.fill(password)
        self.continue_btn.click()