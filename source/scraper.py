# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 08:00:01 2022
"""
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

def scraper_wine(HTML):
    '''
    Analyses the input string to extract from every wine in it the information 
    referring to the following fields:
        "type","name","year","cellar","region","country","varieties",
        "eco","rating","stars","opinions","likes","parker","penin",
        "suckling","tim_atkin","price","old_price","offer","volume","image".
    All these fields are returned in the pandas dataframe df

    Parameters
    ----------
    HTML : TYPE, string
        DESCRIPTION. HTML code of the page to scrap

    Returns
    -------
    df : TYPE, Pandas data frame
        DESCRIPTION. Data frame with the fields listed above for all the wines
        in the input html file

    '''
    
    # apply beautifoulsoup to the request
    soup = BeautifulSoup(HTML,features="html.parser")
    
    df = pd.DataFrame(columns=["type","name","year","cellar","region","country","varieties",
                               "eco","rating","stars","opinions","likes","parker","penin",
                               "suckling","tim_atkin","price","old_price","offer","volume","image"])
    
    # find the table of contents
    table = soup.find("div", {"class":"list large"})
    
    # find the type of wine of tha page
    type_of_wine = soup.find("h1", {"class":"section-heading line-middle"}).get_text()
    
    # find the images, prices and info tables
    images_table = soup.find_all('div', {"class":"product-image desktop"})
    price_table = table.findAll('div', {'class':'quantity-widget small'})
    info_table = table.findAll('div', {'class':'info'})
    
    # iterate and find each element
    for i in range(len(info_table)):
        
        # find the string that includes name of wine and year
        title_year = info_table[i].find("h2", {'class':'title heading'}).get_text().split('(')[0].rstrip()
        # as sometimes there's no year, try to find year. If there's a year, find it and the wine name
        try:
            year = int(title_year[-4:])
            name = title_year[:-4].rstrip()
        except:
            year = -1
            name = title_year.rstrip()
        # find the name of the productor
        cellar = info_table[i].find("div", {'class':'cellar-name'}).get_text()
        # find the region (first part of string  in div class=region)
        region = info_table[i].find("div", {'class':'region'}).get_text().split("(")[0].rstrip()
        # find the country (second part of string  in div class=region)
        country = info_table[i].find("div", {'class':'region'}).get_text().split("(")[1][:-1]
        # find the grape varieties if exist
        try:
            varieties = info_table[i].find("div", {'class':'tags'}).get_text()
        except:
            varieties = ""
        # check if the wine is ecological, if not, set eco to ''
        try:
            eco = info_table[i].find("p", {'class':'ecological-product'}).get_text()
        except:
            eco = ''
        # find the string that contains the rating and the starts of the wine
        rating_stars = info_table[i].find("div", {'class':'styles_starRatings__B9pGX styles_small__cQ8K1'}).attrs['style']
        # find the rating in the string
        rating = float(re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", rating_stars.split('--')[1])[0])
        # find the stars in the string
        stars = int(re.findall(r'\d+', rating_stars.split('--')[2])[0])
        # find the number of opinions
        opinions = int(re.findall(r'\d+', info_table[i].find("span", {"class":"styles_numOpinions__t_p9L"}).get_text())[0])
        # find the number of likes. As there might be no stars, if there aren't, set to 0
        try:
            likes = int(re.findall(r'\d+', info_table[i].find("div", {"class":"styles_likes__Jvb7B"}).get_text())[0])
        except:
            likes = 0
        # try to find Parker punctuation
        try:
            parker = info_table[i].find("span", {'style':'--score-color:var(--pk);'}).get_text()
        except:
            parker = ""
        # try to find Peñín punctuation
        try:
            penin = info_table[i].find("span", {'style':'--score-color:var(--penin);'}).get_text()
        except:
            penin = ""
        # try to find Suckling punctuation
        try:
            suckling = info_table[i].find("span", {'style':'--score-color:var(--suckling);'}).get_text()
        except:
            suckling = ""
        # try to find Tim Atkin punctuation
        try:
            tim_atkin = info_table[i].find("span", {'style':'--score-color:var(--atkins);'}).get_text()
        except:
            tim_atkin = ""  
        # get the price. As there are many, first check if it's a price with no offer.
        try:
            price = price_table[i].find("p", {'class':'price uniq small'}).get_text()
            offer = False
            previous=""
        # if exception appears, the price has a offer
        except:
            # try to find the old price, if not found, old price to ""
            try:
                previous = price_table[i].find("p", {'class':'price old small'}).get_text()
            except:
                previous = ""
            # try to find the offer price. Could be two types.
            try:
                price = price_table[i].find("p", {'class':'dto small'}).get_text()
            except:
                price = price_table[i].find("p", {'class':'special small'}).get_text()
            # set offer to True as we are in the offer part of the code
            offer = True
        # get not standard bottle volume
        try:
            volume = price_table[i].find("span", {'class':'unit-name small'}).get_text()
        except:
            volume = " / bot. 0,75 L "
        # get image from the images table
        try:
            image = requests.get(images_table[0].find('img')['src']).content 
        except:
            image = ''
        # input data to new row of df
        df.loc[len(df.index)] = [type_of_wine,name,year,cellar,region,country,
                                 varieties,eco,rating,stars,opinions,likes,parker,
                                 penin,suckling,tim_atkin,price,previous,offer,volume,image] 
     
    return df
