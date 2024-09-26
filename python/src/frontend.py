import os
from scraper import scrape_obj
from comparison_v2 import compare_obj
from dbinterface import dbinterface
import uuid

#courtesy of https://patorjk.com/software/taag/
os.system('cls' if os.name == 'nt' else 'clear')
exit = False


def main():
    print('''    ___
       / (_)__________________ _____  ___     ____  _________
      / / / ___/ ___/ ___/ __ `/ __ \\/ _ \\   / __ \\/ ___/ __ \\
     / / (__  ) /__/ /  / /_/ / /_/ /  __/  / /_/ / /  / /_/ /
    /_/_/____/\\___/_/   \\__,_/ .___/\\___/  / .___/_/   \\____/
                            /_/           /_/                 ''')

def menu_options():
    print("1. Add license to tracker")
    print("2. Check for license changes") 
    print("3. Edit license (not implemented) ")
    print("4. View license ")
    print("5. Delete license from tracker") 
    scraperhandle = scrape_obj()
    mongohandle = dbinterface(scraperhandle)
    comparehandle = compare_obj()

    match input():
        case '1':
            print("You pressed 1")
            try:
                url = input("Input url to be scraped: ")
                title = input("Please input a name to refer to this licence by: ")
                frequency = int(input("How often should this be checked (hours): "))
                mongohandle.add_tracker(title, url, frequency)
            except TypeError:
                print("invalid input, please try again")

        case '2':
            mongohandle.tracker_list_select(mongohandle.check_license_changed)

        case '4':
            mongohandle.licenses_list_select(mongohandle.view_license)


        case '5':
            mongohandle.tracker_list_select(mongohandle.delete_tracker_item)

        case '6':
            print("You pressed 6")
            print(scraperhandle.save_to_file(input("Input url to be scraped: ")))
        
        case '7':
            print("You pressed 7")
            print(comparehandle.checksum(file1))
            print(comparehandle.checksum(file2))
            print("COMPARING DIFF CHECKSUMS: ")
            print(comparehandle.checksum_compare(file1, file2))
            print(comparehandle.checksum_compare(file2, file1))
            print("COMPARING SAME CHECKSUMS: ")
            print(comparehandle.checksum_compare(file1, file1))
            print(comparehandle.checksum_compare(file2, file2))
        case '8':
            
            print(mongohandle._check_license_changed("https://example.com"))
            


        case 'q':
            print("exiting...")
            exit = True
        case _:
            print("invalid input") #should ignore invalid input but fine for now

main();
while (not exit):
    menu_options()
