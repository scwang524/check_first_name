from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest


keys = ('first_name', 'status', 'error')
# 正確樣本
passList = ['abc', 'Abc']
values = [(i, 1, '') for i in passList]
# 錯誤樣本
errDict = {
    'Please enter a valid first name': ['123', 'abc123'],
    'Maximum characters limit is 40': ['z'*41],
}
values += [(k, 0, i) for i, j in errDict.items() for k in j]


@pytest.mark.parametrize(keys, values)
class TestLogin:
    def setup(self):   
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-web-security')

        driver = webdriver.Chrome(options=options)
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get('https://acy.com/en/open-live-account')

    def teardown(self):
        self.driver.quit()

    def test_first_name(self, first_name, status, error):
        print(f'【{first_name}】')
        for _ in range(2):
            try:
                self.driver.find_element(By.CSS_SELECTOR, 'svg[fill="none"]').click()  # 確認網站出現
                break
            except:
                self.driver.refresh()

        self.driver.find_element(By.CSS_SELECTOR, 'div[class=" css-9qujs6"]').click()
        fillDict = {
            'input[name="firstName"]': first_name,
            'input[name="lastName"]': 'lalala',
            'input[class="form-control phone-input"]': '0912345678',
            'input[name="email"]': f'{first_name}@example.com',
            'input[name="password"]': 'Abcd1234',
        }
        for loc, content in fillDict.items():
            ele = self.driver.find_element(By.CSS_SELECTOR, loc)
            ele.clear()
            ele.send_keys(content)
            ele.submit()

        try:
            self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="continue button"]').click()  # 傳送鍵
        except:
            pass
        
        if status:
            sig = False
            try:
                self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="verify code button"]')  # 傳送成功   
                sig = True
            except:          
                pass
            assert sig == True
        else:
            assert error in self.driver.page_source

  
if __name__ == '__main__':
    pytest.main(['-s', 'test_main.py', '--disable-warnings', '--html=report.html'])         
