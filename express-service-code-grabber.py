from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import re
import PySimpleGUI as sg
#import asyncio

url = "http://support.dell.com"
TIMEOUT = 8


def express_service_code_lookup(serial_number, gui_window):
    # Update window
    window['_OUTPUT_'].update(value="instantiating a psuedo-firefox in RAM (Selenium for Python)", visible=True)
    window.refresh()

    # instantiate headless firefox
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    #driver = webdriver.Firefox()

    # load the Dell support page
    window['_OUTPUT_'].update(value="pulling down " + url)
    window.refresh()
    driver.get(url)

    # grab input box to 'type' our serial number in
    input_field = driver.find_element_by_name("entry-main-input")

    # submit our serial number:
    window['_OUTPUT_'].update(value="loading page for " + serial_number)
    window.refresh()
    input_field.click()
    input_field.send_keys(serial_number)
    input_field.submit()

    # now wait for the appropriate info on the next page to be downloaded, 
    # Dell uses a so-called 'Hero banner' laid out with Flexbox. It is a <div>
    # element that has the following class attribute "product-support-hero"
    css_selector = '.product-support-hero'
    try:
        product_info_has_loaded = EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        WebDriverWait(driver, TIMEOUT).until(product_info_has_loaded)
    except TimeoutException:
        window['_OUTPUT_'].update(value="Express service code not found. Typo?", visible=True)
        window.refresh()
        driver.close()
        return

    # feed into BeautifulSoup (content is in driver.page_source)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Iterate over <p> tags and find the express service code.
    # Once found, close the browser and return
    for p in soup.find_all('p'):
        for child in p.children:
            if (re.findall("Express Service Code", child.string)):
                window['_OUTPUT_'].update(value=p.contents[1] + " (done)")
                window.refresh()

    driver.close() # close the invisible browser
    return

# ...::: GUI stuff :::... #
# window layout
layout = [  [sg.Text("Serial Number:")],
            [sg.InputText()],
            [sg.Text("01234567890123456789012345678901234567890123456789", key="_OUTPUT_", visible=False)],
            [sg.Button(bind_return_key=True, visible=False)]
        ]

# create window
window = sg.Window('Express Service Code Grabber', layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Close'):   # if user closes window or clicks cancel
        break
    express_service_code_lookup(values[0], window)

window.close()