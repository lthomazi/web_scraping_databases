# Data obtained from "https://en.wikipedia.org/wiki/Comparison_of_Linux_distributions"

from dis import dis
import mechanicalsoup
import pandas as pd
import sqlite3
import os

# create a browser object to open any website we'd like
browser = mechanicalsoup.StatefulBrowser()
browser.open("https://en.wikipedia.org/wiki/Comparison_of_Linux_distributions")

# extract table headers (th)
th = browser.page.find_all("th", attrs={"class": "table-rh"})
# only get the text in those tags
distribution = [value.text.replace("\n", "") for value in th]
last_item = distribution.index("Zorin OS") # find the end of the table
distribution = distribution[:(last_item + 1)]

# extract table data (td)
td = browser.page.find_all("td")
columns = [value.text.replace("\n", "") for value in td]
first_item = columns.index("AlmaLinux Foundation")
last_item = columns.index("Binary blobs") # first value in next table
columns = columns[first_item:last_item]


column_names = ["Founder", 
                "Maintainer", 
                "Initial_Release_Year", 
                "Current_Stable_Version", 
                "Security_Updates", 
                "Release_Date", 
                "System_Distribution_Commitment", 
                "Forked_From", 
                "Target_Audience", 
                "Cost", 
                "Status"]

dictionary = {"Distribution": distribution}

# get every 11th item in the table (11 colums per row) 
for i, key in enumerate(column_names):
    dictionary[key] = columns[i:][::11]

df = pd.DataFrame(data = dictionary)

try:
    # insert data into a database
    connection = sqlite3.connect("linux_distro.db")
    cursor = connection.cursor()

    # create table
    cursor.execute("create table linux (Distribution, " + ",".join(column_names) + ")") 
    for i in range(len(df)):
        cursor.execute("insert into linux values (?,?,?,?,?,?,?,?,?,?,?,?)", df.iloc[i])

except:
    os.remove("linux_distro.db")

     # insert data into a database
    connection = sqlite3.connect("linux_distro.db")
    cursor = connection.cursor()

    # create table
    cursor.execute("create table linux (Distribution, " + ",".join(column_names) + ")") 
    for i in range(len(df)):
        cursor.execute("insert into linux values (?,?,?,?,?,?,?,?,?,?,?,?)", df.iloc[i])

connection.commit()



connection.close()