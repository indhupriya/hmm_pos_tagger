import json
import sys
import time
import copy
import pprint

outerTextDictionary={}
outerDictionary={}
allStates=set()
mostLikelyState={}
def readValues():
	global outerTextDictionary,outerDictionary
	with open('hmmmodel.txt') as data_file:    
		data = json.load(data_file)
		outerTextDictionary=data[0]
		outerDictionary = data[1]
		#pprint.pprint(outerDictionary)


def readFile(pathToLearn):
	global outerTextDictionary,outerDictionary
	count=0
	
	with open(pathToLearn, "r") as fp:
		
		writer=open("hmmoutput.txt","w+")
		for line in fp:
			#print line
			prev=set()
			#print count
			count+=1
			probability={}
			backpointer={}
			words=line.split()

			for t in range(0,len(words)):
				#print "t ",t

				word=words[t]
				if word not in outerTextDictionary:
					outerTextDictionary[word]={}
					for tag in outerDictionary:
						if tag!='q0':
							outerTextDictionary[word][tag]=1
				
				if t==0:
					#qdash=set()
					for q in outerDictionary['q0']:
						
						try:
							if outerTextDictionary[word][q]!=0 :
								#qdash.add(q)
								temp1=float(outerDictionary["q0"][q])*float(outerTextDictionary[word][q])
								prev.add(q)
								probability[q]={0:temp1}
								backpointer[q]={0:'q0'}
						except:
							{}
					#print "q0"	
						
					
				else:
					#print "prev ",prev
					qdash=set()
					for q in outerDictionary:
						#print "q ",q
						try:
							if outerTextDictionary[word][q]!=0 and q!='q0':

								
								maxVal=-sys.maxint
								maxBack=-sys.maxint
								back=None
								for w in prev:
									
									if q in outerDictionary[w]:
										#print "w ",w
										temp=(probability[w][t-1])*(outerDictionary[w][q])*(outerTextDictionary[word][q])
										#b=probability[w][t-1]*outerDictionary[w][q]
										qdash.add(q)
								
										if(temp>maxVal):
											maxVal=temp
										#if(b>maxBack):
											back=w
								if q in probability:
									probability[q][t]=maxVal
									backpointer[q][t]=back
								else:
									probability[q]={t:maxVal}
									backpointer[q]={t:back}
						except:
							{}
					#raw_input()
					prev = qdash.copy()

					
					

					
				
			
			finalSolution=[]
			maxima=-sys.maxint 
			for keys in probability:
				try:
					maxvalue=probability[keys][len(words)-1]
					if maxvalue>maxima:
						maxima=maxvalue
						maxsol=keys
				except:
					{}
			#print maxsol
			finalSolution.append(maxsol)

			
			for index in range(len(words)-1,0,-1):
				finalSolution.append(backpointer[maxsol][index])
				maxsol=backpointer[maxsol][index]
				

			finalSolution.reverse()
			#print finalSolution
			str=""
			for index in range(0,len(words)):
				str+=words[index].decode('utf-8')+"/"+finalSolution[index].decode('utf-8')+" "
			#print str
			writer.write(str.encode('utf-8'))
			writer.write("\n")
			
		

if __name__ == "__main__":

	start_time = time.time()
	readValues()
	readFile(sys.argv[1])
	#writeToFile()
	print("--- %s seconds ---" % (time.time() - start_time))