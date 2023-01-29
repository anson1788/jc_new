import requests as req
from selenium import webdriver
import bs4
import json
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import os
import iphone_monitor as monitor

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_experimental_option("detach", True)


def start_purchasing(num,city):
    time.sleep(8)
    driver.find_element("xpath",'//*[@id="noTradeIn"]').click()      # Click on no Button
    time.sleep(3)
    driver.execute_script("document.getElementsByClassName('button button-block')[0].click()")         # Add to Bag
    time.sleep(4)
    driver.find_element("name",'proceed').click()                    # Review Bag
    time.sleep(3)
    select = Select(driver.find_element("class name",'rs-quantity-dropdown'))            # select quantity of phones
    select.select_by_value(str(num))
    driver.find_element(by=By.ID,value='shoppingCart.actions.navCheckout').click()       # click on checkout
    time.sleep(3)
    driver.find_element("class name",'form-button').click()           #sign in as guest


    time.sleep(3)
    driver.execute_script("window.document.getElementById('fulfillmentOptionButtonGroup1').click()")
    time.sleep(3)
#     try:
    driver.find_element("class name",'form-textbox-input').send_keys(city)
    driver.find_element("id",'checkout.fulfillment.pickupTab.pickup.storeLocator.search').click()
#     except:
#         pass
    time.sleep(3)


# In[31]:


def area_selection(page,u_name,l_name,u_email,cardnum,expire,cvv,add,gift_code,slot,payment_check):
    a_store=[]
    ids_of_available_stores=page.find_all('div',attrs={'class':'as-storelocator-searchitem'})
    for i in ids_of_available_stores:
        try:
            c=i.find('span',attrs={'class':'as-storelocator-available-quote'}).text
        except:
            c=''
        if "Available" in c:
            print(c)
            print(i.find('span',attrs={'class':'form-label-small as-storelocator-selector'}).text)
            print(i.find('input')['id'])
            a_store.append((c,i.find('span',attrs={'class':'form-label-small as-storelocator-selector'}).text,i.find('input')['id']))
    # a_store
    driver.find_element(by=By.ID,value=a_store[0][2]).click()
    time.sleep(2)
    select1 = Select(driver.find_element("class name",'form-dropdown-select'))            # select quantity of phones
    select1.select_by_index(int(slot))
    time.sleep(1)
    driver.execute_script("document.getElementById('rs-checkout-continue-button-bottom').click()")

    time.sleep(3)
    driver.find_element("name",'firstName').send_keys(u_name)
    driver.find_element("name",'lastName').send_keys(l_name)
    driver.find_element("name",'emailAddress').send_keys(u_email)
    driver.find_element("name",'mobilePhone').send_keys(11223344)
    driver.execute_script("document.getElementById('rs-checkout-continue-button-bottom').click()")

    time.sleep(3)

    if int(payment_check)==1:
        driver.find_element("name",'checkout.billing.billingOptions.selectBillingOption').click()
        time.sleep(2)
        driver.find_element("name",'cardNumber').send_keys(int(cardnum))
        driver.find_element("name",'expiration').send_keys(expire)
        driver.find_element("name",'securityCode').send_keys(cvv)
        driver.find_element("name",'firstName').send_keys(u_name)
        driver.find_element("name",'lastName').send_keys(l_name)
        driver.find_element("name",'street').send_keys(add)
        driver.execute_script("document.getElementById('rs-checkout-continue-button-bottom').click()")
    else:
        driver.execute_script("document.body.getElementsByClassName('rs-payment-giftcard-toggle as-buttonlink as-util-fadein')[0].click()")
        time.sleep(2)
        driver.find_element("class name",'form-textbox-input').send_keys(gift_code)
        driver.find_element("class name",'apply-button').click()    
        

    time.sleep(3)
    driver.execute_script("document.getElementById('rs-checkout-continue-button-bottom').click()")   # last click


# In[32]:


def Run_fun(u_name,l_name,u_email,cardnum,expire,cvv,gift_code,add,num,slot,city,payment_check):
    start_purchasing(num,city)
    d1=driver.find_element(by=By.ID,value='rs-fulfillment-storelocator-error')
    if "Please try another search." in d1.text:
        driver.find_element(by=By.ID,value='rs-fulfillment-cityStateField').click()
        time.sleep(2)
        driver.find_element("class name",'form-textbox-input').clear()
        driver.find_element("class name",'form-textbox-input').send_keys('ShaTin')
        driver.find_element("class name",'apply-button').click()

        time.sleep(3)
        d2=driver.find_element(by=By.ID,value='rs-fulfillment-storelocator-error')
        if "Please try another search." in d2.text:
            driver.find_element(by=By.ID,value='rs-fulfillment-cityStateField').click()
            time.sleep(2)
            driver.find_element("class name",'form-textbox-input').clear()
            driver.find_element("class name",'form-textbox-input').send_keys('Tsim Sha Tsui')
            driver.find_element("class name",'apply-button').click()

            time.sleep(3)
            d3=driver.find_element(by=By.ID,value='rs-fulfillment-storelocator-error')
            if "Please try another search." in d3.text:
                print('no stock near to you')
            else:
                page=bs4.BeautifulSoup(driver.page_source,'html')
                area_selection(page,u_name,l_name,u_email,cardnum,expire,cvv,add,gift_code,slot,payment_check)            
        else:
            page=bs4.BeautifulSoup(driver.page_source,'html')
            area_selection(page,u_name,l_name,u_email,cardnum,expire,cvv,add,gift_code,slot,payment_check)

    else:
        page=bs4.BeautifulSoup(driver.page_source,'html')
        area_selection(page,u_name,l_name,u_email,cardnum,expire,cvv,add,gift_code,slot,payment_check)
    


# In[3]:


l1=monitor.user_input_data()


# In[33]:


for i in range(len(l1)):
    #driver=webdriver.Chrome('chromedriver.exe')
    driver = webdriver.Chrome(executable_path='/Users/hello/Desktop/chrome/chromedriver107',options=chrome_options)

    driver.get(l1[i][0])
    num,u_name,l_name,u_email,cardnum,expire,cvv,gift_code,add,slot,city,payment_check=l1[i][1],l1[i][2],l1[i][3],l1[i][4],l1[i][5],l1[i][6],l1[i][7],l1[i][8],l1[i][9],l1[i][10],l1[i][11],l1[i][12]
    Run_fun(u_name,l_name,u_email,cardnum,expire,cvv,gift_code,add,num,slot,city,payment_check)
    print("Process Successfully Completed!!!")
    with open('log.txt','a') as f:
        f.write(time.ctime()+'  Process Successfully Completed!!\n')


# In[ ]:


# 1. Kowloon Tong. 2. ShaTin. 3. Tsim Sha Tsui

