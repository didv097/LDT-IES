import sys

new_mc = int(sys.argv[1])						# first parameter - new org_mc
new_ng = int(sys.argv[2])						# first parameter - new org_ng

f_org = open("original.ldt", "r")
f_res = open("result.ldt", "w")

def num2str(n):											# convert number to string
	s = str(int(n * 10000) / 10000)
	if '.' in s:
		return s.rstrip('0').rstrip('.')
	else:
		return s

for i in range(3):
	f_res.write(f_org.readline())

org_mc = int(f_org.readline())			# Number of C-planes between 0 and 360 degrees (usually 24 for interior, 36 for road lighting luminaires)
org_dc = float(f_org.readline())		# Distance between C-planes
org_ng = int(f_org.readline())			# Number of luminous intensities in each C-plane
org_dg = float(f_org.readline())		# Distance between luminous intensities per C-plane

max_angle_c = org_mc * org_dc				# 360
max_angle_g = (org_ng - 1) * org_dg	# 90

if new_mc < 1:											# validate parameters
	f_res.write(num2str(org_mc) + "\n")
	f_res.write(num2str(org_dc) + "\n")
	new_mc = org_mc
else:
	f_res.write(num2str(new_mc) + "\n")
	f_res.write(num2str(max_angle_c / new_mc) + "\n")
if new_ng < 1:
	f_res.write(num2str(org_ng) + "\n")
	f_res.write(num2str(org_dg) + "\n")
	new_ng = org_ng
else:
	f_res.write(num2str(new_ng) + "\n")
	f_res.write(num2str(max_angle_g / (new_ng - 1)) + "\n")

for i in range(35):									# write lines that are unnecessary to change
	f_res.write(f_org.readline())

for i in range(org_mc + org_ng):		# read angles C & G
	f_org.readline()

for i in range(new_mc):							# write new angles C & G
	f_res.write(num2str(max_angle_c / new_mc * i) + "\n")
for i in range(new_ng):
	f_res.write(num2str(max_angle_g / (new_ng - 1) * i) + "\n")

lum_intensity = []
tmp_lum_intensity = []
for i in range(org_mc):							# read luminous intensities
	lum_intensity.append([])
	for j in range(org_ng):
		line = f_org.readline()
		if line == "":
			break
		lum_intensity[i].append(float(line))
	if j < org_ng - 1:
		lum_intensity.pop()
		break

# interpolating function
# https://www.paulinternet.nl/?page=bicubic
def interpolate(p0, p1, p2, p3, x):
	return (-0.5 * p0 + 1.5 * p1 - 1.5 * p2 + 0.5 * p3) * x * x * x + \
		(p0 - 2.5 * p1 + 2 * p2 - 0.5 * p3) * x * x + \
		(-0.5 * p0 + 0.5 * p2) * x + p1

for i in range(org_mc):							# interpolate angles G
	tmp_lum_intensity.append([])
	for j in range(new_ng - 1):
		x = max_angle_g / (new_ng - 1) * j
		it_idx = int(x / org_dg)
		p1 = lum_intensity[i][it_idx]
		p2 = lum_intensity[i][it_idx + 1]
		if it_idx == 0:
			p0 = p1
			p3 = lum_intensity[i][it_idx + 2]
		elif it_idx == org_ng - 2:
			p3 = p2
			p0 = lum_intensity[i][it_idx - 1]
		else:
			p0 = lum_intensity[i][it_idx - 1]
			p3 = lum_intensity[i][it_idx + 2]
		tmp_lum_intensity[i].append(interpolate(p0, p1, p2, p3, x % org_dg / org_dg))
	tmp_lum_intensity[i].append(interpolate(lum_intensity[i][org_ng - 3], \
		lum_intensity[i][org_ng - 2], lum_intensity[i][org_ng - 1], lum_intensity[i][org_ng - 1], 1))

lum_intensity = []
for i in range(new_mc):
	lum_intensity.append([])
	for j in range(new_ng):
		lum_intensity[i].append(0)

for j in range(new_ng):							# interpolate angles C
	for i in range(new_mc):
		x = max_angle_c / new_mc * i
		it_idx = int(x / org_dc)
		p1 = tmp_lum_intensity[it_idx][j]
		p2 = tmp_lum_intensity[(it_idx + 1) % org_mc][j]
		if it_idx == 0:
			p0 = p1
			p3 = tmp_lum_intensity[(it_idx + 2) % org_mc][j]
		elif it_idx == org_mc - 1:
			p3 = p2
			p0 = tmp_lum_intensity[it_idx - 1][j]
		else:
			p0 = tmp_lum_intensity[it_idx - 1][j]
			p3 = tmp_lum_intensity[(it_idx + 2) % org_mc][j]
		lum_intensity[i][j] = interpolate(p0, p1, p2, p3, x % org_dc / org_dc)

for i in range(new_mc):						# write new angles
	for j in range(new_ng):
		f_res.write(num2str(lum_intensity[i][j]) + "\n")

f_org.close()
f_res.close()
