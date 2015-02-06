class Curve:
	def __init__(self, x=[], y=[]):
		self.name = ""
		self.x = x
		self.y = y

	def append(self, i, j):
		self.x.append(i)
		self.y.append(j)

	def value(self, i):
		index = self.x.index(i)
		return self[index]

	def __getitem__(self, i):
		return self.y[i]

	def removeWrongPoints(self):
		x = [self.x[-1]]
		y = [self.y[-1]]
		for i in range(len(self)-2,-1,-1):
			if self.y[i]>=y[-1]:
				x.append(self.x[i])
				y.append(self.y[i])
		x.reverse()
		y.reverse()
		self.y = y
		self.x = x

	def extrapolate(self, x):
		y = [0. for i in x]
		i = 0
		for j in self.x:
			while i < len(x) and x[i] <= j*100:
				y[i] = self.value(j)
				i+=1
		self.y = y
		self.x = x

	def __len__(self):
		return len(self.x)

	def __add__(self, other):
		add = Curve([],[])
		for i in range(0,min(len(self),len(other))):
			add.append(self.x[i], self.y[i] + other.y[i])
		return add

	def __rmul__(self, scalar):
		mul = Curve([],[])
		for i in range(0,len(self)):
			mul.append(self.x[i], scalar * self.y[i])
		return mul

class CSVFile:
	@staticmethod
	def exportToCSV(curves, filename):
		with open(filename, "w") as csvFile:
			csvFile.write(CSVFile.curvesToCSV(curves))

	@staticmethod
	def curvesToCSV(curves):
		s = ", ".join(map(lambda c: c.name, curves))
		s += "\n"
		length = min(map(len, curves))
		for i in range(0,length):
			s += ", ".join(map(lambda c: str(c[i]), curves))
			s += "\n"
		return s 