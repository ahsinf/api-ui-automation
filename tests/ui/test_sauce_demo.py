import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

# --- POSITIVE CASES (TC-UI-001 to 010) ---

def test_tc_ui_001_to_005_login_and_dashboard(page: Page):
    login_page = LoginPage(page)
    inventory_page = DashboardPage(page)

    login_page.navigate()
    login_page.login("standard_user", "secret_sauce") # TC-UI-001
    
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html") # TC-UI-005
    inventory_page.verify_dashboard_elements() # TC-UI-002, 003, 004

@pytest.mark.parametrize("sort_option, mode", [
    ("az", "name_asc"),  # TC-UI-006
    ("za", "name_desc"), # TC-UI-007
    ("lohi", "price_asc"), # TC-UI-008
    ("hilo", "price_desc") # TC-UI-009
])
def test_tc_ui_006_to_009_sorting(page: Page, sort_option, mode):
    login_page = LoginPage(page)
    inventory_page = DashboardPage(page)

    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    
    inventory_page.sort_products(sort_option)
    
    if "name" in mode:
        results = inventory_page.get_all_item_names()
        expected = sorted(results) if mode == "name_asc" else sorted(results, reverse=True)
        assert results == expected
    else:
        results = inventory_page.get_all_item_prices()
        expected = sorted(results) if mode == "price_asc" else sorted(results, reverse=True)
        assert results == expected

def test_tc_ui_010_logout(page: Page):
    login_page = LoginPage(page)
    inventory_page = DashboardPage(page)

    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    inventory_page.logout()
    
    expect(page).to_have_url("https://www.saucedemo.com/") # TC-UI-010

# --- NEGATIVE CASES (TC-UI-011 to 016) ---

@pytest.mark.parametrize("tc_id, user, pwd, expected_err", [
    ("TC-UI-011", "wrong_user", "wrong_pswd", "Username and password do not match"),
    ("TC-UI-012", "", "", "Username is required"),
    ("TC-UI-013", "standard_user", "", "Password is required"),
    ("TC-UI-014", "", "secret_sauce", "Username is required"),
    ("TC-UI-015", "standard_user", "wrong_pswd", "Username and password do not match"),
    ("TC-UI-016", "wrong_user", "secret_sauce", "Username and password do not match"),
])
def test_negative_login_scenarios(page: Page, tc_id, user, pwd, expected_err):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(user, pwd)
    login_page.verify_error_message(expected_err)