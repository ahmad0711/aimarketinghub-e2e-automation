from pages.new_campaign_page import NewCampaignPage


def test_create_messages_or_calls_campaign(open_new_campaign):
    page = open_new_campaign("pro")
    campaign_page = NewCampaignPage(page)

    campaign_page.create_complete_pro_campaign(
        name="Auto E2E - Calls Campaign",
        goal="Get more messages or calls",
        outcome="Calls",
        ai_prompt="Generate direct customer phone calls and inquiries in UAE.",
        cta="Contact Us",
    )