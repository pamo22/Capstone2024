import os
from scraper import scrape
from comparison_v2 import comparison_cancel

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

    match input():
        case '1':
            print("You pressed 1")
            scrape(input("Input url to be scraped: "))
        case '3':
            print("You pressed 3")
            #temp file names
            file1 = "src/eg_1.txt"
            file2 = "src/eg_2.txt"
            comparison_cancel(file1, file2, "comparison_output.txt")
        case _:
            print("invalid input") #should ignore invalid input but fine for now

main();
menu_options()
