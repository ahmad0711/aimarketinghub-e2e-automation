from pages.new_campaign_page import NewCampaignPage


def test_create_grow_audience_campaign(open_new_campaign):
    page = open_new_campaign("pro")
    campaign_page = NewCampaignPage(page)

    campaign_page.create_complete_pro_campaign(
        name="Auto E2E - Grow My Audience",
        goal="Grow my audience",
        ai_prompt="Grow brand awareness and followers in UAE.",
        cta="Learn More",
    )