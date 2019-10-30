# https://docs.agi32.com/PhotometricToolbox/Content/Open_Tool/eulumdat_file_format.htm
# https://docs.agi32.com/AGi32/Content/references/IDH_iesna_standard_file_format.htm

f_ldt = open("original.ldt", "r")
f_ies = open("result.ies", "w")

def num2str(n):									# convert number to string
	s = str(int(n * 10000) / 10000)
	if '.' in s:
		return s.rstrip('0').rstrip('.')
	else:
		return s

company_name = f_ldt.readline()
ltyp = int(f_ldt.readline())		# Type indicator
lsym = int(f_ldt.readline())		# Symmetry indicator
mc = int(f_ldt.readline())			# Number of C-planes between 0 and 360 degrees (usually 24 for interior, 36 for road lighting luminaires)
dc = float(f_ldt.readline())		# Distance between C-planes
ng = int(f_ldt.readline())			# Number of luminous intensities in each C-plane
dg = float(f_ldt.readline())		# Distance between luminous intensities per C-plane
meas_report = f_ldt.readline()	# Measurement report number
lum_name = f_ldt.readline()			# Luminaire name
lum_num = f_ldt.readline()			# Luminaire number
file_name = f_ldt.readline()		# File name
date = f_ldt.readline()					# Date/user
temp = date.find("-")
if temp >= 0:
	user = date[temp + 2 : len(date) - 1]	# User
	date = date[0 : temp - 1] + "\n"			# Date
else:
	user = ""
length_lum = float(f_ldt.readline())					# Length/diameter of luminaire (mm)
width_lum = float(f_ldt.readline())						# b - Width of luminaire (mm) (b = 0 for circular luminaire)
height_lum = float(f_ldt.readline())					# Height of luminaire (mm)
length_lumarea = float(f_ldt.readline())			# Length of luminaire (mm)
width_lumarea = float(f_ldt.readline())				# Width of luminous area (mm) (b1 = 0 for circular luminous area of luminaire)
height_lumarea_c0 = float(f_ldt.readline())		# Height of luminous area C0-plane (mm)
height_lumarea_c90 = float(f_ldt.readline())	# Height of luminous area C90-plane (mm)
height_lumarea_c180 = float(f_ldt.readline())	# Height of luminous area C180-plane (mm)
height_lumarea_c270 = float(f_ldt.readline())	# Height of luminous area C270-plane (mm)
dff = float(f_ldt.readline())				# DFF - Downward flux fraction (%)
lorl = float(f_ldt.readline())			# LORL - Light output ratio luminaire (%)
cffli = float(f_ldt.readline())			# Conversion factor for luminous intensities (depending on measurement)
toldm = float(f_ldt.readline())			# Tilt of luminaire during measurement (road lighting luminaires)
num_set = int(f_ldt.readline())			# n - Number of standard sets of lamps
num_lam = int(f_ldt.readline())			# Number of lamps
type_lam = f_ldt.readline()					# Type of lamps
tlfl = float(f_ldt.readline())			# Total luminous flux of lamps (lm)
col_temp = float(f_ldt.readline())	# Color appearance / color temperature of lamps
col_ren = float(f_ldt.readline())		# Color rendering group / color rendering index
power = float(f_ldt.readline())			# Wattage including ballast (W)
dr = []
for i in range(10):							# DR - Direct ratios for room indices k = 0.6 ... 5
	dr.append(float(f_ldt.readline()))
angle_c = []
for i in range(mc):							# Angles C (beginning with 0 degrees)
	angle_c.append(float(f_ldt.readline()))
angle_c.append(360)							# Append 360 DEG
angle_g = []
for i in range(ng):							# Angles G (beginning with 0 degrees)
	angle_g.append(float(f_ldt.readline()))
lum_intensity = []
for i in range(mc):							# Read luminous intensities
	lum_intensity.append([])
	for j in range(ng):
		line = f_ldt.readline()
		if line == "":
			break
		lum_intensity[i].append(float(line))
	if j < ng - 1:
		lum_intensity.pop()
		break
lum_intensity.append(lum_intensity[0])	# Append luminous intensities for 360 DEG

f_ies.write("IESNA:LM-63-2002\n")
f_ies.write("[TEST] ")
f_ies.write(user + "\n")
f_ies.write("[TESTLAB] ")
f_ies.write(user + " - Test lab\n")
f_ies.write("[MANUFAC] ")
f_ies.write(company_name)
f_ies.write("[ISSUEDATE] ")
f_ies.write(date)
if len(lum_num) > 1:
	f_ies.write("[LUMCAT] ")
	f_ies.write(lum_num)
if len(lum_name) > 1:
	f_ies.write("[LUMINAIRE] ")
	f_ies.write(lum_name)
if len(type_lam) > 1:
	f_ies.write("[LAMP] ")
	f_ies.write(type_lam)
f_ies.write("[_SERIALNUMBER] ")
f_ies.write(meas_report)
f_ies.write("TILT=NONE\n")

if num_lam < 0:
	f_ies.write("1 -1 ")
else:
	f_ies.write(num2str(num_lam) + " ")
	f_ies.write(num2str(tlfl) + " ")	# 
f_ies.write(num2str(cffli) + " ")		# multiplier
f_ies.write(num2str(ng) + " ")
f_ies.write(num2str(mc + 1) + " ")
f_ies.write(num2str(1) + " ")		# photometric type
f_ies.write(num2str(2) + " ")		# unit type
f_ies.write(num2str(width_lumarea / 1000) + " ")
f_ies.write(num2str(length_lumarea / 1000) + " ")
f_ies.write(num2str(height_lum / 1000) + "\n")

f_ies.write("1.0 1.0 ")			# ballast factor, future use
f_ies.write(num2str(power))	# input watts
f_ies.write("\n")
line = ""
for angle in angle_g:				# vertical angles (maximum 240 characters in line)
	if len(line + num2str(angle)) > 238:
		f_ies.write(line + "\n")
		line = " "
	line += num2str(angle) + " "
f_ies.write(line + "\n")
line = ""
for angle in angle_c:				# horizontal angles (maximum 240 characters in line)
	if len(line + num2str(angle)) > 238:
		f_ies.write(line + "\n")
		line = " "
	line += num2str(angle) + " "
f_ies.write(line + "\n")
for intens in lum_intensity:	# Candela values
	line = ""
	for inten in intens:
		it = num2str(inten * float(tlfl) / 1000)
		if len(line + it) > 238:
			f_ies.write(line + "\n")
			line = " "
		line += it + " "
	f_ies.write(line + "\n")

f_ldt.close()
f_ies.close()
