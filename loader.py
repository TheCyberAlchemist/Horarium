import csv
with open('egg.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in spamreader:
	   # print(", ".join(row))
	   # line = list(row)
	   row = row[0].split(",")
	   print(row)
    # for line in csvfile:
	   #  line = parse line to a list
	   