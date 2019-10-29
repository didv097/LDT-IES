import sys

new_mc = int(sys.argv[1])
new_ng = int(sys.argv[2])

f_org = open("original.ldt", "r")
f_res = open("result.ldt", "w")

def num2str(n):
	return "{:g}".format(n)

for i in range(3):
	f_res.write(f_org.readline())

mc = int(f_org.readline())			# Number of C-planes between 0 and 360 degrees (usually 24 for interior, 36 for road lighting luminaires)
dc = float(f_org.readline())		# Distance between C-planes
ng = int(f_org.readline())			# Number of luminous intensities in each C-plane
dg = float(f_org.readline())		# Distance between luminous intensities per C-plane

if new_mc < 1:
	f_res.write(num2str(mc) + "\n")
	f_res.write(num2str(dc) + "\n")
	new_mc = mc
else:
	f_res.write(num2str(new_mc) + "\n")
	f_res.write(num2str(360 / new_mc) + "\n")
if new_ng < 1:
	f_res.write(num2str(ng) + "\n")
	f_res.write(num2str(dg) + "\n")
	new_ng = ng
else:
	f_res.write(num2str(new_ng) + "\n")
	f_res.write(num2str(90 / (new_ng - 1)) + "\n")

for i in range(35):
	f_res.write(f_org.readline())

for i in range(mc + ng):
	f_org.readline()

for i in range(new_mc):
	f_res.write(num2str(360 / new_mc * i) + "\n")
for i in range(new_ng):
	f_res.write(num2str(90 / (new_ng - 1) * i) + "\n")

lum_intensity = []
tmp_lum_intensity = []
for i in range(mc):
	lum_intensity.append([])
	for j in range(ng):
		line = f_org.readline()
		if line == "":
			break
		lum_intensity[i].append(float(line))
	if j < ng - 1:
		lum_intensity.pop()
		break

def interpolate(p0, p1, p2, p3, x):
	return (-0.5 * p0 + 1.5 * p1 - 1.5 * p2 + 0.5 * p3) * x * x * x + \
		(p0 - 2.5 * p1 + 2 * p2 - 0.5 * p3) * x * x + \
		(-0.5 * p0 + 0.5 * p2) * x + p1

for i in range(mc):
	tmp_lum_intensity.append([])
	for j in range(new_ng - 1):
		x = 90 / (new_ng - 1) * j
		it_idx = int(x / dg)
		p1 = lum_intensity[i][it_idx]
		p2 = lum_intensity[i][it_idx + 1]
		if it_idx == 0:
			p0 = p1
			p3 = lum_intensity[i][it_idx + 2]
		elif it_idx == ng - 2:
			p3 = p2
			p0 = lum_intensity[i][it_idx - 1]
		else:
			p0 = lum_intensity[i][it_idx - 1]
			p3 = lum_intensity[i][it_idx + 2]
		tmp_lum_intensity[i].append(interpolate(p0, p1, p2, p3, x % dg / dg))
	tmp_lum_intensity[i].append(interpolate(lum_intensity[i][ng - 3], lum_intensity[i][ng - 2], lum_intensity[i][ng - 1], lum_intensity[i][ng - 1], 1))

lum_intensity = []
for i in range(new_mc):
	lum_intensity.append([])
	for j in range(new_ng):
		lum_intensity[i].append(0)

for j in range(new_ng):
	for i in range(new_mc):
		x = 360 / new_mc * i
		it_idx = int(x / dc)
		p1 = tmp_lum_intensity[it_idx][j]
		p2 = tmp_lum_intensity[(it_idx + 1) % mc][j]
		if it_idx == 0:
			p0 = p1
			p3 = tmp_lum_intensity[(it_idx + 2) % mc][j]
		elif it_idx == mc - 1:
			p3 = p2
			p0 = tmp_lum_intensity[it_idx - 1][j]
		else:
			p0 = tmp_lum_intensity[it_idx - 1][j]
			p3 = tmp_lum_intensity[(it_idx + 2) % mc][j]
		lum_intensity[i][j] = interpolate(p0, p1, p2, p3, x % dc / dc)

for i in range(new_mc):
	for j in range(new_ng):
		f_res.write(num2str(lum_intensity[i][j]) + "\n")

f_org.close()
f_res.close()
