# https://docs.agi32.com/PhotometricToolbox/Content/Open_Tool/eulumdat_file_format.htm
# https://docs.agi32.com/AGi32/Content/references/IDH_iesna_standard_file_format.htm

f_org = open("original.ldt", "r")
f_res = open("result.ies", "w")

def num2str(n):									# convert number to string
	s = str(int(n * 10000) / 10000)
	if '.' in s:
		return s.rstrip('0').rstrip('.')
	else:
		return s

company_name = f_org.readline()
ltyp = int(f_org.readline())		# Type indicator
lsym = int(f_org.readline())		# Symmetry indicator
mc = int(f_org.readline())			# Number of C-planes between 0 and 360 degrees (usually 24 for interior, 36 for road lighting luminaires)
dc = float(f_org.readline())		# Distance between C-planes
ng = int(f_org.readline())			# Number of luminous intensities in each C-plane
dg = float(f_org.readline())		# Distance between luminous intensities per C-plane
meas_report = f_org.readline()	# Measurement report number
lum_name = f_org.readline()			# Luminaire name
lum_num = f_org.readline()			# Luminaire number
file_name = f_org.readline()		# File name
date = f_org.readline()					# Date/user
temp = date.find("-")
if temp >= 0:
	user = date[temp + 2 : len(date) - 1]	# User
	date = date[0 : temp - 1] + "\n"			# Date
else:
	user = ""
length_lum = float(f_org.readline())					# Length/diameter of luminaire (mm)
width_lum = float(f_org.readline())						# b - Width of luminaire (mm) (b = 0 for circular luminaire)
height_lum = float(f_org.readline())					# Height of luminaire (mm)
length_lumarea = float(f_org.readline())			# Length of luminaire (mm)
width_lumarea = float(f_org.readline())				# Width of luminous area (mm) (b1 = 0 for circular luminous area of luminaire)
height_lumarea_c0 = float(f_org.readline())		# Height of luminous area C0-plane (mm)
height_lumarea_c90 = float(f_org.readline())	# Height of luminous area C90-plane (mm)
height_lumarea_c180 = float(f_org.readline())	# Height of luminous area C180-plane (mm)
height_lumarea_c270 = float(f_org.readline())	# Height of luminous area C270-plane (mm)
dff = float(f_org.readline())				# DFF - Downward flux fraction (%)
lorl = float(f_org.readline())			# LORL - Light output ratio luminaire (%)
cffli = float(f_org.readline())			# Conversion factor for luminous intensities (depending on measurement)
toldm = float(f_org.readline())			# Tilt of luminaire during measurement (road lighting luminaires)
num_set = int(f_org.readline())			# n - Number of standard sets of lamps
num_lam = int(f_org.readline())			# Number of lamps
type_lam = f_org.readline()					# Type of lamps
tlfl = float(f_org.readline())			# Total luminous flux of lamps (lm)
col_temp = float(f_org.readline())	# Color appearance / color temperature of lamps
col_ren = float(f_org.readline())		# Color rendering group / color rendering index
power = float(f_org.readline())			# Wattage including ballast (W)
dr = []
for i in range(10):							# DR - Direct ratios for room indices k = 0.6 ... 5
	dr.append(float(f_org.readline()))
angle_c = []
for i in range(mc):							# Angles C (beginning with 0 degrees)
	angle_c.append(float(f_org.readline()))
angle_c.append(360)							# Append 360 DEG
angle_g = []
for i in range(ng):							# Angles G (beginning with 0 degrees)
	angle_g.append(float(f_org.readline()))
lum_intensity = []
for i in range(mc):							# Read luminous intensities
	lum_intensity.append([])
	for j in range(ng):
		line = f_org.readline()
		if line == "":
			break
		lum_intensity[i].append(float(line))
	if j < ng - 1:
		lum_intensity.pop()
		break
lum_intensity.append(lum_intensity[0])	# Append luminous intensities for 360 DEG

f_res.write("IESNA:LM-63-2002\n")
f_res.write("[TEST] ")
f_res.write(user + "\n")
f_res.write("[TESTLAB] ")
f_res.write(user + " - Test lab\n")
f_res.write("[MANUFAC] ")
f_res.write(company_name)
f_res.write("[ISSUEDATE] ")
f_res.write(date)
if len(lum_num) > 1:
	f_res.write("[LUMCAT] ")
	f_res.write(lum_num)
if len(lum_name) > 1:
	f_res.write("[LUMINAIRE] ")
	f_res.write(lum_name)
if len(type_lam) > 1:
	f_res.write("[LAMP] ")
	f_res.write(type_lam)
f_res.write("[_SERIALNUMBER] ")
f_res.write(meas_report)
f_res.write("TILT=NONE\n")

if num_lam < 0:
	f_res.write("1 -1 ")
else:
	f_res.write(num2str(num_lam) + " ")
	f_res.write(num2str(tlfl) + " ")	# 
f_res.write(num2str(cffli) + " ")		# multiplier
f_res.write(num2str(ng) + " ")
f_res.write(num2str(mc + 1) + " ")
f_res.write(num2str(1) + " ")		# photometric type
f_res.write(num2str(2) + " ")		# unit type
f_res.write(num2str(width_lumarea / 1000) + " ")
f_res.write(num2str(length_lumarea / 1000) + " ")
f_res.write(num2str(height_lum / 1000) + "\n")

f_res.write("1.0 1.0 ")			# ballast factor, future use
f_res.write(num2str(power))	# input watts
f_res.write("\n")
line = ""
for angle in angle_g:				# vertical angles (maximum 240 characters in line)
	if len(line + num2str(angle)) > 238:
		f_res.write(line + "\n")
		line = " "
	line += num2str(angle) + " "
f_res.write(line + "\n")
line = ""
for angle in angle_c:				# horizontal angles (maximum 240 characters in line)
	if len(line + num2str(angle)) > 238:
		f_res.write(line + "\n")
		line = " "
	line += num2str(angle) + " "
f_res.write(line + "\n")
for intens in lum_intensity:	# Candela values
	line = ""
	for inten in intens:
		it = num2str(inten * float(tlfl) / 1000)
		if len(line + it) > 238:
			f_res.write(line + "\n")
			line = " "
		line += it + " "
	f_res.write(line + "\n")

f_org.close()
f_res.close()
