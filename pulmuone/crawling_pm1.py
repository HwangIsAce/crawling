from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager 

from pyshadow.main import Shadow

from selenium.common.exceptions import NoSuchElementException

import time

def append_to_file(string, filename='output.txt'):
    string = string.replace('\n', ' ')

    with open(filename, 'a') as file:
        file.write(string + '\n')

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--disable-dev-shm-usage")
options.add_argument("window-size=1920x1080")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
options.add_argument("lang=ko_KR")

# driver = webdriver.Chrome(
#     executable_path='/home/jaesung/jaesung/crawling/chromedriver-linux64/chromedriver', options=options
# )
service = Service(excutable_path=ChromeDriverManager().install()) 
driver = webdriver.Chrome(service=service, options=options)


for id in [v for v in range(5455, 5469)]:
    cnt = 1
    
    tmp = []
    while True:
        if len(tmp) > 2:
            break
        #
        driver.quit()
        driver = webdriver.Chrome(service=service, options=options)
        
        url = f"https://shop.pulmuone.co.kr/shop/goodsList?itemId={id}&page={cnt}"
        print(url)
        driver.get(url)
        time.sleep(3)
        
        for num in [u for u in range(1, 41)]:
            
            try:

                driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/section/div/div[2]/div[2]/div/div[1]/ul/li[{num}]/div').click()

                time.sleep(3)
                
                def get_shadow_root(element):
                    return driver.execute_script('return arguments[0].shadowRoot', element)

                try: 
                    shadow_host = driver.find_element(By.CLASS_NAME, 'shadow-dom__wrapper')

                    title = get_shadow_root(shadow_host).find_element(By.CLASS_NAME, 'detail_title').text
                    description = get_shadow_root(shadow_host).find_element(By.CLASS_NAME, 'detail_text').text    
                    
                    # save
                    append_to_file(title, 'title.txt')
                    append_to_file(description, 'description.txt')
                    
                except NoSuchElementException:
                    print('no element')

                driver.back()
                time.sleep(3)
                            
            except NoSuchElementException:
                tmp.append('no item')
                print('no item')
                
        cnt += 1
        # url = url[:-1] + str(cnt)
        
        driver.quit()


