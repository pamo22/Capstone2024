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
    print("1. Scrape custom url")
    print("2. Run scrape tests") # idk if pytest likes being called from here
    print("3. Compare 2 files")
    print("4. Compare 2 files and save to file") # idk if pytest likes being called from here
    print("5. Scrape url and add to database")
    print("6. Scrape url and save to file")
    print("8. Check if entry has changed")
    scraperhandle = scrape_obj()
    mongohandle = dbinterface(scraperhandle)
    comparehandle = compare_obj()

    match input():
        case '1':
            print("You pressed 1")
            print(scraperhandle.get_text(input("Input url to be scraped: ")))

        case '3':
            print("You pressed 3")
            #temp file names
            #file1 = "src/Comparison_cancelmethod/MonteChristo.txt"
            #file2 = "src/Comparison_cancelmethod/MonteChristo_altered.txt"
            
            file1 = "src/eg_1.txt"
            file2 = "src/eg_2.txt"
            comparehandle.compare_file_verbose(file1, file2)
            comparehandle.compare_file_verbose(file2, file1)
            comparehandle.compare_old_file_verbose(file1, file2)
            comparehandle.compare_old_file_verbose(file2, file1)

            
        case '4':
            print("You pressed 4")
            #temp file names
            file1 = "src/eg_1.txt"
            file2 = "src/eg_2.txt"
            comparehandle.compare_save_to_file(file1, file2,"F1compF2_differences.txt")
            comparehandle.compare_save_to_file(file2, file1,"F2compF1_differences.txt")
        case '5':
            print("You pressed 5")
            url = input("Input url to be scraped: ")
            title = input("Please input a name to refer to this licence by: ")
            frequency = input("How often should this be checked (hours): ")


            mongohandle.add_license(title, url, frequency)

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
