# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 08:16:25 2022

@author: jinglaaynes
"""
from scraper import scraper_wine
from crawler import link_crawler
seed_urls = ['https://www.vinissimus.com/es/vinos/rosado',
             'https://www.vinissimus.com/es/vinos/blanco',
             'https://www.vinissimus.com/es/vinos/tinto']

df = link_crawler(seed_urls, scraper_wine, delay=1, num_max=2)