import pandas as pd
import numpy as np
import sys 


if __name__ == "__main__":
	year = sys.argv[1]
	year2 = year[2:]
	int_year = int(year2)
	prev_year = int_year -1

	# reading in file
	input_file = 'original_data/{}-{}/RC{}U.csv'.format(prev_year, year2, year2)
	df = pd.read_csv(input_file)

	# including only schools in the chicago district
	df = df.loc[df["DISTRICT NAME"].str.contains("299") == True]

	pd.set_option('display.float_format', lambda x: '%.3f' % x)


	rm = ["READ", "MATH"]
	gr3 = pd.DataFrame()
	gr4 = pd.DataFrame()
	gr5 = pd.DataFrame()
	gr6 = pd.DataFrame()
	gr7 = pd.DataFrame()
	gr8 = pd.DataFrame()

	dbs = [0, 0, 0, gr3, gr4, gr5, gr6, gr7, gr8]


	merged = pd.DataFrame()

	for i in range(3, 9):
		grade = str(i)
		if i == 3 or i==6 or i==8:
			#do read, write, math
			for subject in rm:
				not_meet = 'DONOTMEET GOALS GR{} {} SCHOOL'.format(grade, subject)
				meet = 'MEET GOALS GR{} {} SCHOOL'.format(grade, subject)
				exceed = 'EXCEED GOALS GR{} {} SCHOOL'.format(grade, subject)

				not_title = '{}-notmeet'.format(subject)
				met_title = '{}-meet'.format(subject)
				ex_title = '{}-exceed'.format(subject)
				
				# populate df, only include schools that teach specific grade of interest
				dbs[i]["SCHOOL ID"] = df["SCHOOL ID R-C-D-S"].loc[df['GRADES IN SCHOOL'].str.contains(grade)==True]
				dbs[i]["School Name"] = df["SCHOOL NAME"].loc[df['GRADES IN SCHOOL'].str.contains(grade)==True]
				dbs[i]["Grade"] = i
				dbs[i]["Year"] = year
				dbs[i][not_title] = df[not_meet].loc[df['GRADES IN SCHOOL'].str.contains(grade)==True]
				dbs[i][met_title] = df[meet].loc[df['GRADES IN SCHOOL'].str.contains(grade)==True]
				dbs[i][ex_title] = df[exceed].loc[df['GRADES IN SCHOOL'].str.contains(grade)==True]


	# merge dfs, sort by school ID and grade 
	dbs_toappend = [dbs[6], dbs[8]]
	merged = dbs[3].append(dbs_toappend)
	merged.sort(columns = ["SCHOOL ID", "Grade"], inplace = True)

	output_file = 'merged_{}.csv'.format(year)
	merged.to_csv(output_file, index=False)





