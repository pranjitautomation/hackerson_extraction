from RPA.Browser.Selenium import Selenium
from time import *
import re
import csv 


browser = Selenium()

def open_browser():
    browser.open_available_browser("https://www.heycarson.com/task-catalog-browse/task-types/development")
    sleep(5)

def extracting_link():
    """
    this method extract links of all the task card
    """
    link =[]
    for j in range (1,17):
        #taking innerhtml of all the page one by one
        html = browser.get_element_attribute('xpath://*[@id="page-results"]/div[1]/div','innerHTML')
        sleep(2)

        # Extracts the links of all the task card using regex
        extract = re.findall('class="task-catalog__card__title__container" href="(.+?)">',html)
        link.append(extract)

        try:
            #clicking the next element for going to next page
            browser.click_element('css:#page-results > div.marketplace-search-results__pagination > div > a.soft-pagination__page.soft-pagination__page--next')
        except:
            pass
    
    link.remove(link[0])
    print("linkkk          :",link)
    return link

def extracting_rows_for_csv():
    """
    This method extracts rows for csv
    """
    link = extracting_link()
    row = []
    rows = []
    for i in range (0,len(link)):
        hor = link[i]
        for z in range(0,len(hor)):
            browser.go_to('https://www.heycarson.com'+hor[z]) #Going to each task card one by one

            sleep(2)
            description = browser.get_text('xpath://*[@id="root"]/div[4]/div/div[1]/div[5]') #taking the text of description
            
            value = hor[z].split("/")[-1]
            try:
                preview = browser.get_element_attribute('xpath://*[@id="root"]/div[4]/div/div[1]/div[4]/div[1]/a',"href") #taking the demo preview link if present
                
            except:
                preview = "NAN"

            row.append(value)
            row.append(description)
            row.append(preview)
            rows.append(row)
            row = []

    return rows

def making_csv():
    rows = extracting_rows_for_csv()
# field names 
    fields = ['Task Name', 'Descriptions', 'Demo preview'] 

    # name of csv file 
    filename = "data.csv"
        
    # writing to csv file 
    with open(filename, 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields 
        csvwriter.writerow(fields) 
            
        # writing the data rows 
        csvwriter.writerows(rows)

def minimal_task():
    open_browser()
    making_csv()
    print("Done.")


if __name__ == "__main__":
    minimal_task()
