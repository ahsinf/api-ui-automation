import pytest
from datetime import datetime

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call":
        # Ambil screenshot setiap test selesai
        feature_request = item.funcargs.get("page")
        if feature_request:
            screenshot_path = f"screenshots/scr_{datetime.now().strftime('%H%M%S')}.png"
            feature_request.screenshot(path=screenshot_path)
            
            # Masukkan gambar ke dalam HTML Report
            if pytest_html is not None:
                extra.append(pytest_html.extras.image(screenshot_path))
        report.extra = extra