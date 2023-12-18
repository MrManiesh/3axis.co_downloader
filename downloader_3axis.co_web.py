import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import datetime
import colorama
from colorama import Fore, Style

url = 'http://3axis.co'



def forEachPage(pageNo):

    if not os.path.exists('Downloaded_files'):
        os.makedirs('Downloaded_files')


    pagePath = f'Downloaded_files/page_{pageNo}'

    if not os.path.exists(pagePath):
        os.makedirs(pagePath)

    pageUrl = r'https://3axis.co'
    if pageNo != 1:
        pageUrl = f'https://3axis.co/page/{pageNo}/'
    

    with open(f'{pagePath}/failed_log.txt','a') as f:
        f.write('--------------------------------------------------------------')
        f.write(f'\nLog: Page - {pageNo}\n')
        f.write('--------------------------------------------------------------\n')

    def logStore(logMsg):
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        
        with open(f'{pagePath}/failed_log.txt','a') as f:
            f.write(f'{formatted_datetime} - {logMsg}\n')
            

    print(Fore.YELLOW + Style.BRIGHT + '--------------------------------------------------------------')
    print('🌐 Visiting Website:', url)
    print("🛠️  Working with Page - ",pageNo)
    print(Fore.YELLOW + Style.BRIGHT + '--------------------------------------------------------------\n\n')

    print(Fore.YELLOW + Style.BRIGHT + "🔍 Looking for Source Code")

    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        
        # driver.maximize_window()
        # browser = webdriver.Chrome(options=options)
        driver.get(pageUrl)
        # print(f"{pageUrl.replace('/','')} - {driver.current_url.replace('/','')}")
        if pageUrl.replace('/','') != driver.current_url.replace('/',''):
            print(f'Invalid page number - {pageNo}')
            return 0

        pageSource = driver.page_source
        driver.quit()
        print(Fore.GREEN + '✅ Source Code Successfully Retrieved')
    except:
         logStore('Unable to Retrieve Source Code')
         print(Fore.RED + '❌ Unable to Retrieve Source Code')


    print(Fore.YELLOW + Style.BRIGHT + '📌 Extracting Links and Names...')
    try :
        soup = BeautifulSoup(pageSource, 'html.parser')
        post_items = soup.find_all('div', class_='post-item')

        products = []
        for item in post_items:
            product_name_element = item.find('h2', class_='post-subject')
            product_link_element = item.find('a', href=True)

            if product_name_element and product_link_element:
                product_name = product_name_element.text.strip()
                product_link = product_link_element['href'].strip()

                products.append([product_name, product_link])    
        print(Fore.GREEN + '✅ Links Successfully Extracted')
    except:
        logStore('Link Extraction Failed')
        print(Fore.RED + '❌ Link Extraction Failed')

    # products = products[10:] # remove this line - testing purpose only
    # products = [products[-5]] # remove this line - testing purpose only
    for oneProducts in products:
        print(Fore.YELLOW + Style.BRIGHT + '📂 Processing:', oneProducts[0])
        # break
        file_extensions = ['cdr','dxf', 'stl', 'bmp','pdf','dwg','svg'] 

        def download_file(url, destination):
            # try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
                
                with open(f'{pagePath}/{destination}', 'wb') as file:
                    file.write(response.content)
                
                return (True, Fore.GREEN + f"✅ Downloaded Successfully: {destination}")
        
            # except requests.exceptions.RequestException as e:
            #     logStore(f"Error Downloading File: {e}")
            #     print(Fore.RED + f"❌ Error Downloading File: {e}")
            #     return False




        def try_download_file(file_extension):
            try:
                url = f"https://files.3axis.co/docs/{file_extension}/{oneProducts[1].split('/')[-1]}.{file_extension}"
                return download_file(url, f'{oneProducts[0]}.{file_extension}')
                
            except Exception as e:
                try:
                    url = f"https://files.3axis.co/docs/{file_extension}/{oneProducts[1].split('/')[-1]}.zip"
                    # print(url)
                    return download_file(url, f'{oneProducts[0]}.{file_extension}')
                    # return True
                except Exception as e:
                    # logStore(f"Error Downloading {url, f'{oneProducts[0]}.{file_extension}'}: {e}")
                    return (False, Fore.RED + f"Error Downloading {url, f'{oneProducts[0]}.{file_extension}'}: {e}")
                    # return False
      

        found = False
        tryRes = ''
        for extension in file_extensions:
            # print('extension ::::::: ',extension)
            tryRes = try_download_file(extension)
            if tryRes[0] == True:
                found = True
                break

        if found == False:
            print('❌ ', end='')
            print(tryRes[1])
            logStore(tryRes[1])
        else:
            print(tryRes[1])



# ===================================================

def print_fancy_text(text):
    print(Fore.MAGENTA + Style.BRIGHT + text + Style.RESET_ALL)

print_fancy_text("\nWelcome to 3Axis.com Downloader\n")

while True:
    print(Fore.CYAN + "Select Options:")
    print("\n1. Download new files")
    print("\033[9m2. Download failed files again\033[0m")
    print(Fore.CYAN + "3. Exit\n")

    choice = input(Fore.CYAN + "Enter your choice: ")

    if choice == '1':
        print('\nEnter Page Number')
        try:
            fromChoice = int(input(Fore.CYAN + "\nfrom : "))
            toChoice = int(input(Fore.CYAN + "\nto : "))
        except:
            print('\n--------------------------------------------------------------\n')      
            print('Enter valid numbers')
            print('\n--------------------------------------------------------------\n')      
            continue
        print('\n')

        for one in range(int(fromChoice), int(toChoice) + 1):
            try:
                forEachPage(one)
            except:
                print('\n--------------------------------------------------------------\n')      
                print(f'Something wents wrong with page - {one}')
            print('\n--------------------------------------------------------------\n')      
    
    elif choice == '2':
        print('\n--------------------------------------------------------------\n')      
        print('Not available yet')
        print('\n--------------------------------------------------------------\n')      
        
    
    elif choice == '3':
        print_fancy_text("Exiting the downloader. Goodbye!")
        break

    else:
        print(Fore.RED + "Invalid choice. Please enter a valid option.")


# ===================================================

