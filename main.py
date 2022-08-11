import requests
from bs4 import BeautifulSoup
import pandas as pd
from xlsxwriter import Workbook

# Parse possible nutritional elements and ask to choose
with requests.get(url="https://www.nutritionvalue.org/",
                  headers={"Accept-Language": "lt-LT,lt;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6,pl;q=0.5",
                           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                                         "Chrome/103.0.0.0 Safari/537.36"}
                  ) as r:
    main = r.text

s_main = BeautifulSoup(main, "html.parser")

elements = s_main.find_all(class_="l", name="a")
elements_list_not_clean = [element.getText()for element in elements]
elements_list = elements_list_not_clean[:-52]

elements_links = [f'https://www.nutritionvalue.org{element.get("href")}' for element in elements]
chosen_element = input(f"Enter nutritional element from the list: \n{elements_list}\n")
spec_link = elements_links[elements_list.index(chosen_element)]

# Parse page of selected nutritional element
response = requests.get(url=spec_link,
                        headers={"Accept-Language":"lt-LT,lt;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6,pl;q=0.5",
                                                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                                                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                                 "Chrome/103.0.0.0 Safari/537.36"})
page = response.text

soup = BeautifulSoup(page, "html.parser")

foods = soup.find_all(class_="table_item_name")
quantity = soup.find_all(name="td", class_="right")

# Generate food, quantity and links lists from html
foods_list = [food.get("title") for food in foods]
links_list = [f'https://www.nutritionvalue.org{link.get("href")}' for link in foods]
number_list = [int(float(numb.getText().split()[0])) for numb in quantity]

# Generate excel from lists
dict = {'quant': number_list, 'food': foods_list, 'links': links_list}
df = pd.DataFrame(dict)
df.columns = ['Quantity (mg.)', 'Food', 'More info']

writer = pd.ExcelWriter(f"{chosen_element}.xlsx", engine='xlsxwriter')
df.to_excel(writer,sheet_name=f"{chosen_element}", index=False)
writer.save()

# Message after generating excel file
print(f"Excel file generated: there you will find the list of foods that have most {chosen_element}.")