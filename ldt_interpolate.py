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
else:
	f_res.write(num2str(new_mc) + "\n")
	f_res.write(num2str(360 / new_mc) + "\n")
if new_ng < 1:
	f_res.write(num2str(ng) + "\n")
	f_res.write(num2str(dg) + "\n")
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
for i in range(0, mc):
	lum_intensity.append([])
	for j in range(0, ng):
		line = f_org.readline()
		if line == "":
			break
		lum_intensity[i].append(float(line))
	if j < ng - 1:
		lum_intensity.pop()
		break
lum_intensity.append(lum_intensity[0])

f_org.close()
f_res.close()
