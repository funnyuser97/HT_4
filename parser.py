import re,os,csv

INPUT_FILE = "openerp-server.log"
ALL_DATA = "./reports/all_data.csv"
UNIQUE = "./reports/unique.csv"

pattern_error = r".+ERROR.+"
pattern_warning = r".+WARNING.+"
pattern_critical = r".+CRITICAL.+"

pattern_date = r"^.{19}"
pattern_marker = r"[E|W|C][A-Z]{4,7}"
pattern_description = r"[E|W|C][A-Z]{4,7}.*$"

def main():
	try:
	    os.makedirs('reports')
	except OSError:
	    pass

	inputfile = open(INPUT_FILE, mode='r',encoding='utf-8')
	mytext = inputfile.read()
	inputfile.close()

	records_error = re.findall(pattern_error,mytext)
	records_warning = re.findall(pattern_warning,mytext)
	records_critical = re.findall(pattern_critical,mytext)

	count_error = len(records_error)
	count_warning = len(records_warning)
	count_critical = len(records_critical)

	print('ERROR:'+str(len(records_error)))
	print('WARNING:'+str(len(records_warning)))
	print('CRITICAL:'+str(len(records_critical)))
	print('Total:'+str(len(records_critical)+len(records_warning)+len(records_error)))

	inf_error = parser(count_error,0,records_error)
	inf_warning = parser(count_warning,count_error,records_warning)
	inf_critical = parser(count_critical,count_error+count_warning,records_critical)

	file_write(ALL_DATA,"id_line",inf_error,inf_warning,inf_critical)

	uni_error = uni(inf_error)
	uni_warning = uni(inf_warning)
	uni_critical = uni(inf_critical)

	print('Unique error:'+str(len(uni_error)))
	print('Unique warning:'+str(len(uni_warning)))
	print('Unique critical:'+str(len(uni_critical)))
	print('Total unique:'+str(len(uni_error)+len(uni_warning)+len(uni_critical)))

	file_write(UNIQUE,"count",uni_error,uni_warning,uni_critical)
	return;

def parser(count,plus,records):
	info = []
	records_date = []
	records_marker = []
	records_description = []

	for i in range(count):
		tmp1 = re.findall(pattern_date,records[i])
		tmp2 = re.findall(pattern_marker,records[i])
		tmp3 = re.findall(pattern_description,records[i])
		records_date.append(tmp1[0])
		records_marker.append(tmp2[0])
		records_description.append(tmp3[0].replace(tmp2[0],''))
		mydict={"id_line":i+plus,"marker":records_marker[i],"date":records_date[i],"description":records_description[i]}
		info.append(mydict)
	return info

def uni(list_of_dict):
	new=[]
	count = 1
	plus = 0
	for t_dict in list_of_dict:
		for n_dict in new:
			if (n_dict.get("description")==t_dict.get("description")):
				n_dict["count"]=n_dict.get("count")+1
				plus=1
		if plus!=1:
			mydict={"count":count,"marker":t_dict.get("marker"),"date":t_dict.get("date"),"description":t_dict.get("description")}
			new.append(mydict)
		else: plus=0
	return new

def file_write(name_file,first_col,inf_error,inf_warning,inf_critical):
	with open(name_file, "w", newline="") as file:
	    columns = [first_col,"marker", "date", "description"]
	    writer = csv.DictWriter(file, fieldnames=columns)
	    writer.writeheader()
	     
	    writer.writerows(inf_error)
	    writer.writerows(inf_warning) 	
	    writer.writerows(inf_critical) 	
	return;

main()