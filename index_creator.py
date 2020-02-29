import math
from spacy.lang.en import English
from tqdm import tqdm
nlp = English()

class Docs:

	def __init__(self):
		self.docs=[]
		self.num_docs=0
		print("Docs Initialized")

	def push(self,doc):
		self.docs.append(doc)

	def clean_doc(self,doc):
		new_doc=""
		tag_status=0

		for c in doc:
			if(c=="<"):
				tag_status=1

			elif(c==">"):
				tag_status=0
				continue

			elif(tag_status==1):
				continue

			else:
				new_doc=new_doc+c

		return new_doc

	def populate(self,filename):
		#read the file , parse it and populate itself
		docs_file = open(filename, "rt") # opening the file to read different docs
		docs = docs_file.read()         # read the entire file into a string
		docs_file.close()
		
		doc=""
		doc_status=0
		len_docs=len(docs)
		doc_id=0

		for i in tqdm(range(0,len_docs)):
			if(doc_status==0 and docs[i]=='<' and docs[i+1]=='d' and docs[i+2]=='o' and docs[i+3]=='c'):
				doc=""
				doc_status=1

			if(doc_status==1 and docs[i]=='<' and docs[i+1]=='/' and docs[i+2]=='d' and docs[i+3]=='o' and docs[i+4]=='c' and docs[i+5]=='>'):
				doc=doc+"</doc>"
				doc=self.clean_doc(doc)
				self.push((doc_id,nlp(doc)))
				self.num_docs+=1
				doc_id+=1
				doc_status=0
				doc=""

			if(doc_status==1):
				doc=doc+docs[i]
						

		return self.docs

	def get_doc(self,doc_id):
		return self.docs[doc_id][1]

class Index:
	def __init__(self):
		self.index={}
		self.idf={}
		self.bi_index={}
		self.bi_idf={}
		print("Inverted Index Initialized..")

	def generate_index(self,Doc):
		#function to generate the inverted index
		for doc_id,doc in Doc.docs:
			#print("Doc ID: ",doc_id)
			for token in doc:
				if(self.index.get(token.text)!=None):
					if(self.index[token.text].get(doc_id)!=None):
						self.index[token.text][doc_id]+=1
					else:
						self.index[token.text][doc_id]=1
				else:
					self.index[token.text]={doc_id:1}

		print("Inverted Index Created")

		self.calculate_idf(Doc)

	def calculate_idf(self,Doc):
		#function to populate idf
		for term in self.index.keys():
			self.idf[term]=math.log(Doc.num_docs/len(self.index[term].keys()))

	def calculate_tf(self,term,doc_id):
		#function to calculate tf-score
		if(self.index.get(term)!=None and self.index[term].get(doc_id)!=None):
			return 1 + math.log(self.index[term][doc_id])
		else:
			return 0

class Bi_Index:

	def __init__(self):
		self.bi_index={}
		self.bi_idf={}
		print("Biword Inverted Index Initialized..")

	def generate_bi_index(self,Doc):
		#function to generate the inverted index
		for doc_id,doc in Doc.docs:
			len_doc=len(doc)
			for bi_term in zip(doc[0:-1],doc[1:]):
				if(self.bi_index.get((bi_term[0].text,bi_term[1].text))!=None):
					if(self.bi_index[(bi_term[0].text,bi_term[1].text)].get(doc_id)!=None):
						self.bi_index[(bi_term[0].text,bi_term[1].text)][doc_id]+=1
					else:
						self.bi_index[(bi_term[0].text,bi_term[1].text)][doc_id]=1
				else:
					self.bi_index[(bi_term[0].text,bi_term[1].text)]={doc_id:1}

		print("Biword Index Generated")

		self.calculate_bi_idf(Doc)


	def calculate_bi_tf(self,bi_term,doc_id):
		#function to calculate tf-score
		if(self.bi_index.get(bi_term)!=None and self.bi_index[bi_term].get(doc_id)!=None):
			return 1 + math.log(self.bi_index[bi_term][doc_id])
		else:
			return 0



	def calculate_bi_idf(self,Doc):
		#function to populate idf
		for bi_term in self.bi_index.keys():
			self.bi_idf[bi_term]=math.log(Doc.num_docs/len(self.bi_index[bi_term].keys()))








		
