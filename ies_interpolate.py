import sys

new_cnt_ver = int(sys.argv[1])
new_cnt_hor = int(sys.argv[2])

f_org = open("original.ies", "r")
f_res = open("result.ies", "w")

def num2str(n):
	s = str(int(n * 10000) / 10000)
	if '.' in s:
		return s.rstrip('0').rstrip('.')
	else:
		return s

f_res.write(f_org.readline())

while True:
	line = f_org.readline()
	f_res.write(line)
	if line[0] != '[':
		break

line = f_org.readline()
items = line.split()
org_cnt_ver = int(items[3])
org_cnt_hor = int(items[4])
if new_cnt_ver < 1:
	new_cnt_ver = org_cnt_ver
if new_cnt_hor < 1:
	new_cnt_hor = org_cnt_hor
items[3] = num2str(new_cnt_ver)
items[4] = num2str(new_cnt_hor)
f_res.write(" ".join(items) + "\n")

f_res.write(f_org.readline())

line = f_org.readline()
items = line.split()
bal_fac = float(items[0])
fut_use = float(items[1])
input_watts = float(items[2])

ver_angles = []
hor_angles = []
line = f_org.readline()
max_ver_angle = [float(i) for i in line.split()][-1]
while True:
	line = f_org.readline()
	if line[0] != ' ':
		break
	max_ver_angle = [float(i) for i in line.split()][-1]

max_hor_angle = [float(i) for i in line.split()][-1]
while True:
	line = f_org.readline()
	if line[0] != ' ':
		break
	max_hor_angle = [float(i) for i in line.split()][-1]

ver_angles = [i * max_ver_angle / (new_cnt_ver - 1) for i in range(new_cnt_ver)]
hor_angles = [i * max_hor_angle / (new_cnt_hor - 1) for i in range(new_cnt_hor)]

angles = []
for i in range(org_cnt_hor):
	angles.append([float(j) for j in line.split()])
	while True:
		line = f_org.readline()
		if line == "" or line[0] != ' ':
			break
		angles[i] += [float(j) for j in line.split()]

line = ""
for i in range(new_cnt_ver):
	it = num2str(i * max_ver_angle / (new_cnt_ver - 1))
	if len(line + it) > 238:
		f_res.write(line + "\n")
		line = " "
	line += it + " "
f_res.write(line + "\n")

line = ""
for i in range(new_cnt_hor):
	it = num2str(i * max_hor_angle / (new_cnt_hor - 1))
	if len(line + it) > 238:
		f_res.write(line + "\n")
		line = " "
	line += it + " "
f_res.write(line + "\n")

def interpolate(p0, p1, p2, p3, x):
	return (-0.5 * p0 + 1.5 * p1 - 1.5 * p2 + 0.5 * p3) * x * x * x + \
		(p0 - 2.5 * p1 + 2 * p2 - 0.5 * p3) * x * x + \
		(-0.5 * p0 + 0.5 * p2) * x + p1

tmp_angles = []
for i in range(org_cnt_hor):
	tmp_angles.append([])
	for j in range(new_cnt_ver - 1):
		x = max_ver_angle / (new_cnt_ver - 1) * j
		it_idx = int(x / (max_ver_angle / (org_cnt_ver - 1)))
		p1 = angles[i][it_idx]
		p2 = angles[i][it_idx + 1]
		if it_idx == 0:
			p0 = p1
		else:
			p0 = angles[i][it_idx - 1]
		if it_idx == org_cnt_ver - 2:
			p3 = p2
		else:
			p3 = angles[i][it_idx + 2]
		tmp_angles[i].append(interpolate(p0, p1, p2, p3, x / (max_ver_angle / (org_cnt_ver - 1)) % 1))
	tmp_angles[i].append(interpolate(angles[i][-3], angles[i][-2], angles[i][-1], angles[i][-1], 1))

angles = []
for i in range(new_cnt_hor):
	angles.append([])
	for j in range(new_cnt_ver):
		angles[i].append(0)

line = ""
for j in range(new_cnt_ver):
	line = ""
	for i in range(new_cnt_hor - 1):
		x = max_hor_angle / (new_cnt_hor - 1) * i
		it_idx = int(x / (max_hor_angle / (org_cnt_hor - 1)))
		p1 = tmp_angles[it_idx][j]
		p2 = tmp_angles[it_idx + 1][j]
		if it_idx == 0:
			p0 = p1
		else:
			p0 = tmp_angles[it_idx - 1][j]
		if it_idx == org_cnt_hor - 2:
			p3 = p2
		else:
			p3 = tmp_angles[it_idx + 2][j]
		angles[i][j] = interpolate(p0, p1, p2, p3, x / (max_hor_angle / (org_cnt_hor - 1)) % 1)
	angles[-1][j] = interpolate(tmp_angles[-3][j], tmp_angles[-2][j], tmp_angles[-1][j], tmp_angles[-1][j], 1)

for i in range(new_cnt_hor):
	line = ""
	for j in range(new_cnt_ver):
		if len(line + num2str(angles[i][j])) > 238:
			f_res.write(line + "\n")
			line = " "
		line += num2str(angles[i][j]) + " "
	f_res.write(line + "\n")

f_org.close()
f_res.close()
