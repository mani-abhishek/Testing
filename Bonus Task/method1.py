from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from amazoncaptcha import AmazonCaptcha

options = Options()
options.headless=True

driver=webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options, )
driver.get('https://www.amazon.com/errors/validateCaptcha')

list=driver.find_element_by_tag_name('img')
link=list.get_attribute('src')



captcha = AmazonCaptcha.fromlink(link)
solution = captcha.solve()
print(solution)

