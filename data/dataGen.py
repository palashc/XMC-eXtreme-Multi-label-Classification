import pickle
import nltk

def remspace(my_str):  #remove irritating spaces
    if len(my_str) < 2: # returns ' ' unchanged
        return my_str
    if my_str[-1] == '\n':
        if my_str[-2] == ' ':
            return my_str[:-2] + '\n'
    if my_str[-1] == ' ':
        return my_str[:-1]
    return my_str


pkl_file = open('labelDict.pkl', 'rb')
labelDict = pickle.load(pkl_file)
invLabelDict = {v: k for k,v in labelDict.iteritems()}     # index -> label mapping

data = open("dataset.txt","r").readlines()

pkl_file = open('uniqTag2WordDict.pkl', 'rb')
tagWordDict = pickle.load(pkl_file)

final = ""
i = 0
for d in data:
	print i
	temp = d.split(",")   
	temp1 = temp.pop()
	temp1 = temp1.split(" ")
	temp.append(temp1[0])             #temp now has all label indices
	feature = " ".join(temp1[1:])    #feature vector, to be appended with n-grams later
	newLabels = []
	for t in temp:					#iterating ann all labels
		t = int(t)
		label = invLabelDict[t]
		pos_tags = nltk.pos_tag(nltk.word_tokenize(label))     #get pos tags for each word in the label
		for tup in pos_tags:
			if tup[1] == 'NN':										
				try:
					newLabels.append(str(tagWordDict['NN'].index(tup[0])))   #make entry in the tag->word map
				except:
					pass
	if (1):
		newLabels = ",".join(set(newLabels))				#create string to write into the data file
		s = newLabels + " " + feature
		final += remspace(s)
	i += 1

f = open("NN-Data.txt","w")
f.write(final)
f.close()

