# python 3.6

import pandas as pd

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TWAIT = 1


def punch_pin(browser, wait, pin):
    
    wait.until(EC.presence_of_element_located((By.ID, 'SearchFormEx1_PINTextBox0')))
    
    browser.find_element_by_id('SearchFormEx1_PINTextBox0').clear()
    browser.find_element_by_id('SearchFormEx1_PINTextBox1').clear()
    browser.find_element_by_id('SearchFormEx1_PINTextBox2').clear()
    browser.find_element_by_id('SearchFormEx1_PINTextBox3').clear()
    browser.find_element_by_id('SearchFormEx1_PINTextBox4').clear()    
    
    browser.find_element_by_id('SearchFormEx1_PINTextBox0').send_keys('%02d' % (pin // 10e11))
    browser.find_element_by_id('SearchFormEx1_PINTextBox1').send_keys('%02d' % (pin // 10e9 % 10e1))
    browser.find_element_by_id('SearchFormEx1_PINTextBox2').send_keys('%03d' % (pin // 10e6 % 10e2))
    browser.find_element_by_id('SearchFormEx1_PINTextBox3').send_keys('%03d' % (pin // 10e3 % 10e2))
    browser.find_element_by_id('SearchFormEx1_PINTextBox4').send_keys('%04d' % (pin % 10e3))
    
    browser.find_element_by_id('SearchFormEx1_btnSearch').click()
    
    time.sleep(TWAIT)


def get_doc_data(browser, wait):

    wait.until(EC.presence_of_element_located((By.ID, 'DocDetails1_GridView_Details_ctl02_ctl00')))

    return {
        'doc_no':        [browser.find_element_by_id('DocDetails1_GridView_Details_ctl02_ctl00').text],
        'date_executed': [browser.find_element_by_id('DocDetails1_GridView_Details_ctl02_ctl01').text],
        'date_recorded': [browser.find_element_by_id('DocDetails1_GridView_Details_ctl02_ctl02').text],
        'doc_type':      [browser.find_element_by_id('DocDetails1_GridView_Details_ctl02_ctl03').text],
        'amount':        [browser.find_element_by_id('DocDetails1_GridView_Details_ctl02_ctl05').text],
        'PIN_1st':       [browser.find_element_by_id('DocDetails1_GridView_LegalDescription_ctl02_ctl00').text],
        'prop':          [browser.find_element_by_id('DocDetails1_GridView_LegalDescription_ctl02_ctl01').text],
        'unit_no':       [browser.find_element_by_id('DocDetails1_GridView_LegalDescription_ctl02_ctl02').text],
        'STR':           [browser.find_element_by_id('DocDetails1_GridView_LegalDescription_ctl02_ctl03').text],
        'sub_div':       [browser.find_element_by_id('DocDetails1_GridView_LegalDescription_ctl02_ctl04').text],
        'grantor_1st':   [browser.find_element_by_id('DocDetails1_GridView_Grantor_ctl02_ctl00').text],
        'grantee_1st':   [browser.find_element_by_id('DocDetails1_GridView_Grantee_ctl02_ctl00').text]
        }


def get_pin_data(browser, wait, pin):
    
    df_pin_list = []
    
    punch_pin(browser, wait, pin)
    
    more_pages = True
    while more_pages:

        for term in ['WARRANTY DEED', 'SPECIAL WARRANTY DEED', 'DEED IN TRUST', 'TRUSTEES DEED', 'CORRECTED DEED', 'DEED']:

            wait.until(EC.presence_of_element_located((By.ID, 'DocList1_ContentContainer1')))

            # don't know how this interacts as rhs of for with a reloading page so going the safe way
            elem_javas = [elem.get_attribute('href') for elem in browser.find_elements_by_link_text(term)]
            
            for elem_java in elem_javas:

                browser.execute_script(elem_java)
                time.sleep(TWAIT)
                
                df_pin_list.append(pd.DataFrame.from_dict(get_doc_data(browser, wait)))
                
        try:
            browser.find_element_by_id('DocList1_LinkButtonNext').click()
            time.sleep(TWAIT)
        except:
            more_pages = False
            
    df_pin = pd.concat(df_pin_list)
    df_pin['PIN'] = pin
    return df_pin


def get_pins_data(pins):

    # opening browser
    browser = webdriver.Chrome('chromedriver.exe')
    browser.maximize_window()
    wait = WebDriverWait(browser, 10) # seconds
    browser.get('http://162.217.184.82/i2/')
    time.sleep(5)

    df_list = []

    for pin in pins:
        
        # df_pin = get_pin_data(browser, wait, pin) # for quick and dirty testing

        retry = 5
        while retry > 0:
            try:
                df_pin = get_pin_data(browser, wait, pin)
                retry = 0
            except:
                retry -= 1
                if retry > 0:
                    print('Retrying %d. Attempts left: %d' % (pin, retry))
                else:
                    print('All attempts failed.')
                time.sleep(TWAIT)

        df_list.append(df_pin)

    df = pd.concat(df_list).reset_index(drop=True)

    df['amount'] = pd.to_numeric(df['amount'].replace({'\$':'', ',':''}, regex=True))
    df['date_executed'] = pd.to_datetime(df['date_executed'])
    df['date_recorded'] = pd.to_datetime(df['date_recorded'])

    df = df.sort_values('date_executed')

    return df


if __name__ == '__main__':

    pins = [17042200960000 + l4 for l4 in range(1001, 1010)]
    df = get_pins_data(pins)

    print(df)
