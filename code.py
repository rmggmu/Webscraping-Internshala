import requests
from bs4 import BeautifulSoup
import pandas as pd
#importing libraries

#requesting for link
r = requests.get("https://internshala.com/internships/work-from-home-computer%20science-jobs")
c = r.content
soup = BeautifulSoup(c, "html.parser")
#defining list which will store the dictionaries
l=[]
#finding next page reference
dat=soup.find_all("a",{"id":"navigation-forward"})
href=dat[0].get("href")

#if next page reference is valid the true
while(href!='#'):
    all_data = soup.find_all("div",{"class":"container-fluid individual_internship "})
    for j in all_data:
        d={}
        find_title=j.find_all("h4")[0].text
        find_loc=j.find_all("a",{"class":"location_link"})[0].text
        find_com=j.find_all("h4")[1].text
        find_detai=j.find_all("table",{"class":"table"})
        d["Title"]=find_title.rstrip().lstrip()
        d["Location"]=find_loc.rstrip().lstrip()
        leng=len(find_com)-1
        d["Company"]=find_com[0:leng].rstrip().lstrip()

        d["Start Date:"]=(find_detai[0].find_all("td")[0].text).rstrip().lstrip()
        d["Duration"] = (find_detai[0].find_all("td")[1].text).rstrip().lstrip()
        d["Salary"] = (find_detai[0].find_all("td")[2].text).rstrip().lstrip()
        d["Posted on"] = (find_detai[0].find_all("td")[3].text).rstrip().lstrip()
        d["Last Date"] = (find_detai[0].find_all("td")[4].text).rstrip().lstrip()
        l.append(d)

    r = requests.get("https://internshala.com"+href)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    dat = soup.find_all("a", {"id": "navigation-forward"})
    href = dat[0].get("href")

#creating output files
df=pd.DataFrame(l)
df.to_json("Result.json")
df.to_csv("Res.csv")

