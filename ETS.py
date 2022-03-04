import requests
import bs4
import csv

#This script scraps info from ETS.kz - open auctions
#It takes description of tender, its amount, dates, number of tender

def start_scrapping():
    #initialization of lists - will be necessary to store scrapped info
    auct = []
    auct_lot = []
    auct_price = []
    auct_apply_date = []
    auct_final_date = []
    auct_tech_files = []

    #our URL that we are going to use - it shows all available tenders from the newest to oldest
    base_url = "https://ets.kz/announced-auctions/?sort=date&adesc=DESC"

    result = requests.get(base_url)

    soup = bs4.BeautifulSoup(result.text, "lxml")

    announced_auctions = soup.find_all('div', class_="i_announced_auctions_wrapper_item") #Info on all open tenders is stored here.

    for announced_auction in announced_auctions: #we will loop through all divs with tenders info
        auct.append(announced_auction.find("strong").text.strip()) #we save auction name
        auct_lot.append(announced_auction.find('span', class_="i_announced_auctions_wrapper_code").text.strip()) #we save auction lot number
        auct_price.append(announced_auction.find('strong', class_="i_announced_auctions_wrapper_amount").text.strip()) #we save auction budget price
        auct_apply_date.append(announced_auction.find('div', class_='i_announced_auctions_wrapper_introduction').find('strong').text[:10]) #we save tender apply date
        auct_final_date.append(announced_auction.find('span', class_='i_announced_auctions_wrapper_date').find('b').text) #we save date when tender happens
        auct_tech_files.append('https://ets.kz' + announced_auction.find_all('a')[1].get('href')) #this line takes the URL of PDF attachments as link

    tables = zip(auct, auct_lot, auct_price, auct_apply_date, auct_final_date, auct_tech_files) #all lists are zipped into one zip

    #lines below create a CSV file and put all gathere data into one table
    with open(file='ETS_tenders.csv', mode='w',encoding="utf-8", newline='') as file:
        writer = csv.writer(file, delimiter=';')

        for table in tables:
            writer.writerow(table)



def main():
    print("starting the process")
    start_scrapping()
    print("process is finished")


if __name__ == '__main__':
    main()
