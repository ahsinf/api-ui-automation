from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://www.saucedemo.com/"

        # Login selector
        self.input_username = self.page.locator('input[name="user-name"]')
        self.input_password = self.page.locator('input[name="password"]')
        self.login_btn = self.page.locator('input[type="submit"]')
        self.error_login = self.page.locator('h3[data-test="error"]')
        self.passed_login = self.page.locator(".product_label")

    def navigate(self):
        self.page.goto(self.url)

    def login(self, username, password):
        if username is not None: self.input_username.fill(username)
        if password is not None: self.input_password.fill(password)
        self.login_btn.click()

    def verify_error_message(self, expected_text):
        expect(self.error_login).to_be_visible()
        expect(self.error_login).to_contain_text(expected_text)