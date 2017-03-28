import nltk
trueLabels = open("../labels.txt","r").readlines()[36332:]
predLabels = open("predictedLabels.txt","r").readlines()

metrics = []

def getPrecision(r, c):
	temp = [word for word in c if word in r]
	return len(temp)*1.0/len(c)

def getMetric(tr, pr):
	a = b = c = d = 0
	for rel in tr:
		c += 1
		rel = nltk.word_tokenize(rel)
		for cand in pr:
			a += 1
			cand = nltk.word_tokenize(cand)
			b += getPrecision(rel, cand)
		d += (b*1.0/a)
	return d*1.0/c


for i in range(12113):
	print i
	t = trueLabels[i].split("|")
	p = predLabels[i].split("|")
	t = [tt.rstrip().lower() for tt in t]
	p = [pp.rstrip().lower() for pp in p][1:]
	metrics.append(getMetric(t, p))


print metrics

print sum(metrics)/len(metrics)

print max(metrics)
