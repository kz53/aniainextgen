import csv
import ast

# use python csvhelper.py to create csv file

infile = "anime.csv"
outfile = "animelite.csv"

with open(infile, encoding='utf-8') as f, open(outfile, 'w') as o:
	reader = csv.reader(f)
	writer = csv.writer(o, delimiter=',') # adjust as necessary
	animeids = set()
	for row in reader:
		if row[0] != "anime_id":
			row0 = row[0]
			if row0 not in animeids:
				animeids.add(row0)
				writer.writerow(row)
		else:
			writer.writerow(row)