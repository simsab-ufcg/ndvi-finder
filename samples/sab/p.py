valid = []
for i in range(64, 68):
	valid.append((214, i))
for i in range(63, 69):
	valid.append((215, i))
for i in range(63, 73):
	valid.append((216, i))
for i in range(62, 73):
	valid.append((217, i))
for i in range(62, 73):
	valid.append((218, i))
for i in range(62, 73):
	valid.append((219, i))
for i in range(65, 73):
	valid.append((220, i))
for i in range(67, 69):
	valid.append((221, i))
with open('path_row.txt') as open_file:
	for line in open_file:
		line_sp = line.split(' ')
		id = line_sp[0]
		res = []
		res.append(id)
		for i in range(1, (len(line_sp) - 1)/2 + 1):
			path = int(line_sp[2 * i - 1])
			row = int(line_sp[2 * i])
			if (path, row) in valid:
				res.append(str(path))
				res.append(str(row))
		print ' '.join(res)
	
