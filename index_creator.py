import math
from spacy.lang.en import English
from tqdm import tqdm
nlp = English()

#class Docs for implementation of parsing of docs, cleaning of docs, population of docs object.
class Docs:
	def __init__(self):
		
		self.docs=[]#to store the nlp objects of docs, tokenized
		self.docs_ids=[] # to store the ids of the docs
		self.docs_text=[] # to store the text corresponding to each docs.

		self.num_docs=0 # to store the net number of docs processed
		print("Docs Initialized")

	#function to push a new doc into the doc array
	def push(self,doc):
		self.docs.append(doc)

	#to clean the doc of all tags for index creation
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

	#to populate the Docs object with all the docs given in the filename
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

				self.docs_text.append(doc)

				doc=self.clean_doc(doc)

				self.push(nlp(doc))
				
				self.docs_ids.append(doc_id)

				self.num_docs+=1
				
				doc_id+=1
				
				doc_status=0
				
				doc=""

			if(doc_status==1):
				doc=doc + docs[i]
						

	def get_doc_text(self,doc_id):
		return self.docs_text[doc_id]

#class for implementation of single term indexes
class Index:
	def __init__(self):

		self.index={} # dictionary to store the index
		self.idf={} # dictionary to store the idf value corresponding to each term
		self.bi_index={} # dictionary to store the bi-word indexed
		self.bi_idf={} #dictionary to store the idf values corresponding to each bi word
		print("Inverted Index Initialized..")

	#function to generate term index
	def generate_index(self,Doc):
		#function to generate the inverted index
		for doc_id in Doc.docs_ids:
			#print("Doc ID: ",doc_id)
			for token in Doc.docs[doc_id]:
				if(self.index.get(token.text)!=None):
					if(self.index[token.text].get(doc_id)!=None):
						self.index[token.text][doc_id]+=1
					else:
						self.index[token.text][doc_id]=1
				else:
					self.index[token.text]={doc_id:1}

		print("Inverted Index Created")

		self.calculate_idf(Doc)

	#function to calculate idf.
	def calculate_idf(self,Doc):
		#function to populate idf
		for term in self.index.keys():
			self.idf[term]=math.log(Doc.num_docs/len(self.index[term].keys()))

	#function to calculate log term frequency of term in each doc
	def calculate_tf(self,term,doc_id):
		#function to calculate tf-score
		if(self.index.get(term)!=None and self.index[term].get(doc_id)!=None):
			return 1 + math.log(self.index[term][doc_id])
		else:
			return 0

#class to implement bi word indexes
class Bi_Index:

	def __init__(self):
		self.bi_index={}#dictionary to store bi word
		self.bi_idf={}#dictionary to store idf value of each bi word
		print("Biword Inverted Index Initialized..")

	#function to generate bi word indexes
	def generate_bi_index(self,Doc):
		
		for doc_id in Doc.docs_ids:
			for bi_term in zip(Doc.docs[doc_id][0:-1],Doc.docs[doc_id][1:]):
				if(self.bi_index.get((bi_term[0].text,bi_term[1].text))!=None):
					if(self.bi_index[(bi_term[0].text,bi_term[1].text)].get(doc_id)!=None):
						self.bi_index[(bi_term[0].text,bi_term[1].text)][doc_id]+=1
					else:
						self.bi_index[(bi_term[0].text,bi_term[1].text)][doc_id]=1
				else:
					self.bi_index[(bi_term[0].text,bi_term[1].text)]={doc_id:1}

		print("Biword Index Generated")

		self.calculate_bi_idf(Doc)

	#function to calculate tf-score
	def calculate_bi_tf(self,bi_term,doc_id):
		
		if(self.bi_index.get(bi_term)!=None and self.bi_index[bi_term].get(doc_id)!=None):
			return 1 + math.log(self.bi_index[bi_term][doc_id])
		else:
			return 0


	#function to populate idf
	def calculate_bi_idf(self,Doc):
		
		for bi_term in self.bi_index.keys():
			self.bi_idf[bi_term]=math.log(Doc.num_docs/len(self.bi_index[bi_term].keys()))








		
