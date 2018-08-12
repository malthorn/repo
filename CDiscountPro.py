from bs4 import BeautifulSoup
import pandas as pd
import math
import requests
import re
import locale
import openpyxl
import time

locale.setlocale(locale.LC_NUMERIC, "")


# Download all product ID's from search page

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

r = requests.get('https://www.cdiscountpro.com/produits/4/c-cm-m-r/champagne.htm', headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')
ProductIDs = soup.find_all("input", id="idProductList")[0]['value']
ProductIDlist = ProductIDs.split(",")
NrProducts = len(ProductIDlist)
NrPages = math.ceil(len(ProductIDlist)/50)
Product = []

Archive = pd.DataFrame(columns=['ProductID','ProductName','ProductDescription','ProductCurrentPrice','ProductOriginalPrice','ProductDiscount','ProductLink','ProductImageLink'])

# Archive = pd.DataFrame(columns=['ProductID','ProductProducer','ProductName','ProductDescription','ProductCurrentPrice','ProductOriginalPrice','ProductDiscount','ProductType','ProductCharacteristics','ProductVintage','ProductColor','ProductContents','ProductAlcoholVolume','ProductGrapes','ProductTastingNotes','ProductFoodSuggestions','ProductLink','ProductImageLink'])


# Download each products in pools of 50 and decipher them

start = 0
end = 50

for x in range(0, NrPages):
   parameter = {'iPageSize': '50', 'idproducts': ProductIDlist[start:end]}
   m = requests.get('https://www.cdiscountpro.com/catalogue/catproductlist4sub.aspx', params=parameter, headers=headers)
   prod = BeautifulSoup(m.text, 'html.parser')
# Divide up each product
   Product = Product + prod.find_all("div", class_="boxcontent")
   len(ProductIDlist[start:end])
   start = start+50
   end = end+50


# Find all information and load into datastructure

for y in range(0, NrProducts):
   # Find ID
      ProductID = Product[y].findAll("input", attrs={"name" : "checkCompare"})
      ProductIDText = ProductID[0]['id']
   # Find Name
      ProductName = Product[y].find_all("span", id=re.compile("lbprd"))
      ProductNameText = ProductName[0].get_text()
   # Find Description
      ProductDescription = Product[y].select(".ShortDescription")
      ProductDescriptionText = ProductDescription[0].get_text()
   # Find Current Price
      ProductCurrentPrice = Product[y].find_all("span", class_="spanSalePriceWithQuantityBreak")
      if not ProductCurrentPrice: ProductCurrentPriceText = '0,00' 
      else: ProductCurrentPriceText = ProductCurrentPrice[0].get_text()
      ProductCurrentPriceValue = re.findall(r'(?:\d+\.)?\d+,\d+', ProductCurrentPriceText)
      ProductCurrentPriceValue = locale.atof(ProductCurrentPriceValue[0])
   # Find Original Price
      ProductOriginalPrice = Product[y].find_all("span", id="PRICEAMOUNT")
      if not ProductOriginalPrice: ProductOriginalPriceText = '0,00' 
      else: ProductOriginalPriceText = ProductOriginalPrice[0].get_text()
      ProductOriginalPriceValue = re.findall(r'(?:\d+\.)?\d+,\d+', ProductOriginalPriceText)
      ProductOriginalPriceValue = locale.atof(ProductOriginalPriceValue[0])
   # Find Discount percentage
      ProductDiscount = Product[y].find_all("span", class_="Amount")
      if not ProductDiscount: ProductDiscountText = ''
      else: ProductDiscountText = ProductDiscount[0].get_text()
   # Find link
      ProductLink = Product[y].find_all("a", href=re.compile("https://www.cdiscountpro.com/"))
      ProductLinkText = ProductLink[0].get('href')
   # Find Image
      ProductImage = Product[y].find_all("img", id=re.compile("prdimg"))
      ProductImageLinkText = ProductImage[0]['src'] 
   # Save to archive
      [int(ProductIDText),ProductNameText,ProductDescriptionText,ProductCurrentPriceValue,ProductOriginalPriceValue,ProductDiscountText,ProductLinkText,ProductImageLinkText]
      Archive.loc[y] = [int(ProductIDText),ProductNameText,ProductDescriptionText,ProductCurrentPriceValue,ProductOriginalPriceValue,ProductDiscountText,ProductLinkText,ProductImageLinkText]
      time.sleep(2)


// Save to csv

Archive.to_excel('CDiscountPro.xlsx', sheet_name='CDiscountPro')





########### 

   ## Get details on product
      n = requests.get(ProductLinkText, headers=headers, allow_redirects=False)
      info = BeautifulSoup(n.text, 'html.parser')
   # Find Producer
      ProductProducer = [t.nextSibling.text for t in info.findAll('td', text = re.compile('Maison :'))]
      if not ProductProducer: ProductProducer = ''
      else: ProductProducer = ProductProducer[0]
   # Find product type and concatenate   
      ProductType = [t.nextSibling.text for t in info.findAll('td', text = re.compile('Type de produit :'))]
      if not ProductType: ProductTypeText = ''
      else: ProductTypeText = ' / '.join(ProductType)
   # Find Color
      ProductColor = [t.nextSibling.text for t in info.findAll('td', text = re.compile('Couleur :'))]
      if not ProductColor: Productcolor = ''
      else: ProductColor = ProductColor[0]
   # Find Year
      ProductVintage = [t.nextSibling.text for t in info.findAll('td', text = re.compile('Millésime :'))]
      if not ProductVintage: ProductVintage = ''
      else: ProductVintage = ProductVintage[0]
   # Find Characteristic
      ProductCharacteristics = [t.nextSibling.text for t in info.findAll('td', text = re.compile('Caractéristiques :'))]
      if not ProductCharacteristics: ProductCharacteristics = ''
      else: ProductCharacteristics = ProductCharacteristics[0]
   # Find Contents 
      ProductContents = [t.nextSibling.text for t in info.findAll('td', text = re.compile('Contenance :'))]
      if not ProductContents: ProductContents = ''
      else: ProductContents = ProductContents[0]
   # Find Alcohol Volume
      ProductAlcoholVolume = [t.nextSibling.text for t in info.findAll('td', text = re.compile("Taux d'alcool :"))]
      if not ProductAlcoholVolume: ProductAlcoholVolume = ''
      else: ProductAlcoholVolume = ProductAlcoholVolume[0]
   # Find Grapes
      ProductGrapes = [t.nextSibling.text for t in info.findAll('td', text = re.compile("Encépagement :"))]
      if not ProductGrapes: ProductGrapes = ''
      else: ProductGrapes = ProductGrapes[0]
   # Find Tasting Notes 
      ProductTastingNotes = [t.nextSibling.text for t in info.findAll('td', text = re.compile("Notes de dégustation :"))]
      if not ProductTastingNotes: ProductTastingNotes = ''
      else: ProductTastingNotes = ' / '.join(ProductTastingNotes)
   # Find Food Suggestions
      ProductFoodSuggestions = [t.nextSibling.text for t in info.findAll('td', text = re.compile("Accords Mets :"))]
      if not ProductFoodSuggestions: ProductFoodSuggestions = ''
      else: ProductFoodSuggestions = ' / '.join(ProductFoodSuggestions)
      [int(ProductIDText),ProductProducer,ProductNameText,ProductDescriptionText,ProductCurrentPriceValue,ProductOriginalPriceValue,ProductDiscountText,ProductTypeText,ProductCharacteristics,ProductVintage,ProductColor,ProductContents,ProductAlcoholVolume,ProductGrapes,ProductTastingNotes,ProductFoodSuggestions,ProductLinkText,ProductImageLinkText] 
   # Save in datastructure
      Archive.loc[y] = [int(ProductIDText),ProductProducer,ProductNameText,ProductDescriptionText,ProductCurrentPriceValue,ProductOriginalPriceValue,ProductDiscountText,ProductTypeText,ProductCharacteristics,ProductVintage,ProductColor,ProductContents,ProductAlcoholVolume,ProductGrapes,ProductTastingNotes,ProductFoodSuggestions,ProductLinkText,ProductImageLinkText]



