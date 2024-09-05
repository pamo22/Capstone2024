import os
from scraper import scrape_obj
from comparison_v2 import comparison_cancel
from dbinterface import dbinterface
import uuid

#courtesy of https://patorjk.com/software/taag/
os.system('cls' if os.name == 'nt' else 'clear')


def main():
    print('''    ___
       / (_)__________________ _____  ___     ____  _________
      / / / ___/ ___/ ___/ __ `/ __ \\/ _ \\   / __ \\/ ___/ __ \\
     / / (__  ) /__/ /  / /_/ / /_/ /  __/  / /_/ / /  / /_/ /
    /_/_/____/\\___/_/   \\__,_/ .___/\\___/  / .___/_/   \\____/
                            /_/           /_/                 ''')

def menu_options():
    print("1. Scrape custom url")
    print("2. Run scrape tests") # idk if pytest likes being called from here
    print("3. Compare 2 files")
    print("4. Run compare tests") # idk if pytest likes being called from here
    print("5. Scrape url and add to database")
    print("6. Scrape url and save to file")
    scraperhandle = scrape_obj()

    match input():
        case '1':
            print("You pressed 1")
            print(scraperhandle.get_text(input("Input url to be scraped: ")))

        case '3':
            print("You pressed 3")
            #temp file names
            file1 = "src/eg_1.txt"
            file2 = "src/eg_2.txt"
            comparison_cancel(file1, file2, "comparison_output.txt")
        case '5':
            print("You pressed 5")
            url = input("Input url to be scraped: ")
            filename = uuid.uuid4()
            scraped_text = scraperhandle.get_text(url)
            file = scraperhandle.save_to_file(url, filename)

            
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # PLAINTEXT CREDENTIALS IN SOURCE CODE || TESTING ONLY
            mongohandle = dbinterface("mongodb://mytester:databased1204@localhost:2701")
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            mongohandle.create_license(url, file[0], file[1])

        case '6':
            print("You pressed 6")
            print(scraperhandle.save_to_file(input("Input url to be scraped: ")))

        case _:
            print("invalid input") #should ignore invalid input but fine for now

main();
menu_options()
