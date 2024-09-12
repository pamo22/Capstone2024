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
                mongohandle.add_license(title, url, frequency)
            except TypeError:
                print("invalid input, please try again")

        case '2':
            print("You pressed 2")
            for i,item in enumerate(mongohandle.get_tracker_list()):
                print (str(i) + ": " + item['title'] + " | " + item['url'])
            sel = input ("please select a license to check: ")
            for i,item in enumerate(mongohandle.get_tracker_list()):
                if (i == int(sel)):
                    result = mongohandle.check_license_changed(item['_id'])
                    if (result[0]):
                        print("File unchanged")
                    else:
                        print("File has changed as follows:")
                        for tup in comparehandle.compare_bytes(result[1], mongohandle.get_old_content(item['_id'])):
                            print("line number " + str(tup[0]) + ": " + str(tup[1])) 
                        choice = input("would you like to update it in the database? (y/n)")
                        if (choice == "y" or choice == "Y"):
                            mongohandle._save_license_info(item['title'], item['url'], item['_id'])

            
        case '4':
            for i,item in enumerate(mongohandle.get_licenses_list()):
                print (str(i) + ": " + item['title'] + " | " + item['url'] )
            sel = input ("please select a license to view: ")
            for i,item in enumerate(mongohandle.get_licenses_list()):
                if (i == int(sel)):
                    mongohandle.delete_tracker_item(item['_id'])
        case '5':
            for i,item in enumerate(mongohandle.get_tracker_list()):
                print (str(i) + ": " + item['title'] + " | " + item['url'])
            sel = input ("please select a license to delete: ")
            for i,item in enumerate(mongohandle.get_tracker_list()):
                if (i == int(sel)):
                    mongohandle.delete_tracker_item(item['_id'])

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
