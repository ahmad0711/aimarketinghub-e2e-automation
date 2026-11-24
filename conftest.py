import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from users import USERS


@pytest.fixture
def open_new_campaign(page: Page):
    """Logs in as the specified user role and navigates to the New Campaign wizard."""
    def _open(role: str = "pro"):
        user = USERS[role]
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)

        login_page.open()
        login_page.login(user["email"], user["password"])
        dashboard_page.verify_loaded()
        dashboard_page.go_to_new_campaign()
        return page

    return _open