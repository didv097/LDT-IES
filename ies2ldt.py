# https://docs.agi32.com/PhotometricToolbox/Content/Open_Tool/eulumdat_file_format.htm
# https://docs.agi32.com/AGi32/Content/references/IDH_iesna_standard_file_format.htm

f_org = open("original.ies", "r")
f_res = open("result.ldt", "w")

def num2str(n):									# convert number to string
	s = str(int(n * 10000) / 10000)
	if '.' in s:
		return s.rstrip('0').rstrip('.')
	else:
		return s

test = ""
manufac = ""
issue_date = ""
luminaire = ""
lum_num = ""
serial_number = ""
type_lamp = ""

f_org.readline()
while True:
	line = f_org.readline()
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

line = f_org.readline()
items = line.split()
cnt_lamps = int(items[0])				# number of lamps
lumens = int(items[1])					# lumens/lamp
multiplier = int(items[2])			# multiplier
cnt_ver_angles = int(items[3])	# number of vertical angles
cnt_hor_angles = int(items[4])	# number of horizontal angles
phot_type = int(items[5])				# photometric type
unit_type = int(items[6])				# units type
width = float(items[7])					# width
length = float(items[8])				# length
height = float(items[9])				# height

line = f_org.readline()
items = line.split()
bal_fac = float(items[0])				# ballast factor
fut_use = float(items[1])				# future use
input_watts = float(items[2])		# input watts

line = f_org.readline()
ver_angles = [float(i) for i in line.split()]	# vertical angles
while True:
	line = f_org.readline()
	if line[0] != ' ':
		break
	ver_angles += [float(i) for i in line.split()]

hor_angles = [float(i) for i in line.split()]	# horizontal angles
while True:
	line = f_org.readline()
	if line[0] != ' ':
		break
	hor_angles += [float(i) for i in line.split()]
hor_angles.pop()															# Remove 360 deg from horizontal angles

angles = []
for i in range(cnt_hor_angles):								# candela values
	angles.append([float(j) for j in line.split()])
	while True:
		line = f_org.readline()
		if line == "" or line[0] != ' ':
			break
		angles[i] += [float(j) for j in line.split()]

f_res.write(manufac + "\n")												# Company
f_res.write("2\n0\n")															# Ityp, Isym
f_res.write(num2str(cnt_hor_angles - 1) + "\n")		# Mc - Remove 360 deg
f_res.write(num2str(hor_angles[1] - hor_angles[0]) + "\n")	# Dc
f_res.write(num2str(cnt_ver_angles) + "\n")				# Ng
f_res.write(num2str(ver_angles[1] - ver_angles[0]) + "\n")	# Dg
f_res.write(serial_number + "\n")									# Measurement report number
f_res.write(luminaire + "\n")											# Luminaire name
f_res.write(lum_num + "\n")												# Luminaire number
f_res.write("result.ldt\n")												# File name
f_res.write(issue_date + " - " + test + "\n")			# Date/user
f_res.write(num2str(length * 1000) + "\n")				# Length/diameter of luminaire (mm)
f_res.write(num2str(width * 1000) + "\n")					# b - Width of luminaire (mm) (b = 0 for circular luminaire)
f_res.write(num2str(height * 1000) + "\n")				# Height of luminaire (mm)
f_res.write(num2str(length * 1000) + "\n")				# Length/diameter of luminous area (mm)
f_res.write(num2str(width * 1000) + "\n")					# b1 - Width of luminous area (mm) (b1 = 0 for circular luminous area of luminaire)
f_res.write("0\n0\n0\n0\n")												# Height of luminous area C-planes (mm)
f_res.write("100\n100\n")													# DFF, LORL
f_res.write(num2str(multiplier) + "\n")						# Conversion factor for luminous intensities (depending on measurement)
f_res.write("0\n1\n")															# Tilt of luminaire during measurement, Number of standard sets of lamps
f_res.write(num2str(cnt_lamps) + "\n")						# Number of lamps
f_res.write(type_lamp + "\n")											# Type of lamps
f_res.write(num2str(lumens) + "\n")								# Total luminous flux of lamps (lm)
f_res.write("\n\n")																# Color appearance, Color rendering group
f_res.write(num2str(input_watts) + "\n")					# Wattage including ballast (W)
for i in range(10):																# DR - Direct ratios for room indices
	f_res.write("1\n")
for i in range(len(hor_angles)):									# Angles C (beginning with 0 degrees)
	f_res.write(num2str(hor_angles[i]) + "\n")
for i in range(len(ver_angles)):									# Angles G (beginning with 0 degrees)
	f_res.write(num2str(ver_angles[i]) + "\n")
for i in range(len(angles)):											# Luminous intensity distribution (cd/1000 lumens)
	for j in range(len(angles[i])):
		f_res.write(num2str(angles[i][j] / lumens * 1000) + "\n")

f_org.close()
f_res.close()
