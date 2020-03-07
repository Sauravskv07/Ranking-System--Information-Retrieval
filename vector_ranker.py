import math
from query_corrector import QueryCorrector

#class to implement vector ranking model
class Ranker:

	def __init__(self):
		self.score={}#dictionary to store scores of docs corresponding to the query
		print("Let's rank some queries")

	#function to assign rank via vanilla ranking model
	def rank(self,Index,query):

		term_count={}

		docs_union=[]

		for term in query.split(' '):
			if(term_count.get(term)==None):
				term_count[term]=1
			else:
				term_count[term]+=1

		for term in query.split(' '):
			if(Index.index.get(term)!=None):
				docs_union+=Index.index[term].keys()

		for doc_id in docs_union:
			sqr_wqt=0
			sqr_wdt=0

			for term in query.split(' '):
				wdt=Index.calculate_tf(term,doc_id)

				if(Index.idf.get(term)!=None):
					wqt=Index.idf[term]*(1+math.log(term_count[term]))
				else:
					wqt=0

				sqr_wdt+=wdt*wdt
				sqr_wqt+=wqt*wqt					
				
				if(self.score.get(doc_id)!=None):
					self.score[doc_id]+=wqt*wdt
				else:
					self.score[doc_id]=wqt*wdt

			n_factor=(math.sqrt(sqr_wqt)*math.sqrt(sqr_wdt))
			

			if(n_factor!=0):
				self.score[doc_id]/=n_factor

	#function to rank based on bi word index and spelling correction
	def rank_advance(self,Index,Bi_index,query,type):

		self.score={}
		
		if(type==0):
			self.rank(Index,query)

		else:

			query=QueryCorrector().query_corrector(query,Index.index)

			self.rank(Index,query)			
		
			bi_term_count={}

			for bi_term in zip(query.split(" ")[:-1], query.split(" ")[1:]):
				if(bi_term_count.get(bi_term)!=None):
					bi_term_count[bi_term]+=1
				else:
					bi_term_count[bi_term]=1


			docs_union=[]

			for bi_term in zip(query.split(" ")[:-1], query.split(" ")[1:]):
				if(Bi_index.bi_index.get(bi_term)!=None):
					docs_union+=Bi_index.bi_index[bi_term].keys()

			for doc_id in docs_union:
				sqr_wqt=0
				sqr_wdt=0
				score_d=0

				for bi_term in zip(query.split(" ")[:-1], query.split(" ")[1:]):
					
					wdt=Bi_index.calculate_bi_tf(bi_term,doc_id)
					
					if(Bi_index.bi_idf.get(bi_term)!=None):
						wqt=Bi_index.bi_idf[bi_term]*(1+math.log(bi_term_count[bi_term]))
					else:
						wqt=0

					sqr_wdt+=wdt*wdt
					sqr_wqt+=wqt*wqt					
				
					score_d+=wqt*wdt

				n_factor=(math.sqrt(sqr_wqt)*math.sqrt(sqr_wdt))
				
				if(n_factor!=0):
					self.score[doc_id]+=score_d/n_factor
				
		
		return self.score

