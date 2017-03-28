################## imports #############################
import operator
import glob
import pickle
import itertools
###################### creating predictions #####################
print "Collecting predictions...."
pred = {}         #contains predictions for all pos tag clfrs
score_files = glob.glob("scores/*.txt")

for score_file in score_files:
	print score_file
	name = score_file[7:].replace("-score.txt", "")
	pred[name] = []
	lines = open(score_file, "r").readlines()
	lines = lines[1:]
	prediction = ""
	predDict = {}
	for line in lines:
		scores = line.split(" ")
		for score in scores:
			score = score.split(":")
			predDict[int(score[0])] = float(score[1])

		#sort in descending order and pick up top 3
		newA = dict(sorted(predDict.iteritems(), key=operator.itemgetter(1), reverse=True)[:3])
		temp = [str(i) for i in newA.keys()]
		pred[name].append(temp)

	# save to file if needed ######
	#
	# predfile = name + "-pred.txt"
	# f1 = open(predfile, "w")
	# f1.write(prediction)
	# f1.close()
	# print "--> Done!"
	#
	#############################


#################################################################
print "creating index 2 word maps...."
pred_pos = ['in', 'cd', 'jj', 'nn', 'nns', 'nnp', 'vbn', 'vbd', 'vbg', 'vb', 'nnps']   #the tags which have clfrs trained
pkls = glob.glob("../postag_data/*.pkl")   ##get this from google drive link of categorized data
pklDict = {}  
for pickl in pkls:
	print pickl
	name = pickl.replace("../postag_data/", "")[:-10]
	pklDict[name] = {v: k for k, v in pickle.load(open(pickl, "r")).iteritems()}

preds = open("META-CLFR.txt", "r").readlines()
my_map = pickle.load(open("../taggedLabelDict.pkl", "r"))
taggedLabelDict = {v: k for k, v in my_map.iteritems()}
finalAns = ''

#take top 3 predictions of every pos tag clfr in the predicted meta label and return all possible combinations
def getPermutations(l):      
	permuts = list(itertools.product(*l))
	ans = ''
	for t in permuts:
		ans += "|"
		ans += " ".join(t)
	return ans


print "getting predicted labels..."
for i in range(len(preds)):
	print i
	finalPreds = ''
	p = preds[i].split(" ")
	p = [taggedLabelDict[int(k)] for k in p]
	for j in p:
		temp = []
		symbols = j.split(" ")
		symbols = [symbol.lower() for symbol in symbols]
		for s in symbols:
			if s in ["(", ")", "-", ":", ";", ","]:          #to be taken as it is
				temp.append([s])
			elif s not in pred_pos:                          #no clfr since support<5
				temp.append(pklDict[s].values())
			else:
				temp1 = [pklDict[s][int(q)] for q in pred[s][i]]
				temp.append(temp1)
		perms = getPermutations(temp)
		finalPreds += perms
	finalAns += finalPreds
	finalAns += '\n'


#write to file
myf = open("predictedLabels.txt","w")
myf.write(finalAns)
myf.close()
