from playwright.sync_api import Page, expect

class DashboardPage:
    def __init__(self, page: Page):
        self.page = page
        self.header_title = page.locator(".app_logo")
        self.product_list = page.locator(".inventory_list")
        self.cart_icon = page.locator(".shopping_cart_link")
        self.sort_dropdown = page.locator(".product_sort_container")
        self.inventory_item_name = page.locator(".inventory_item_name")
        self.inventory_item_price = page.locator(".inventory_item_price")
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("#logout_sidebar_link")

    def verify_dashboard_elements(self):
        expect(self.header_title).to_have_text("Swag Labs") # TC-UI-002
        expect(self.product_list).to_be_visible()         # TC-UI-003
        expect(self.cart_icon).to_be_visible()            # TC-UI-004

    def sort_products(self, option_value):
        self.sort_dropdown.select_option(option_value)

    def get_all_item_names(self):
        return self.inventory_item_name.all_inner_texts()

    def get_all_item_prices(self):
        prices = self.inventory_item_price.all_inner_texts()
        return [float(p.replace('$', '')) for p in prices]

    def logout(self):
        self.menu_button.click()
        self.logout_link.click()