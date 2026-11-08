import re

import pytest
from playwright.sync_api import Locator, Page, expect

SITE = "https://en.ehuniversity.lt"

def test_about_page_navigation(page: Page):
    page.goto("/")

    page.get_by_role("link", name="About", exact=True).first.click()

    expect(page).to_have_url(SITE + r"/about/")
    expect(page).to_have_title("About - European Humanities University")
    expect(page.locator("h1")).to_have_text("About")


def submit_by_enter(search: Locator):
    search.locator("input[name='s']").press("Enter")


def submit_by_click(search: Locator):
    search.locator("button[type='submit']").click()


@pytest.mark.parametrize(
    "submit",
    [submit_by_enter, submit_by_click],
    ids=["press Enter", "click Search"],
)
def test_search(page: Page, submit):
    page.goto("/")

    grid = page.locator("//div[contains(@class,'grid')]")
    search = grid.locator("//div[@class='header-search']")
    search.hover()
    search.locator("input[name='s']").fill("study programs")

    submit(search)

    expect(page).to_have_url(re.compile(r"\?s=study\+programs"))

    study_programs = page.locator("//div[contains(@class, 'search-results')]//a[contains(@href, 'study') and contains(@href, 'programs')]")
    study_program = find_in_search_results(page, study_programs)

    expect(study_program).to_be_visible()


def find_in_search_results(page: Page, wanted: Locator) -> Locator:
    page.wait_for_load_state('domcontentloaded')
    next_button = page.locator("a.next.page-numbers")

    while wanted.count() == 0 and next_button.count() > 0:
        with page.expect_navigation(wait_until='domcontentloaded'):
            next_button.click()

    if wanted.count() == 0:
        pytest.fail("No one search result have 'study programs''")
    return wanted.first


@pytest.mark.parametrize(
    "language, html_lang, about_heading",
    [
        ("lt", "lt-LT", "Apie mus"),
        ("be", "bel", "Пра нас"),
        ("ru", "ru-RU", "О нас"),
    ],
    ids=['lithuanian', 'belarusian', 'russian'],
)
def test_language_change(page: Page, language, html_lang, about_heading):
    page.goto("/")

    grid = page.locator("//div[contains(@class,'grid')]")
    language_switcher = grid.locator("//ul[contains(@class, 'language-switcher')]")
    language_switcher.hover()
    language_switcher.locator(f"//a[text()='{language}']").click()

    expect(page).to_have_url(re.compile(rf"https://{language}\.ehuniversity\.lt"))

    expect(page.locator("html")).to_have_attribute("lang", html_lang)
    expect(page.get_by_role("heading", name=about_heading)).to_be_visible()


def test_contact_info(page: Page):
    page.goto("/contact/")

    email = page.get_by_role("link", name="franciskscarynacr@gmail.com")
    expect(email).to_be_visible()
    expect(email).to_have_attribute("href", "mailto:franciskscarynacr@gmail.com")

    expect(page.locator("li", has_text="Phone (LT)")).to_contain_text("+370 68 771365")
    expect(page.locator("li", has_text="Phone (BY)")).to_contain_text("+375 29 5781488")

    expect(page.get_by_text("Join us in the social networks")).to_be_visible()
    for network in ["Facebook", "Telegram", "VK"]:
        expect(page.get_by_role("link", name=network, exact=True)).to_be_visible()

