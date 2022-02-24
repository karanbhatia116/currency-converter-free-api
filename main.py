from bs4 import BeautifulSoup
import requests
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

origins = [
    "*"
]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    from_currency: str
    to_currency: str

@app.get('/')
async def index():
    return "Hello"

@app.post('/convert')
async def convert(item: Item):
    from_currency = item.from_currency
    to_currency = item.to_currency
    url = 'https://www.google.com/search?q=' + from_currency + '+to+' + to_currency + '&oq=' + from_currency + '+to+'+ to_currency + '+&aqs=chrome..69i57j69i59.2472j0j1&sourceid=chrome&ie=UTF-8'
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    conversion_rate = soup.find('div', class_ = 'BNeawe').text[0:6]
    if len(conversion_rate):
        while not conversion_rate[len(conversion_rate) - 1].isdigit():
            conversion_rate = conversion_rate[:-1]
        if(len(conversion_rate) > 0):
            conversion_rate = float(conversion_rate)
        else:
            raise HTTPException(status_code=400, detail="Bad Request")
        obj = {
            from_currency.upper() + '_' + to_currency.upper() : conversion_rate,
        }
        return obj
    else:
        raise HTTPException(status_code=400, detail="Bad Request")


# with open('scrape.html', 'w') as google_page:
#     google_page.write(soup.prettify())