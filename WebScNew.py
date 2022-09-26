from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#creating my CSV file to store the return of the scrape
filename = "neweggs_gpus.csv"
f = open(filename, "w")

headers = "brand, product_name, rating, current_price\n"

f.write(headers)

#simple loop to be able to iterate through all pages of the results
for page in range(1,100):
    my_url = f'https://www.newegg.com/p/pl?d=graphics+cards&page={page}'
    #opening the conection and saving the page locally.
    uclient = uReq(my_url)
    page_html = uclient.read()
    uclient.close()

    #html parsing
    page_soup = soup(page_html, "html.parser")

    #grabs each product (graphics card listing)
    containers = page_soup.findAll("div",{"class":"item-container"})



    #Creating a for loop to loop through each product and grap the items I want
    for container in containers:
        spon_con = container.findAll("div", {"class":"item-sponsored-box"})
        if len(spon_con) <= 0:
            brand_container = container.find_all("a",{"class":"item-brand"})
            if len(brand_container) > 0:
                brand_name = brand_container[0].img["title"]

            title_container = container.findAll("a", {"class":"item-title"})
            product_name = title_container[0].text

            current_price_con = container.findAll("li",{"class":"price-current"})
            try:
                decimal_price = current_price_con[0].sup.text
            except AttributeError:
                decimal_price = '0'
            try:
                whole_price = current_price_con[0].strong.text
            except AttributeError:
                whole_price = '0'
            try:
                rating_container = container.findAll("a",{"class":"item-rating"})
                rating = rating_container[0].i["aria-label"]
            except IndexError:
                continue
        
            f.write(brand_name + "," + product_name.replace(",","|") + "," + str(rating) + "," + str(whole_price) + str(decimal_price) + "\n")
#finally just want to close the file that was created
f.close()