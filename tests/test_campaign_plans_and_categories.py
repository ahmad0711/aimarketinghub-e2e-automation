import re
import pytest
from playwright.sync_api import expect
from pages.new_campaign_page import NewCampaignPage


def test_builder_user_tiktok_not_available(open_new_campaign):
    page = open_new_campaign("builder")
    campaign_page = NewCampaignPage(page)

    campaign_page.fill_campaign_basics(
        name="Builder Plan Check - UAE",
        goal="Get more website visits",
        ai_prompt="Promote tech gadgets in UAE.",
        special_category="None",
    )
    campaign_page.select_audience(age="25-44", gender="All", language="English")

    expect(page.get_by_text("Meta (Facebook & Instagram)")).to_be_visible()
    expect(page.get_by_text("Google Ads")).to_be_visible()
    expect(page.get_by_text("TikTok Page for ads")).not_to_be_visible()


def test_starter_user_sees_upgrade_popup_on_launch(open_new_campaign):
    page = open_new_campaign("starter")
    campaign_page = NewCampaignPage(page)

    campaign_page.fill_campaign_basics(
        name="Starter Plan Check - UAE",
        goal="Get more website visits",
        ai_prompt="Promote tech gadgets in UAE.",
        special_category="None",
    )
    campaign_page.select_audience(age="25-44", gender="All", language="English")
    campaign_page.select_platforms(fb_page_name="T For Tech")
    campaign_page.set_budget_and_schedule(budget="AED 2,000")
    campaign_page.choose_use_ai()
    campaign_page.fill_ad_destination(
        landing_url="https://aimarketinghub.ae",
        cta="Shop Now",
        description="Limited time tech offer in UAE",
        brand_name="T For Tech",
        tiktok_type="Image Ad",
    )
    campaign_page.wait_for_ai_ads_and_review()

    page.get_by_role("button", name=re.compile("Launch", re.IGNORECASE)).click()
    expect(page.get_by_text(re.compile("Upgrade", re.IGNORECASE)).first).to_be_visible(timeout=10000)


@pytest.mark.parametrize(
    "category",
    [
        "Financial products and services",
        "Employment",
        "Housing / real estate",
    ],
)
def test_special_ad_categories_show_modal(open_new_campaign, category: str):
    page = open_new_campaign("pro")
    campaign_page = NewCampaignPage(page)

    page.get_by_text(category, exact=True).click()
    expect(campaign_page.discriminatory_modal_title).to_be_visible()

    campaign_page.understand_continue_btn.click()
    expect(campaign_page.discriminatory_modal_title).not_to_be_visible()


def test_none_category_does_not_show_modal(open_new_campaign):
    page = open_new_campaign("pro")
    campaign_page = NewCampaignPage(page)

    page.get_by_text("None", exact=True).click()
    expect(campaign_page.discriminatory_modal_title).not_to_be_visible()