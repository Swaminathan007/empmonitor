import csv
f = open("Adidas US Sales Datasets.csv","r")
r = csv.reader(f)
r = list(r)
print(r[1])