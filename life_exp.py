from selenium import webdriver
import pandas as pd
def get_exp():
    browser=webdriver.Chrome("chromedriver.exe")
    browser.implicitly_wait(10)
    browser.get("https://www.worldometers.info/demographics/life-expectancy/")
    df=pd.read_html(browser.page_source)[0]
    del df["#"]
    del df["Females Life Expectancy"]
    del df["Males Life Expectancy"]
    df.drop(29)
    df.to_csv("life_exp.csv",index=False)
    browser.quit()
