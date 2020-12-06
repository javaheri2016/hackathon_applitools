from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome

import os

master_branch = "https://demo.applitools.com/tlcHackathonMasterV1.html"
dev_branch = "https://demo.applitools.com/tlcHackathonDev.html"
prod_branch = "https://demo.applitools.com/tlcHackathonMasterV2.html"

from applitools.selenium import (
    logger,
    VisualGridRunner,
    Eyes,
    Target,
    BatchInfo,
    BrowserType,
    DeviceName,
)


def set_up(eyes):

    # You can get your api key from the Applitools dashboard
    eyes.configure.set_api_key('APPLITOOLS_API_KEY')

    # Create a new batch info instance and set it to the configuration
    eyes.configure.set_batch(BatchInfo("Holiday Shopping"))

    # Add browsers with different viewports
    # Add mobile emulation devices in Portrait mode
    (
        eyes.configure.add_browser(1200, 800, BrowserType.CHROME)
            .add_browser(1200, 800, BrowserType.FIREFOX)
            .add_browser(1200, 800, BrowserType.EDGE_CHROMIUM)
            .add_browser(1200, 800, BrowserType.SAFARI)
            .add_device_emulation(DeviceName.iPhone_X)
    )


def main_page_test(web_driver, eyes):
    try:
        # Navigate to the url we want to test
        web_driver.get(prod_branch)

        # Call Open on eyes to initialize a test session
        eyes.open(
            web_driver, "AppliFashion", "Test 1"
        )

        # Check main page
        eyes.check("", Target.window().fully().with_name("main page"))

        # Call Close on eyes to let the server know it should display the results
        eyes.close_async()
    except Exception as e:
        eyes.abort_async()
        print(e)


def filter_by_color_test(web_driver, eyes):
    try:
        # Navigate to the url we want to test
        web_driver.get(prod_branch)

        # Call Open on eyes to initialize a test session
        eyes.open(
            web_driver, "AppliFashion", "Test 2"
        )

        # Check filters
        web_driver.find_element_by_id("LI____103").click()
        web_driver.find_element_by_id("filterBtn").click()
        eyes.check_region("#product_grid", "filter by color")

        # Call Close on eyes to let the server know it should display the results
        eyes.close_async()
    except Exception as e:
        eyes.abort_async()
        print(e)


def product_details_test(web_driver, eyes):
    try:
        # Navigate to the url we want to test
        web_driver.get(prod_branch)

        # Call Open on eyes to initialize a test session
        eyes.open(
            web_driver, "AppliFashion", "Test 3"
        )

        # Click on product
        web_driver.find_element_by_id("H3____218").click()

        # # Check the app page
        eyes.check("", Target.window().fully().with_name("product details"))

        # Call Close on eyes to let the server know it should display the results
        eyes.close_async()
    except Exception as e:
        eyes.abort_async()
        print(e)


def tear_down(web_driver, runner):
    # Close the browser
    web_driver.quit()

    # we pass false to this method to suppress the exception that is thrown if we
    # find visual differences
    all_test_results = runner.get_all_test_results()
    print(all_test_results)


# Create a new chrome web driver
web_driver = Chrome(ChromeDriverManager().install())

# Create a runner with concurrency of 1
runner = VisualGridRunner(1)

# Create Eyes object with the runner, meaning it'll be a Visual Grid eyes.
eyes = Eyes(runner)

set_up(eyes)

try:
    main_page_test(web_driver, eyes)
    filter_by_color_test(web_driver, eyes)
    product_details_test(web_driver, eyes)
finally:
    tear_down(web_driver, runner)
