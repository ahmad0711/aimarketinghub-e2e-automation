from playwright.sync_api import Page, expect


class DashboardPage:
    def __init__(self, page: Page):
        self.page = page
        self.dashboard_heading = page.get_by_text("Dashboard", exact=True)
        self.new_campaign_menu = page.get_by_role("button", name="New Campaign")
        self.new_campaign_heading = page.get_by_text("What do you want from this campaign?")

    def verify_loaded(self):
        expect(self.dashboard_heading).to_be_visible(timeout=20000)
        self.page.wait_for_load_state("networkidle")

    def go_to_new_campaign(self):
        expect(self.new_campaign_menu).to_be_visible(timeout=15000)
        expect(self.new_campaign_menu).to_be_enabled(timeout=15000)

        # Click New Campaign and retry once if sidebar event was still hydrating
        self.new_campaign_menu.click()
        if not self.new_campaign_heading.is_visible():
            self.page.wait_for_timeout(1500)
            if self.new_campaign_menu.is_visible():
                self.new_campaign_menu.click()

        expect(self.new_campaign_heading).to_be_visible(timeout=20000)