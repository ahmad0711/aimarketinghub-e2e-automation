import re
from datetime import datetime
from playwright.sync_api import Page, expect
from pages.campaigns_page import CampaignsPage


class NewCampaignPage:
    def __init__(self, page: Page):
        self.page = page

        # Step 1: Goal & Campaign Details
        self.campaign_name_input = page.get_by_placeholder("e.g. Ramadan Hydrating Serum")
        self.ai_prompt_input = page.get_by_placeholder("Example: I want to sell more hydrating skincare")
        self.next_audience_btn = page.get_by_role("button", name="Next: Choose Audience")

        # Modal: Discriminatory Practices (Special Ad Category)
        self.discriminatory_modal_title = page.get_by_text("Discriminatory Practices")
        self.understand_continue_btn = page.get_by_role("button", name="I understand — continue")

        # Step 2: Audience
        self.next_platforms_btn = page.get_by_role("button", name="Next: Where to show ads")

        # Step 3: Platforms
        self.fb_page_dropdown = page.get_by_text("Select a Facebook Page")
        self.next_budget_btn = page.get_by_role("button", name="Next: Budget & duration")

        # Step 4: Budget & Duration
        self.budget_heading = page.get_by_text("How much do you want to spend?")
        self.next_create_ad_btn = page.get_by_role("button", name="Next: Create your ad")

        # Modal: Service Charge Confirmation
        self.accept_service_charge_btn = page.get_by_role("button", name="I Accept")

        # Step 5: Create Ads Method
        self.use_ai_btn = page.get_by_role("button", name="Use AI")

        # Step 6: Ad Destination
        self.cta_dropdown = page.get_by_text("Select a CTA")
        self.landing_url_input = page.get_by_placeholder("https://example.com")
        self.description_input = page.get_by_placeholder("Limited time Ramadan offer")
        self.brand_name_input = page.get_by_placeholder("GlowCare")
        self.next_generate_ads_btn = page.get_by_role("button", name="Next: Generate Ads")

        # Step 7: AI Ad Generation & Review
        self.next_review_btn = page.get_by_role("button", name="Next: Review Campaign")

        # Step 8: Final Review, Confirmation Modal & Launch
        self.launch_campaign_btn = page.get_by_role("button", name=re.compile("Launch", re.IGNORECASE))
        self.confirm_modal_title = page.get_by_text("You are about to create campaigns")
        self.confirm_create_campaigns_btn = page.get_by_role("button", name="Create Campaigns")

    def select_special_ad_category(self, category: str):
        self.page.get_by_text(category, exact=True).click()
        if category != "None":
            self.understand_continue_btn.wait_for(state="visible", timeout=5000)
            self.understand_continue_btn.click()

    def fill_campaign_basics(
        self,
        name: str,
        goal: str,
        ai_prompt: str,
        special_category: str = "None",
        outcome: str | None = None,
    ):
        self.campaign_name_input.fill(name)
        self.page.get_by_text(goal, exact=True).click()

        if outcome:
            outcome_option = self.page.get_by_text(outcome, exact=True)
            expect(outcome_option).to_be_visible(timeout=5000)
            outcome_option.click()

        self.ai_prompt_input.fill(ai_prompt)
        self.select_special_ad_category(special_category)
        self.next_audience_btn.click()

    def select_audience(self, age: str = "25-44", gender: str = "All", language: str = "English"):
        if age == "All":
            self.page.get_by_text("All", exact=True).first.click()
        else:
            self.page.get_by_text(age, exact=True).click()

        if gender == "All":
            self.page.get_by_text("All", exact=True).last.click()
        else:
            self.page.get_by_text(gender, exact=True).click()

        self.page.get_by_text(language, exact=True).click()
        self.next_platforms_btn.click()

    def select_platforms(self, fb_page_name: str = "T For Tech"):
        self.fb_page_dropdown.click()
        self.page.get_by_text(fb_page_name, exact=True).click()
        self.next_budget_btn.click()

    def set_budget_and_schedule(self, budget: str = "AED 2,000"):
        expect(self.budget_heading).to_be_visible(timeout=15000)

        budget_radio = self.page.get_by_role("radio", name=budget)
        expect(budget_radio).to_be_enabled(timeout=10000)
        budget_radio.click()

        end_date_input = self.page.get_by_role("textbox", name="End date")
        end_date_input.click()
        self.page.keyboard.press("Enter")

        if not self.next_create_ad_btn.is_enabled():
            enabled_day = self.page.locator("button[name='day']:not([disabled]), [role='gridcell'] button:not([disabled])").last
            if enabled_day.is_visible():
                enabled_day.click()

        expect(self.next_create_ad_btn).to_be_enabled(timeout=10000)
        self.next_create_ad_btn.click()

        self.accept_service_charge_btn.wait_for(state="visible", timeout=5000)
        self.accept_service_charge_btn.click()

    def choose_use_ai(self):
        self.use_ai_btn.click()

    def fill_ad_destination(
        self,
        landing_url: str,
        cta: str = "Shop Now",
        description: str = "",
        brand_name: str = "",
        tiktok_type: str = "Image Ad",
    ):
        if self.cta_dropdown.is_visible():
            self.cta_dropdown.click()
            self.page.get_by_text(cta, exact=True).click()

        self.landing_url_input.fill(landing_url)
        if description:
            self.description_input.fill(description)
        if brand_name:
            self.brand_name_input.fill(brand_name)

        self.page.get_by_text(tiktok_type, exact=True).click()
        expect(self.next_generate_ads_btn).to_be_enabled(timeout=10000)
        self.next_generate_ads_btn.click()

    def wait_for_ai_ads_and_review(self):
        expect(self.next_review_btn).to_be_enabled(timeout=90000)
        self.next_review_btn.click()

    def launch_and_verify_success(self):
        expect(self.launch_campaign_btn).to_be_enabled(timeout=15000)
        self.launch_campaign_btn.click()

        # Confirm the "You are about to create campaigns" modal
        expect(self.confirm_modal_title).to_be_visible(timeout=10000)
        self.confirm_create_campaigns_btn.click()

        # Wait for campaign creation to finish across Meta, Google & TikTok (up to 90s)
        expect(self.confirm_modal_title).not_to_be_visible(timeout=90000)
        success_or_redirect = self.page.get_by_text(
            re.compile(r"success|launched|created|My Campaigns", re.IGNORECASE)
        ).first
        expect(success_or_redirect).to_be_visible(timeout=90000)
        self.page.wait_for_load_state("networkidle")

    def create_complete_pro_campaign(
        self,
        name: str,
        goal: str,
        ai_prompt: str,
        cta: str,
        outcome: str | None = None,
        landing_url: str = "https://aimarketinghub.ae",
        fb_page_name: str = "T For Tech",
        budget: str = "AED 2,000",
    ):
        unique_campaign_name = f"{name} ({datetime.now().strftime('%H%M%S')})"

        self.fill_campaign_basics(
            name=unique_campaign_name,
            goal=goal,
            ai_prompt=ai_prompt,
            special_category="None",
            outcome=outcome,
        )
        self.select_audience(age="25-44", gender="All", language="English")

        expect(self.page.get_by_text("Meta (Facebook & Instagram)")).to_be_visible()
        expect(self.page.get_by_text("Google Ads")).to_be_visible()
        expect(self.page.get_by_text("TikTok Ads")).to_be_visible()
        self.select_platforms(fb_page_name=fb_page_name)

        self.set_budget_and_schedule(budget=budget)
        self.choose_use_ai()
        self.fill_ad_destination(
            landing_url=landing_url,
            cta=cta,
            description="Limited time offer in UAE",
            brand_name=fb_page_name,
            tiktok_type="Image Ad",
        )
        self.wait_for_ai_ads_and_review()

        # Launch, confirm modal, wait for creation, and verify across all 3 platforms
        self.launch_and_verify_success()
        campaigns_page = CampaignsPage(self.page)
        campaigns_page.verify_campaign_across_platforms(
            campaign_name=unique_campaign_name,
            platforms=["Meta", "Google", "TikTok"],
        )