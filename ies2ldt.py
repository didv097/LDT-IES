
f_ies = open("original.ies", "r")
f_ldt = open("result.ldt", "w")

def num2str(n):
	return "{:g}".format(n)

f_ies.readline()
while True:
	line = f_ies.readline()
	if line[0] == '[':
		cls_index = line.index(']')
		keyword = line[1 : cls_index]
		if keyword == "TEST":
			test = line[cls_index + 2 : -1]
		elif keyword == "MANUFAC":
			manufac = line[cls_index + 2 : -1]
		elif keyword == "ISSUEDATE":
			issue_date = line[cls_index + 2 : -1]
		elif keyword == "LUMINAIRE":
			luminaire = line[cls_index + 2 : -1]
		elif keyword == "_SERIALNUMBER":
			serial_number = line[cls_index + 2 : -1]
		continue
	if line[0:4] == "TILT":
		break

f_ies.close()
f_ldt.close()