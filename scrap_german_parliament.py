from bs4 import BeautifulSoup
import requests
import json
import time
import random

member_name_list=[]

for i in range(0,735,20):
    url=(f'https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=20&noFilterSet=true&offset={i}')
    #print(url)

    q=requests.get(url) # getting the urls
    result=q.content

    scrapper: BeautifulSoup=BeautifulSoup(result,'lxml')  #passing the contents

    all_members=scrapper.select(".bt-slide-content a")
    for member in all_members:
        member_url=member.get("href")   # getting all the urls using the get method
        member_name_list.append(member_url)
        #print(member_url)

with open('member_name_list.txt','a') as file: # saving the urls to a txt file
    for line in member_name_list:
        file.write(f'{line}\n')

with open("member_name_list.txt") as file:  # saving the urls in a new list

    lines=[line.strip() for line in file.readlines()]

    data_dict=[]
    count=0 # creating a counter to make the terminal process more appealing

    for line in lines:
        q=requests.get(line) # requesting the data from the new list
        result=q.content

        scrapper=BeautifulSoup(result,'lxml')
        person=scrapper.find(class_="bt-biografie-name").find("h3").text # creating a new object from soup , using find method , getting the h3 components
        person_political_party=person.strip().split(',')  # seperating to 2 elements
        person_name=person_political_party[0] # with 0 index, getting the name
        person_party=person_political_party[1].strip() # with index: 1 , getting the political party

        social_networks=scrapper.find_all(class_='bt-link-extern')

        social_networks_urls=[] # new list for the social sites

        for link in social_networks:
             social_networks_urls.append(link.get("href"))  # adding the urls

        data={
            'person name':person_name,
            'person political party':person_party, # keys
            'social contacts':social_networks_urls
        }
        count+=1
        time.sleep(random.randrange(2, 4)) # avoiding site's attempt, : <makes it considerably slower>
        print(f"{count}: {line} is done!") # console friendly

        data_dict.append(data)

        with open('data.json', 'w',encoding='utf-8') as json_file:
            json.dump(data_dict,json_file,indent=4,ensure_ascii=False)

