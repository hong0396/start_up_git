
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def search():
    driver = webdriver.Chrome()
    driver.get("https://www.taobao.com/")
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
    )
    click = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button"))
    )

    element.send_keys('meishi')
    click.click()



search()







#
#
# driver.get("http://www.python.org")
# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# elem.send_keys("selenium")
# elem.send_keys(Keys.RETURN)
# assert "Google" in driver.title
# driver.close()
# driver.quit()