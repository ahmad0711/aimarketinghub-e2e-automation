from pages.new_campaign_page import NewCampaignPage


def test_create_website_visits_campaign(open_new_campaign):
    page = open_new_campaign("pro")
    campaign_page = NewCampaignPage(page)

    campaign_page.create_complete_pro_campaign(
        name="Auto E2E - Website Visits",
        goal="Get more website visits",
        ai_prompt="Drive high-intent traffic to our UAE website.",
        cta="Learn More",
    )