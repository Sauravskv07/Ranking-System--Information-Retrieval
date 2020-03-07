class QueryCorrector:

	def __init__(self):
		print("Initialized Query Corrector..")
		self.mem = {}

	#function to calculate levenstein distance
	def levenshtein(self,s, t):
		if (s == ""):
			return len(t)
		if (t == ""):
			return len(s)
    
		if(s[-1] == t[-1]):
			cost=0
    	
		else:
			cost=1
       
		i1 = (s[:-1], t)
    
		if not i1 in self.mem:
			self.mem[i1] = self.levenshtein(*i1)
    
		i2 = (s, t[:-1])
    
		if not i2 in self.mem:
			self.mem[i2] = self.levenshtein(*i2)

		i3 = (s[:-1], t[:-1])
    
		if not i3 in self.mem:
			self.mem[i3] = self.levenshtein(*i3)

    
		res = min([self.mem[i1]+1, self.mem[i2]+1, self.mem[i3]+cost])
    
		return res

	#function to implement spelling correction in a query
	def query_corrector(self,query,index):

		flag=0

		new_query=""

		for term in query.split(' '):
			min_v=100
			min_t=term
			if(term not in index.keys()):
				flag=1
				for v_term in index.keys():
					distance=self.levenshtein(term,v_term)
					if(distance<min_v):
						min_v=distance
						min_t=v_term
			new_query=new_query+min_t+" "

		if(flag==1):
			print("Instead Showing Results for : ",new_query)

		return new_query

