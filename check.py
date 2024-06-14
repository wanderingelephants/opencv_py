def check():
	c = a + b
	if c < 50:
		print('Less than 50')
		b = b * 2
		a = a + 10
	else:
		print('>= 50')
		a = a * 2
		b = b + 10
check()
