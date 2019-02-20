import requests
import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

def scrape_all_imgs_google(searchTerm):

    def scroll_page():
        for i in range(7):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)

    def click_button():
        more_imgs_button_xpath = '//*[@id="smb"]'
        driver.find_element_by_xpath(more_imgs_button_xpath).click()

    def create_soup():
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, 'html.parser')

    def find_imgs(soup):
        imgs_urls = []
        for img in soup.find_all('img'):
            try:
                if img['src'].startswith('http'):
                    imgs_urls.append(img['src'])
            except:
                pass

    #create webdriver
    driver = selenium.webdriver.Chrome()

    #define url using search term
    searchUrl = "https://www.google.com/search?q={}&source=lnms&tbm=isch&sa=X&ved=0ahUKEwi5ydGM4cfgAhUgyosBHT7kCSQQ_AUIDigB&biw=1534&bih=1007".format(searchTerm)

    #get url
    driver.get(searchUrl)

    try:
        click_button()
        scroll_page()
    except:
        scroll_page()
        click_button()

    #create soup only after we loaded all imgs when we scroll'ed the page down
    create_soup()

    #find imgs in soup
    find_imgs()

    #close driver
    driver.close()

    #return list of all img urls found in page
    return imgs_urls

urls = scrape_all_imgs_google('dog')

print(len(urls))
print(urls)