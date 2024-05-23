import requests as rq
from bs4 import BeautifulSoup as bs
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

#Функция выбирает необходимую информацию со страницы и выводит статьи с искомыми словами:
        
def get_inf(link):
    full_inf = [] #Список с информацией о статье
    res = rq.get(url=link)
    soup = bs(res.text, 'lxml')
    Authors = soup.find_all('p', class_='AVev') #Поиск автора
    for a in Authors:
        author = a.get_text()
        full_inf.append('Автор:' + author)        
    Headline = soup.find_all('h1') #Поиск заголовка
    for h in Headline:
        head = h.get_text()
        full_inf.append('Заголовок:' + head)        
    Text = soup.find_all('section', class_ = 'KFalv') #Поиск аннотации
    for t in Text:
        allText = t.find('p', class_ =None).text
        full_inf.append('Аннотация:' + allText)
#Преобразование списка в строку для поиска слов и дальнейшей записи в log-файл:
    log = ''
    for i in full_inf:
        log += str(i)
        log += '\n'
#Оптимизациея скорости поиска по нескольким словам с использованием предварительно скомпелированных регулярных выражений:        
    for word in words:
        pattern = re.compile(r'\b{}\b'.format((re.escape(word)), re.IGNORECASE))
        found = bool(pattern.search(log))
        if found == True:
            print(log)
            
    return(log)

#Функция для поиска всех ссылок на главной странице и записи результата поиска содержания статей в файл:
def search_art():
    links = set() #Множество для поиска всех ссылок на странице ссылок
    driver = webdriver.Chrome(service = service) #Запуск драйвера
    driver.get('https://www.fontanka.ru/24hours_news.html') #Открытие страницы в браузере с помощью драйвера
    time.sleep(10) #Время на загрузку контента
    #Выбираем ссылки и записываем в лог
    while True:
        try:
                content = driver.find_elements(By.CLASS_NAME, 'IFb1')
                for c in content:
                        l = c.get_attribute("href")
                        if l != None and l.startswith('https://www.fontanka.ru/'):
                            links.add(l)

                diff = links.difference(check) #Проверка на наличие новых новостей
                
                for x in diff:
                    check.add(x)
                    file.write(get_inf(x) + '\n')
                break
        except TimeoutException as _ex:
                break
    driver.quit( )

        
file = open('log.txt', 'w+', encoding="utf-8") #Открытие лог-файла для записи
service = Service(ChromeDriverManager().install()) #Установка драйвера, если ранее не установлен.
#Ввод слов для поиска
words = []
print("Введите количество слов для поиска:")
n= int(input())
print("Введите слова для поиска в статьях:")
for word in range(n):
    word = input()
    words.append(word)

check = set() #Дополнительное множество для проверки новой ссылки
deadline = time.monotonic() + 10800 #Время, на которое запускается временной цикл
while time.monotonic() < deadline:
    search_art()
    time.sleep(600)
file.close() #Лог-файл закрывается
