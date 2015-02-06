class Measure:
	@classmethod
	def getRecall(cls, tp, fp, fn):
		return float(tp) / (tp + fn)

class Precision(Measure):
	@classmethod
	def getMeasure(cls, tp, fp, fn):
		return float(tp) / (tp + fp)

class FMeasure(Precision):
	@classmethod
	def getMeasure(cls, tp, fp, fn):
		p = Precision.getMeasure(tp, fp, fn)
		r = cls.getRecall(tp, fp, fn)
		if p+r == 0:
			return 0.
		else :
			return 2*p*r/(p+r)

class EMeasure(FMeasure):
	@classmethod
	def getMeasure(cls, tp, fp, fn):
		return 1 - FMeasure.getMeasure(tp, fp, fn)