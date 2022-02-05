from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import io
import requests
import pytesseract
from PIL import Image


options = Options()
options.headless=True
driver=webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options, )
driver.get('https://www.amazon.com/errors/validateCaptcha')

list=driver.find_element_by_tag_name('img')
url=list.get_attribute('src')

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

r = requests.get(url,headers=headers)
img = Image.open(io.BytesIO(r.content))
text = pytesseract.image_to_string(img)

print(text)