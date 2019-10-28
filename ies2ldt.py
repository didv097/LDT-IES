f_ies = open("original.ies", "r")
f_ldt = open("result.ldt", "w")

def num2str(n):
	return "{:g}".format(n)

test = ""
manufac = ""
issue_date = ""
luminaire = ""
lum_num = ""
serial_number = ""
type_lamp = ""

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
		elif keyword == "LUMCAT":
			lum_num = line[cls_index + 2 : -1]
		elif keyword == "LAMP":
			type_lamp = line[cls_index + 2 : -1]
		elif keyword == "_SERIALNUMBER":
			serial_number = line[cls_index + 2 : -1]
		continue
	if line[0:4] == "TILT":
		break

line = f_ies.readline()
items = line.split()
cnt_lamps = int(items[0])
lumens = int(items[1])
multiplier = int(items[2])
cnt_ver_angles = int(items[3])
cnt_hor_angles = int(items[4])
phot_type = int(items[5])
unit_type = int(items[6])
width = float(items[7])
length = float(items[8])
height = float(items[9])

line = f_ies.readline()
items = line.split()
bal_fac = float(items[0])
fut_use = float(items[1])
input_watts = float(items[2])

line = f_ies.readline()
ver_angles = [float(i) for i in line.split()]
while True:
	line = f_ies.readline()
	if line[0] != ' ':
		break
	ver_angles += [float(i) for i in line.split()]

hor_angles = [float(i) for i in line.split()]
while True:
	line = f_ies.readline()
	if line[0] != ' ':
		break
	hor_angles += [float(i) for i in line.split()]
hor_angles.pop()																	# Remove 360 deg

angles = []
for i in range(cnt_hor_angles):
	angles.append([float(j) for j in line.split()])
	while True:
		line = f_ies.readline()
		if line == "" or line[0] != ' ':
			break
		angles[i] += [float(j) for j in line.split()]

f_ldt.write(manufac + "\n")
f_ldt.write("2\n0\n")
f_ldt.write(num2str(cnt_hor_angles - 1) + "\n")			# Remove 360 deg
f_ldt.write(num2str(hor_angles[1] - hor_angles[0]) + "\n")
f_ldt.write(num2str(cnt_ver_angles) + "\n")
f_ldt.write(num2str(ver_angles[1] - ver_angles[0]) + "\n")
f_ldt.write(serial_number + "\n")
f_ldt.write(luminaire + "\n")
f_ldt.write(lum_num + "\n")		# luminaire number
f_ldt.write("result.ldt\n")
f_ldt.write(issue_date + " - " + test + "\n")				# ? "date - test_string"
f_ldt.write(num2str(length * 1000) + "\n")
f_ldt.write(num2str(width * 1000) + "\n")
f_ldt.write(num2str(height * 1000) + "\n")
f_ldt.write(num2str(length * 1000) + "\n")
f_ldt.write(num2str(width * 1000) + "\n")
f_ldt.write("0\n0\n0\n0\n")
f_ldt.write("100\n100\n")
f_ldt.write(num2str(multiplier) + "\n")
f_ldt.write("0\n1\n")
f_ldt.write(num2str(cnt_lamps) + "\n")
f_ldt.write(type_lamp + "\n")		# type of lamps
f_ldt.write(num2str(lumens) + "\n")
f_ldt.write("\n\n")		# 
f_ldt.write(num2str(input_watts) + "\n")
for i in range(10):
	f_ldt.write("1\n")
for i in range(len(hor_angles)):
	f_ldt.write(num2str(hor_angles[i]) + "\n")
for i in range(len(ver_angles)):
	f_ldt.write(num2str(ver_angles[i]) + "\n")
for i in range(len(angles)):
	for j in range(len(angles[i])):
		f_ldt.write(num2str(angles[i][j] / lumens * 1000) + "\n")

f_ies.close()
f_ldt.close()
