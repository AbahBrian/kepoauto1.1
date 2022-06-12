import time
import random
import os
import schedule

from datetime import datetime as dt
from twilio.rest import Client 
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=4 , minute=26)
def scheduled_job():
    
    account_sid = os.environ["TWILIO_SID"] 
    auth_token = os.environ["TWILIO_TOKEN"]
    kepo_id = os.environ["KEPO_ID"]
    kepo_pass = os.environ["KEPO_PASS"]
    client = Client(account_sid, auth_token) 
    opt = Options()
    opt.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    opt.add_argument("--headless")
    opt.add_argument("--disable-extensions")
    opt.add_argument("--disable-gpu")
    opt.add_argument("--no-sandbox")
    opt.add_argument('--disable-dev-shm-usage')
    opt.add_experimental_option('prefs', {
        'geolocation': True
        })
    
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=opt)

    act = ActionChains(driver)


    latitude = [-6.1957654247079965,-6.194814169612861,-6.194814169612864]
    longitude = [107.17602245978799,107.17638035509395,107.17638035509394]
    i = random.choice([0, 1, 2])


    driver.execute_cdp_cmd(
        "Browser.grantPermissions",
         {
            "origin": "https://ieiapps.epson.biz:443",
            "permissions": ["geolocation"]
         },
     )
    
    driver.execute_cdp_cmd(
        "Emulation.setGeolocationOverride",
        {
            "latitude": latitude[i],
            "longitude": longitude[i],
            "accuracy": 100,
        },
    )

    time.sleep(3)

    driver.get("https://ieiappslogin.epson.biz/auth/realms/epson/protocol/openid-connect/auth?client_id=kepo&redirect_uri=https%3A%2F%2Fieiapps.epson.biz%2Fkepo%2Fsignin-oidc&response_type=code&scope=openid%20email%20profile%20roles&code_challenge=3n2DlKVL6Er_pGwsBUAsnm67rFOeg1cUO4vPwPkGtws&code_challenge_method=S256&response_mode=form_post&nonce=637825371611659124.ZWE1NjZiYWQtNzg4Yi00ZGI4LTg1MmUtYWZjY2M1N2NhOThjYzBmM2FmMjEtOWVlZS00NDExLWE1NmMtYjg0MGY4NDMwOTBm&state=CfDJ8IMpfE6zqLZBmi4Ei7a4eZF-DB07B9u9vu8MBl9i3Gn7R5GR3wE_i6eq80F854honpK22hNHz5p0lJ07QxEVVybqmQgVH9Nz0YUVNlbu-vtP96KWCwFeMgMzjayKf8M-an2pIezN6hFTkR74iVzwx2tBrxFr2ZB0ur4cfZrBXx7yI51DQ-AStFGXAP96n5snVoC_XyXrxxpPHsQZA_x87_JWvVQJqZn_9aOXhr-MrwBNb7GIdinyiRy3zXByjUsmy_cke3-Q5itojbYGPZ6mwQFYauBmEDxFC9YBghZl8PMyRB5yZJUwthLc5ijXZG6-1aE832c2vyk8MKT_FdGFqDW5PEez_4wnOYjOGhLLSH8aCQ501bii21T9g7NiqqDAtYI5ISiK4qDydz2WMuohGCI&x-client-SKU=ID_NETSTANDARD2_0&x-client-ver=5.5.0.0")

    time.sleep(10)
    driver.find_element_by_name("username").send_keys(kepo_id)
    time.sleep(10)
    driver.find_element_by_name("password").send_keys(kepo_pass)
    time.sleep(10)

    driver.find_element_by_css_selector("input[type=\"submit\"i]").click()
    
    time.sleep(30)
    
    try:
        login = driver.find_element_by_xpath("//h3[@class='display-5']")    
        if login.is_displayed():
            print ("Anda Berhasil Login")
    except NoSuchElementException:
        print ("Ada Masalah Saat Login, Pastikan ID dan Password Benar") 
    

    time.sleep(30)

    WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='k-dropdown-wrap k-state-default']"))).click()
    WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, "//li[@data-offset-index='3']"))).click()

    time.sleep(10)

    driver.find_element_by_id("MeetWith").send_keys("Istri,Anak,dan Orangtua")

    time.sleep (10)

    a = random.randint(1,3)
    x = range(a)
    for n in x:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//span[@title='Increase value']//span[@class='k-icon k-i-arrow-60-up']"))).click()
    
    time.sleep(10)
    
    suhu = driver.find_element_by_xpath("//input[@aria-valuenow]")
    suhunya = suhu.get_attribute("value")

    print ('Setting Suhu pada angka :' + suhunya)
    
    y = range(10)
    for n in y:
        driver.execute_cdp_cmd(
        "Emulation.setGeolocationOverride",
        {
            "latitude": latitude[i],
            "longitude": longitude[i],
            "accuracy": 100,
        },
     )    


    push = range(5)
    for n in push:
        driver.minimize_window()
        time.sleep (5)
        driver.maximize_window()
        time.sleep (5)
        act.send_keys(Keys.F8).perform()
        time.sleep (2)
        act.send_keys(Keys.F8).perform()
        time.sleep (2)
        act.send_keys(Keys.F8).perform()
        time.sleep (2)
        act.send_keys(Keys.F8).perform()
        time.sleep (2)
        driver.minimize_window()
        time.sleep (5)
        driver.maximize_window()
    
    time.sleep(10)

    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Submit']"))).click()

    time.sleep(10)

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Yes']"))).click()

    time.sleep(20)

    driver.get_screenshot_as_file(os.getcwd()+"/screeenshoot/"+"selenium"+".png")
    
    clo = dt.now()
    jam = clo.strftime("%X")
    
    kepo_ok = "Anda sudah berhasil kepo pada jam => " + jam + " !!! " + "Dengan Suhu : " + suhunya
    
    try:
        attem = driver.find_element_by_xpath("//span[@class='text-danger field-validation-error']")    
        if attem.is_displayed():
            print ("Anda Sudah Kepo Beberapa saat Lalu, Tunggu 1 atau 2 Jam lagi ")
            message = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body='Anda Sudah Kepo Beberapa saat Lalu, Tunggu 1 atau 2 Jam lagi',      
                              to='whatsapp:+6282112430501' 
                          ) 
    except NoSuchElementException:
        print ("Anda sudah berhasil KEPO !!")
        message = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body=kepo_ok,      
                              to='whatsapp:+6282112430501' 
                          )     
        driver.quit()
    
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=7 , minute=26)
def scheduled_job():
    
    account_sid = os.environ["TWILIO_SID"] 
    auth_token = os.environ["TWILIO_TOKEN"]
    kepo_id = os.environ["KEPO_ID"]
    kepo_pass = os.environ["KEPO_PASS"] 
    client = Client(account_sid, auth_token) 
    opt = Options()
    opt.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    opt.add_argument("--headless")
    opt.add_argument("--disable-extensions")
    opt.add_argument("--disable-gpu")
    opt.add_argument("--no-sandbox")
    opt.add_argument('--disable-dev-shm-usage')
    opt.add_experimental_option('prefs', {
        'geolocation': True
        })
    
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=opt)
    
    act = ActionChains(driver)


    latitude = [-6.1957654247079965,-6.194814169612861,-6.194814169612864]
    longitude = [107.17602245978799,107.17638035509395,107.17638035509394]
    i = random.choice([0, 1, 2])


    driver.execute_cdp_cmd(
        "Browser.grantPermissions",
         {
            "origin": "https://ieiapps.epson.biz:443",
            "permissions": ["geolocation"]
         },
     )
    
    driver.execute_cdp_cmd(
        "Emulation.setGeolocationOverride",
        {
            "latitude": latitude[i],
            "longitude": longitude[i],
            "accuracy": 100,
        },
    )

    time.sleep(3)

    driver.get("https://ieiappslogin.epson.biz/auth/realms/epson/protocol/openid-connect/auth?client_id=kepo&redirect_uri=https%3A%2F%2Fieiapps.epson.biz%2Fkepo%2Fsignin-oidc&response_type=code&scope=openid%20email%20profile%20roles&code_challenge=3n2DlKVL6Er_pGwsBUAsnm67rFOeg1cUO4vPwPkGtws&code_challenge_method=S256&response_mode=form_post&nonce=637825371611659124.ZWE1NjZiYWQtNzg4Yi00ZGI4LTg1MmUtYWZjY2M1N2NhOThjYzBmM2FmMjEtOWVlZS00NDExLWE1NmMtYjg0MGY4NDMwOTBm&state=CfDJ8IMpfE6zqLZBmi4Ei7a4eZF-DB07B9u9vu8MBl9i3Gn7R5GR3wE_i6eq80F854honpK22hNHz5p0lJ07QxEVVybqmQgVH9Nz0YUVNlbu-vtP96KWCwFeMgMzjayKf8M-an2pIezN6hFTkR74iVzwx2tBrxFr2ZB0ur4cfZrBXx7yI51DQ-AStFGXAP96n5snVoC_XyXrxxpPHsQZA_x87_JWvVQJqZn_9aOXhr-MrwBNb7GIdinyiRy3zXByjUsmy_cke3-Q5itojbYGPZ6mwQFYauBmEDxFC9YBghZl8PMyRB5yZJUwthLc5ijXZG6-1aE832c2vyk8MKT_FdGFqDW5PEez_4wnOYjOGhLLSH8aCQ501bii21T9g7NiqqDAtYI5ISiK4qDydz2WMuohGCI&x-client-SKU=ID_NETSTANDARD2_0&x-client-ver=5.5.0.0")

    time.sleep(10)
    driver.find_element_by_name("username").send_keys(kepo_id)
    time.sleep(10)
    driver.find_element_by_name("password").send_keys(kepo_pass)
    time.sleep(10)

    driver.find_element_by_css_selector("input[type=\"submit\"i]").click()
    
    time.sleep(30)
    
    try:
        login = driver.find_element_by_xpath("//h3[@class='display-5']")    
        if login.is_displayed():
            print ("Anda Berhasil Login")
    except NoSuchElementException:
        print ("Ada Masalah Saat Login, Pastikan ID dan Password Benar") 
    

    time.sleep(30)

    WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='k-dropdown-wrap k-state-default']"))).click()
    WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, "//li[@data-offset-index='3']"))).click()

    time.sleep(10)

    driver.find_element_by_id("MeetWith").send_keys("Istri,Anak,dan Orangtua")

    time.sleep (10)

    a = random.randint(1,3)
    x = range(a)
    for n in x:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//span[@title='Increase value']//span[@class='k-icon k-i-arrow-60-up']"))).click()
    
    time.sleep(10)
    
    suhu = driver.find_element_by_xpath("//input[@aria-valuenow]")
    suhunya = suhu.get_attribute("value")

    print ('Setting Suhu pada angka :' + suhunya)
    
    y = range(10)
    for n in y:
        driver.execute_cdp_cmd(
        "Emulation.setGeolocationOverride",
        {
            "latitude": latitude[i],
            "longitude": longitude[i],
            "accuracy": 100,
        },
     )    


    push = range(5)
    for n in push:
        driver.minimize_window()
        time.sleep (5)
        driver.maximize_window()
        time.sleep (5)
        act.send_keys(Keys.F8).perform()
        time.sleep (2)
        act.send_keys(Keys.F8).perform()
        time.sleep (2)
        act.send_keys(Keys.F8).perform()
        time.sleep (2)
        act.send_keys(Keys.F8).perform()
        time.sleep (2)
        driver.minimize_window()
        time.sleep (5)
        driver.maximize_window()
    
    time.sleep(10)

    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Submit']"))).click()

    time.sleep(10)

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Yes']"))).click()

    time.sleep(20)

    driver.get_screenshot_as_file(os.getcwd()+"/screeenshoot/"+"selenium"+".png")
    
    clo = dt.now()
    jam = clo.strftime("%X")
    
    kepo_ok = "Anda sudah berhasil kepo pada jam => " + jam + " !!! " + "Dengan Suhu : " + suhunya
    
    try:
        attem = driver.find_element_by_xpath("//span[@class='text-danger field-validation-error']")    
        if attem.is_displayed():
            print ("Anda Sudah Kepo Beberapa saat Lalu, Tunggu 1 atau 2 Jam lagi ")
            message = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body='Anda Sudah Kepo Beberapa saat Lalu, Tunggu 1 atau 2 Jam lagi',      
                              to='whatsapp:+6282112430501' 
                          ) 
    except NoSuchElementException:
        print ("Anda sudah berhasil KEPO !!")
        message = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body=kepo_ok,      
                              to='whatsapp:+6282112430501' 
                          )     
        driver.quit()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=10 , minute=26)
def scheduled_job():
    
    account_sid = os.environ["TWILIO_SID"] 
    auth_token = os.environ["TWILIO_TOKEN"]
    kepo_id = os.environ["KEPO_ID"]
    kepo_pass = os.environ["KEPO_PASS"] 
    client = Client(account_sid, auth_token) 
    opt = Options()
    opt.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    opt.add_argument("--headless")
    opt.add_argument("--disable-extensions")
    opt.add_argument("--disable-gpu")
    opt.add_argument("--no-sandbox")
    opt.add_argument('--disable-dev-shm-usage')
    opt.add_experimental_option('prefs', {
        'geolocation': True
        })
    
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=opt)

    act = ActionChains(driver)


    latitude = [-6.1957654247079965,-6.194814169612861,-6.194814169612864]
    longitude = [107.17602245978799,107.17638035509395,107.17638035509394]
    i = random.choice([0, 1, 2])


    driver.execute_cdp_cmd(
        "Browser.grantPermissions",
         {
            "origin": "https://ieiapps.epson.biz:443",
            "permissions": ["geolocation"]
         },
     )
    
    driver.execute_cdp_cmd(
        "Emulation.setGeolocationOverride",
        {
            "latitude": latitude[i],
            "longitude": longitude[i],
            "accuracy": 100,
        },
    )

    time.sleep(3)

    driver.get("https://ieiappslogin.epson.biz/auth/realms/epson/protocol/openid-connect/auth?client_id=kepo&redirect_uri=https%3A%2F%2Fieiapps.epson.biz%2Fkepo%2Fsignin-oidc&response_type=code&scope=openid%20email%20profile%20roles&code_challenge=3n2DlKVL6Er_pGwsBUAsnm67rFOeg1cUO4vPwPkGtws&code_challenge_method=S256&response_mode=form_post&nonce=637825371611659124.ZWE1NjZiYWQtNzg4Yi00ZGI4LTg1MmUtYWZjY2M1N2NhOThjYzBmM2FmMjEtOWVlZS00NDExLWE1NmMtYjg0MGY4NDMwOTBm&state=CfDJ8IMpfE6zqLZBmi4Ei7a4eZF-DB07B9u9vu8MBl9i3Gn7R5GR3wE_i6eq80F854honpK22hNHz5p0lJ07QxEVVybqmQgVH9Nz0YUVNlbu-vtP96KWCwFeMgMzjayKf8M-an2pIezN6hFTkR74iVzwx2tBrxFr2ZB0ur4cfZrBXx7yI51DQ-AStFGXAP96n5snVoC_XyXrxxpPHsQZA_x87_JWvVQJqZn_9aOXhr-MrwBNb7GIdinyiRy3zXByjUsmy_cke3-Q5itojbYGPZ6mwQFYauBmEDxFC9YBghZl8PMyRB5yZJUwthLc5ijXZG6-1aE832c2vyk8MKT_FdGFqDW5PEez_4wnOYjOGhLLSH8aCQ501bii21T9g7NiqqDAtYI5ISiK4qDydz2WMuohGCI&x-client-SKU=ID_NETSTANDARD2_0&x-client-ver=5.5.0.0")

    time.sleep(10)
    driver.find_element_by_name("username").send_keys(kepo_id)
    time.sleep(10)
    driver.find_element_by_name("password").send_keys(kepo_pass)
    time.sleep(10)

    driver.find_element_by_css_selector("input[type=\"submit\"i]").click()
    
    time.sleep(30)
    
    try:
        login = driver.find_element_by_xpath("//h3[@class='display-5']")    
        if login.is_displayed():
            print ("Anda Berhasil Login")
    except NoSuchElementException:
        print ("Ada Masalah Saat Login, Pastikan ID dan Password Benar") 
    

    time.sleep(30)

    WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='k-dropdown-wrap k-state-default']"))).click()
    WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, "//li[@data-offset-index='3']"))).click()

    time.sleep(10)

    driver.find_element_by_id("MeetWith").send_keys("Istri,Anak,dan Orangtua")

    time.sleep (10)

    a = random.randint(1,3)
    x = range(a)
    for n in x:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//span[@title='Increase value']//span[@class='k-icon k-i-arrow-60-up']"))).click()
    
    time.sleep(10)
    
    suhu = driver.find_element_by_xpath("//input[@aria-valuenow]")
    suhunya = suhu.get_attribute("value")

    print ('Setting Suhu pada angka :' + suhunya)
    
    y = range(10)
    for n in y:
        driver.execute_cdp_cmd(
        "Emulation.setGeolocationOverride",
        {
            "latitude": latitude[i],
            "longitude": longitude[i],
            "accuracy": 100,
        },
     )    


    push = range(5)
    for n in push:
        driver.minimize_window()
        time.sleep (5)
        driver.maximize_window()
        time.sleep (5)
        act.send_keys(Keys.F8).perform()
        time.sleep (2)
        act.send_keys(Keys.F8).perform()
        time.sleep (2)
        act.send_keys(Keys.F8).perform()
        time.sleep (2)
        act.send_keys(Keys.F8).perform()
        time.sleep (2)
        driver.minimize_window()
        time.sleep (5)
        driver.maximize_window()
    
    time.sleep(10)

    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Submit']"))).click()

    time.sleep(10)

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Yes']"))).click()

    time.sleep(20)

    driver.get_screenshot_as_file(os.getcwd()+"/screeenshoot/"+"selenium"+".png")
    
    clo = dt.now()
    jam = clo.strftime("%X")
    
    kepo_ok = "Anda sudah berhasil kepo pada jam => " + jam + " !!! " + "Dengan Suhu : " + suhunya
    
    try:
        attem = driver.find_element_by_xpath("//span[@class='text-danger field-validation-error']")    
        if attem.is_displayed():
            print ("Anda Sudah Kepo Beberapa saat Lalu, Tunggu 1 atau 2 Jam lagi ")
            message = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body='Anda Sudah Kepo Beberapa saat Lalu, Tunggu 1 atau 2 Jam lagi',      
                              to='whatsapp:+6282112430501' 
                          ) 
    except NoSuchElementException:
        print ("Anda sudah berhasil KEPO !!")
        message = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body=kepo_ok,      
                              to='whatsapp:+6282112430501' 
                          )     
        driver.quit()

sched.start() 
