import re
from playwright.sync_api import Page, expect


class CampaignsPage:
    def __init__(self, page: Page):
        self.page = page
        self.campaigns_menu = page.get_by_role("button", name="Campaigns")
        self.page_heading = page.get_by_text("My Campaigns", exact=True)

    def open_from_sidebar(self):
        if not self.page_heading.is_visible():
            self.campaigns_menu.click()
        expect(self.page_heading).to_be_visible(timeout=20000)
        self.page.wait_for_load_state("networkidle")

    def verify_campaign_on_platform(self, platform: str, campaign_name: str):
        platform_tab = self.page.get_by_text(platform, exact=True).first
        expect(platform_tab).to_be_visible(timeout=10000)
        platform_tab.click()
        self.page.wait_for_load_state("networkidle")

        campaign_entry = self.page.locator("table").get_by_text(re.compile(re.escape(campaign_name))).first
        expect(campaign_entry).to_be_visible(timeout=25000)

    def verify_campaign_across_platforms(self, campaign_name: str, platforms: list[str]):
        self.open_from_sidebar()
        for platform in platforms:
            self.verify_campaign_on_platform(platform=platform, campaign_name=campaign_name)