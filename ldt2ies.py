
f_ldt = open("original.ldt", "r")

def num2str(n):
	return "{:g}".format(n)

company_name = f_ldt.readline()
ltyp = int(f_ldt.readline())	# Type indicator
lsym = int(f_ldt.readline())	# Symmetry indicator
mc = int(f_ldt.readline())		# Number of C-planes between 0 and 360 degrees (usually 24 for interior, 36 for road lighting luminaires)
dc = float(f_ldt.readline())	# Distance between C-planes
ng = int(f_ldt.readline())		# Number of luminous intensities in each C-plane
dg = float(f_ldt.readline())		# Distance between luminous intensities per C-plane
meas_report = f_ldt.readline()	# Measurement report number
lum_name = f_ldt.readline()			# Luminaire name
lum_num = f_ldt.readline()			# Luminaire number
file_name = f_ldt.readline()		# File name
date = f_ldt.readline()					# Date/user
temp = date.index("-")
user = date[temp + 2 : len(date)]
date = date[0 : temp - 1]
length_lum = float(f_ldt.readline())		# Length/diameter of luminaire (mm)
width_lum = float(f_ldt.readline())		# b - Width of luminaire (mm) (b = 0 for circular luminaire)
height_lum = float(f_ldt.readline())		# Height of luminaire (mm)
length_lumarea = float(f_ldt.readline())				# Length of luminaire (mm)
width_lumarea = float(f_ldt.readline())				# Width of luminous area (mm) (b1 = 0 for circular luminous area of luminaire)
height_lumarea_c0 = float(f_ldt.readline())		# Height of luminous area C0-plane (mm)
height_lumarea_c90 = float(f_ldt.readline())		# Height of luminous area C90-plane (mm)
height_lumarea_c180 = float(f_ldt.readline())	# Height of luminous area C180-plane (mm)
height_lumarea_c270 = float(f_ldt.readline())	# Height of luminous area C270-plane (mm)
dff = float(f_ldt.readline())		# DFF - Downward flux fraction (%)
lorl = float(f_ldt.readline())		# LORL - Light output ratio luminaire (%)
cffli = float(f_ldt.readline())	# Conversion factor for luminous intensities (depending on measurement)
toldm = float(f_ldt.readline())	# Tilt of luminaire during measurement (road lighting luminaires)
num_set = int(f_ldt.readline())		# n - Number of standard sets of lamps
num_lam = int(f_ldt.readline())		# Number of lamps
type_lam = (f_ldt.readline())		# Type of lamps
tlfl = int(f_ldt.readline())				# Total luminous flux of lamps (lm)
col_temp = float(f_ldt.readline())		# Color appearance / color temperature of lamps
col_ren = float(f_ldt.readline())		# Color rendering group / color rendering index
power = float(f_ldt.readline())			# Wattage including ballast (W)
dr = []
for i in range(0, 10):		# DR - Direct ratios for room indices k = 0.6 ... 5
	dr.append(float(f_ldt.readline()))
angle_c = []
for i in range(0, mc):		# Angles C (beginning with 0 degrees)
	angle_c.append(float(f_ldt.readline()))
angle_g = []
for i in range(0, ng):		# Angles G (beginning with 0 degrees)
	angle_g.append(float(f_ldt.readline()))
lum_intensity = []
for i in range(0, mc):
	lum_intensity.append([])
	for j in range(0, ng):
		lum_intensity[i].append(float(f_ldt.readline()))


f_ies = open("result.ies", "w")

f_ies.write("IESNA:LM-63-2002\n")
f_ies.write("[TEST] ")
f_ies.write(user)
f_ies.write("[TESTLAB] ")
f_ies.write(user)
f_ies.write("[MANUFAC] ")
f_ies.write(company_name)
f_ies.write("[ISSUEDATE] ")
f_ies.write(date)
f_ies.write("\n[LUMINAIRE] ")
f_ies.write(lum_name)
f_ies.write("[_SERIALNUMBER] ")
f_ies.write(meas_report)
f_ies.write("TILT=NONE\n")

f_ies.write(num2str(num_lam) + " ")
f_ies.write(num2str(tlfl) + " ")
f_ies.write(num2str(1) + " ")		# ? multiplier
f_ies.write(num2str(ng) + " ")
f_ies.write(num2str(mc) + " ")
f_ies.write(num2str(1) + " ")		# ? photometric type
f_ies.write(num2str(2) + " ")		# ? unit type
f_ies.write(num2str(width_lum / 1000) + " ")
f_ies.write(num2str(length_lum / 1000) + " ")
f_ies.write(num2str(height_lum / 1000) + "\n")

f_ies.write("1.0 1.0 ")			# ? ballast factor, future use
f_ies.write(num2str(power))
f_ies.write("\n")
for i in range(0, ng):
	f_ies.write(num2str(angle_g[i]) + " ")
f_ies.write("\n")
for i in range(0, mc):
	f_ies.write(num2str(angle_c[i]) + " ")
f_ies.write("\n")
for i in range(0, mc):
	for j in range(0, ng):
		f_ies.write(num2str(lum_intensity[i][j]) + " ")
	f_ies.write("\n")