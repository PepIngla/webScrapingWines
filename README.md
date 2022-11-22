# webScrapingWines
Scraper and database to extract the characteristics of the wines sold by Vinissimus in Spain.
## Authors
J. Quadrada Jané and J. Ingla Aynés
## Instructions:
Execute the file main.py with the crawler.py and scraper.py files in the same folder and the generated dataset will be saved at the same folder.
## Fields
Dataset with 1320 wines obtained from scraping the Vinissimus website. The code used to obtain it can be found here: Github.

It contains the following fields:

Type: String, indicates the type of wine. It can take three values “Vino tinto” or red wine, “Vino blanco” or white wine, “Vinos rosados y rosé” or rosé wine because we have restricted our search to these types.

Name: String, contains the name of the wine.

Year: Integer, indicates the crop year. If it was not specified on the website its value in the database is -1.

Cellar: String, wine producer.

Region: String, the region where the wine was produced.

Country: String, the country where the wine was produced.

Varieties: String, grape varieties contained in the wine. If there is no variety specified on the website, we have set it to "".

Eco: String, if the wine has the "eco" label it takes the value "ECO", otherwise, it is nan.

Rating: Float, wine rating according to the vinissimus.com customers.

Stars: Integer, tells us the number of stars of the wine according to the vinissimus.com customers.

Opinions: Integer, number of opinions published on the website about the wine.

Likes: Integer, number of likes by the vinissimus.com customers.

Parker: String, Parker rating. If it is not available, the value is "".

Penin: String, Peñín rating. If it is not available, the value is "".

Suckling: String, Suckling rating.  If it is not available, the value is "".

Tim_atkin: String, Tim Atkin rating.  If it is not available, the value is "".

Price: String, the current price of the wine.

Old_price: String, if the wine is on offer, it indicates the old price.

Offer: Boolean, True if the wine is on offer, False otherwise.

Volume: String, indicates the volume of the bottle. The default value is: “ / bot. 0,75 L “.

Image: bytes, an image of the wine bottle.
