from pages.new_campaign_page import NewCampaignPage


def test_create_more_sales_campaign(open_new_campaign):
    page = open_new_campaign("pro")
    campaign_page = NewCampaignPage(page)

    campaign_page.create_complete_pro_campaign(
        name="Auto E2E - More Sales",
        goal="Get more sales",
        outcome="Website purchases",
        ai_prompt="Promote top-selling products in UAE with special discounts.",
        cta="Shop Now",
    )