from pypresence import Presence
import time
import requests
from bs4 import BeautifulSoup
import os

id = 994345924761489510
RPC = Presence(id)
user_id = None

def menu():
    os.system("cls")
    global user_id
    user_name = os.getlogin()
    while True:
        try:
            if not os.path.exists("C:\\Users\\" + user_name + "\\AppData\\Roaming\\vk_rpc"):
                #создаем папку в AppData\Roaming
                os.mkdir("C:\\Users\\" + user_name + "\\AppData\\Roaming\\vk_rpc")
                continue
            #если файл с id нет, то создаем его
            if not os.path.exists("C:\\Users\\" + user_name + "\\AppData\\Roaming\\vk_rpc\\id.txt"):
                file = open("C:\\Users\\" + user_name + "\\AppData\\Roaming\\vk_rpc\\id.txt", "w")
                file.close()
                continue
            #если файл с id пустой, то запрашиваем id
            if os.stat("C:\\Users\\" + user_name + "\\AppData\\Roaming\\vk_rpc\\id.txt").st_size == 0:
                user_id = input("Введите id страницы: ")
                file = open("C:\\Users\\" + user_name + "\\AppData\\Roaming\\vk_rpc\\id.txt", "w")
                file.write(user_id)
                file.close()
                continue
            else:
                file = open("C:\\Users\\" + user_name + "\\AppData\\Roaming\\vk_rpc\\id.txt", "r")
                user_id = file.read()
                file.close()
                update()
        except TypeError:
            os.system("cls")
            print("ПОСТАВЬТЕ В НАСТРОЙКАХ ВК -Кому в интернете видна моя страница- ПУНКТ -ВСЕМ-!!!")
            time.sleep(1)
            continue
            

def get_song():
        response = requests.get("https://vk.com/id" + str(user_id))
        soup = BeautifulSoup(response.text, "html.parser")
        status = soup.find("div", {"class": "pp_status"})
        if status is None:
            return None
        else:
            status = status.text
            # получаем название песни
            song = status[status.find("«") + 1:status.find("»")]
            # получаем имя исполнителя
            artist = status[status.find("»") + 1:status.find("—") - 1]
            # получаем название альбома
            album = status[status.find("—") + 1:]
            url = "https://www.google.com/search?q=" + status + "&tbm=isch"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            images = soup.find_all("img")
            image = images[1]['src']
            return song, artist, album, image

def update():
    while True:
        try:
            if get_song() != False:
                song, artist, album, image = get_song()
                RPC.update(state=artist, details=album, large_image=image, large_text=song)
                time.sleep(10)
                os.system("cls")
                print("Статус обновлен")
                continue
            else:
                os.system("cls")
                print("Статус не обновлен")
                RPC.clear()
                time.sleep(5)
                continue
        except Exception as e:
            os.system("cls")
            print("ВКЛЮЧИТЕ -Трансляция аудиозаписей- К СЕБЕ НА СТРАНИЦУ!!!")
            time.sleep(1)
            continue


if __name__ == "__main__":
    RPC.connect()
    menu()
