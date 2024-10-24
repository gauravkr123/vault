import requests
import os
import re
from colorama import Fore, Style
from multiprocessing import Pool
import multiprocessing
import shutil

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def log(text, style):
    print(style + str(text) + Style.RESET_ALL)

def download(passed_from_main):
    _path = passed_from_main[0]
    _item = passed_from_main[1]
    j = 1
    try:
        while True:
            try:
                filename = _item[_item.rfind("/") + 1:]
                _url = _item

                if os.path.isfile(_path + str(filename)):
                    log("           " + filename + " already exists.", Fore.LIGHTBLACK_EX)
                    break

                response = requests.get(_url, stream=True)
                with open(_path+str(filename), "wb") as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                    #for chunk in response.iter_content(chunk_size=None):
                    #    if chunk:
                    #        out_file.write(chunk)
                del response
                if out_file:
                    break
            except Exception as e:
                log(e, Fore.RED)
                os.remove(_path + str(filename))
                log("Failed attempt " + str(j) + " for " + filename + "\n", Fore.RED)
                log("Retrying "+ filename + "...", Fore.YELLOW)
                j += 1

    except Exception as e:
        print(e)
        print("Failed to Download")

if __name__ == '__main__':
    clear()

    #Change path here
    local_download_folder = "F:\Downloads\goFile"
    
    if os.path.isfile("URLs.txt"):
        print("URLs.txt exists")
    else:
        f = open("URLs.txt", "w+")
        print("URLs.txt created")

    if os.stat("URLs.txt").st_size == 0:
        print("Please put URLs in URLs.txt")

    file_object = open("URLs.txt", "r")
    for line in file_object:
        url = line.rstrip()

        folderId = url[url.rfind("/") + 1:]
        try:
            path =  local_download_folder + "/" + folderId + "/"
            os.mkdir(path)
        except OSError:
            print("Creation of directory %s failed" % path)
        else:
            print()
            print ("Directory %s was created" % path)
        print()
        print("Downloading %s " %folderId)

        createAccountAPI = "https://api.gofile.io/createAccount"
        getAccount = requests.get(createAccountAPI)
        accountJSON = getAccount.json()
        sessionToken = accountJSON["data"]["token"]
        contentAPIPrefix = "https://api.gofile.io/getContent?contentId=" 
        urlCall = contentAPIPrefix+folderId+"&token="+sessionToken
        getFolder = requests.get(urlCall)
        folderJSON = getFolder.json()
        fileListSize = len(folderJSON["data"]["contents"])
        pass_to_func = []
        for i in folderJSON["data"]["contents"]:
            fileId = folderJSON["data"]["contents"][i]["id"]
            fileLink = folderJSON["data"]["contents"][i]["link"]
            fileName = folderJSON["data"]["contents"][i]["name"]
            pass_to_func.append([path, fileLink]) 

        print("Downloading " + str(len(pass_to_func)) + " files...")
        pool = Pool(processes = multiprocessing.cpu_count())
        proc = pool.map_async(download, pass_to_func)
        proc.wait()
        pool.close()

    ex = input("\nFinished. Press enter to quit.")