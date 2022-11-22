from selenium import webdriver
# import Action chains
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from robot.libraries.BuiltIn import BuiltIn

def perform_click(element):
    """

    :param element:
    :return:
    """
    #driver = BuiltIn().get_library_instance('SeleniumLibrary')

    action = ActionChains(driver)
    action.click(on_element=element)
    action.perform()

# get element
# driver = webdriver.Chrome()
# #
#
# driver.get("https://qauat02.logicmonitor.com")
# element = driver.find_element(By.XPATH, "//div[@class='ace_scroller']")
# perform_click(element, driver)
