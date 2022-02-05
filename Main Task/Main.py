import csv
import time
from numpy import product
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Column, String, create_engine,ForeignKey

username = "abhishek"
password = "Abhi123"
db_name = "abhi"

con = f"mysql+pymysql://{username}:{password}@localhost:3306/{db_name}"


engine=create_engine(con,echo=True)
Session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
Base = declarative_base()

Base.metadata.create_all(engine)

session=Session(bind=engine) 
print("connected")


class Book(Base):
    __tablename__ = 'book'
    __table_args__ = {'extend_existing': True}

    book_id = Column(Integer, primary_key=True)
    url = Column(String(100))
    title = Column(String(100))
    imageLink = Column(String(100))
    price = Column(String(10))

class Product_Details(Base):
    __tablename__ = 'product'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    publisher = Column(String(100))
    language = Column(String(50))
    ISBN_10 = Column(String(50))
    ISBN_13 = Column(String(50))

Base.metadata.create_all(engine)

def convert(text):
    blob=TextBlob(text)
    text=str(blob.translate(to="EN"))
    return text

list = []
all = {}
all_data={}
count = 0

with open('a.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for line in csv_reader:
        asin = line[' Asin      ']
        country = line[' country']
        url = f"https://www.amazon.{country.strip()}/dp/{asin.strip()}"

        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64;rv:84.0) Gecko/20100101',
                'Accept-Language': 'en-GB,en;q=0.5',
                'Referer': 'https://google.com',
                'DNT':'1',
            }

        if count==0:
            with open("data.json", "w") as final:
                json.dump([], final)

        count = count+1

        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        if page:
            try:
                list = []
                all = {}
                all_data={}

                print("URL [", count, "] : ", url)
                title = soup.find('span', id='productTitle').text.strip()
                print("Title [", count, "] : ", title)
                all["Title"]=title

                image = soup.find('img', id='imgBlkFront')
                img=image.attrs.get('src')
                print("Image [", count, "] : ",img)
                all["Image Link"]=img

                price=soup.find('a',class_="a-size-mini a-link-normal").text.strip()

                price=price.split(" ")
                price=str(price[len(price)-1])+str(price[len(price)-2])
                price=price.replace("from","")
                print("Price [", count, "] : ",price)
                all["Price"]=price

                # Adding book deatils in database
                book = Book(url=url, title=title, imageLink=img, price=price)
                session.add(book)
                session.commit()

                detail=soup.find_all('span',class_='a-list-item')
                
                details={}

                detail=detail[6:11]

                l=[]
 
                for item in detail:
                    i=item.find('span',class_='a-text-bold').text
                    sub=i.strip()
                    sub=sub.replace("\n", "")
                    sub=sub.replace("\u200f", "")
                    sub=sub.replace(" ","")
                    sub=sub.replace("\u200e","")
                    sub=sub.replace("\u00c9","")
                    sub=sub.replace("\u00e7","")
                    sub=sub.replace(":","")

                    j=item.find('span',class_='').text.strip()

                    l.append(j)

                    details[sub]=j

                product_info = Product_Details(publisher=l[0], language=l[1], ISBN_10=details.get("ISBN-10"), ISBN_13 = details.get("ISBN-13"))
                session.add(product_info)
                session.commit()

                all["Product Details"]=details

                
                all_data[url]=all

                print(all_data)

                with open("data.json", "r") as file:
                    list = json.load(file)

                list.append(all_data)

                with open("data.json", "w") as final:
                    json.dump(list, final)

            except:
                # print("Connection refused by the server..")
                # print("Let me sleep for 5 seconds")
                # print("ZZzzzz...")
                time.sleep(5)
                
                all_data[url]=all
                if all:
                    print(all_data)
                    with open("data1.json", "r",encoding='utf-8') as file:
                        list = json.load(file)

                    list.append(all_data)

                    with open("data1.json", "w",encoding='utf-8') as final:
                        json.dump(list, final)

                continue
