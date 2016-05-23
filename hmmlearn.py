import sys
import json 
import time
import pprint

content=[]
outerTextDictionary={}
outerDictionary={}
transitionDictionary={}
emissionDictionary={}



def getOuterTextDictionary(word,text):
	global outerTextDictionary
	if text in outerTextDictionary:
		if word in outerTextDictionary[text]:
			outerTextDictionary[text][word]+=1
		else:
			outerTextDictionary[text][word]=1
	else:
		outerTextDictionary[text]={word:1}

def getStates(z,words,word):
	try:
	
		wordNext=words[z+1]
		wordNext=wordNext[-2:]
		if word in outerDictionary:
			emissionDictionary[word]+=1
			transitionDictionary[word]+=1
			if wordNext in outerDictionary[word]:
				outerDictionary[word][wordNext]+=1
			else:
				outerDictionary[word][wordNext]=1
		else:
			transitionDictionary[word]=1
			emissionDictionary[word]=1
			outerDictionary[word]={wordNext:1}
	except:
		if word in emissionDictionary:
			emissionDictionary[word]+=1

		else:
			emissionDictionary[word]=1	

def readFile(pathToLearn):
	count=0
	with open(pathToLearn, "r") as fp:
		for line in fp:
			# print count
			# count+=1
			#print line
			words=line.split()
			for z in range(-1,len(words)):
				if(z==-1):
					word="q0"
					#text=""
				else:
					word=words[z]
					text=word[0:-3]
					word=word[-2:]
					getOuterTextDictionary(word,text)
				getStates(z,words,word)


#def printFunc():
	#pprint.pprint(outerDictionary)
	#pprint.pprint(transitionDictionary)
	#pprint.pprint(outerTextDictionary)
	#pprint.pprint(emissionDictionary)
	# print "dictionary "			
	# for keys in outerDictionary.keys():
	# 	print keys,outerDictionary[keys]

	# print "transitionDictionary "
	# for keys in transitionDictionary.keys():
	# 	print keys,transitionDictionary[keys]

	# print "emissionDictionary"
	# for keys in emissionDictionary.keys():
	# 	print keys,emissionDictionary[keys]
	# print "word Dictionary "
	# for keys in outerTextDictionary.keys():
	# 	print keys,outerTextDictionary[keys]
		

	#raw_input()
def calcTransmission():
	global outerTextDictionary
	for key in outerDictionary:
		for innerkey in outerDictionary[key]:
			outerDictionary[key][innerkey]=float(outerDictionary[key][innerkey])/transitionDictionary[key]
def calcEmission():
	global outerTextDictionary
	for key in outerTextDictionary:
		for innerkey in outerTextDictionary[key]:
			outerTextDictionary[key][innerkey]=float(outerTextDictionary[key][innerkey])/emissionDictionary[innerkey]
def writeToFile():
	jsonDumpFile=[]
	jsonDumpFile.append(outerTextDictionary)
	jsonDumpFile.append(outerDictionary)
	#jsonDumpFile.append(emissionDictionary)
	#jsonDumpFile.append(transitionDictionary)
	with open('hmmmodel.txt','w+') as myfile:
		json.dump(jsonDumpFile,myfile)
		
def smoothing():
	global outerTextDictionary
	for key in outerDictionary.keys():
		for key2 in transitionDictionary.keys():
			if key2 not in outerDictionary[key]:
				outerDictionary[key][key2]=1
			else:
				outerDictionary[key][key2]+=1
	for key in transitionDictionary.keys():
		transitionDictionary[key]+=len(transitionDictionary)	



if __name__ == "__main__":
	start_time = time.time()
	readFile(sys.argv[1])
	smoothing()
	calcTransmission()
	calcEmission()
	#printFunc()
	
	writeToFile()
	print("--- %s seconds ---" % (time.time() - start_time))