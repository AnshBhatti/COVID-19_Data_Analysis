from selenium import webdriver
import pandas as pd
def acquire_ghs():
    browser=webdriver.Chrome("chromedriver.exe")
    browser.implicitly_wait(10)
    browser.get("https://www.ghsindex.org/")
    table=browser.find_element_by_class_name("countryTable")
    btn=browser.find_element_by_xpath("//button[@class='seeCompleteList button']")
    btn.click()
    content=pd.read_html(browser.page_source)[0]
    content=content[[content.columns[1],content.columns[2]]]
    countries=content["Country"]
    scores=content[content.columns[1]]
    for a in range(len(countries)):
        countries[a]=countries[a][9:]
        scores[a]=float(scores[a][13:17])
    content["Country"]=countries
    content[content.columns[1]]=scores
    content.to_csv("ghs.csv",index=False)
    browser.quit()
