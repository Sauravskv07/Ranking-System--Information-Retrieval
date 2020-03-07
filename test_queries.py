import vector_ranker as vr
from index_creator import Index,Bi_Index,Docs
from operator import itemgetter
try:
    import cPickle as pickle
except ImportError:  # python 3.x
    import pickle

#menu driven interface of the search engine
def main():

	R_Pro=vr.Ranker()

	print("Loading Indexes")
	
	with open('index.p', 'rb') as fp:
		index = pickle.load(fp)
	
	with open('bi_index.p', 'rb') as fp:
		bi_index = pickle.load(fp)

	print("Index Loaded")

	with open('docs.p', 'rb') as fp:
		D = pickle.load(fp)

	while(1):

		query=input("Enter your Query Here: ")

		choice=int(input("Press 0 for normal query, Press 1 for advance query:  "))

		if(choice==0 or choice==1):
			
			scores=R_Pro.rank_advance(index,bi_index,query,choice)

			scores_list=sorted(scores.items(), key=itemgetter(1), reverse= True)

			k=int(input("Enter Number of Documents Desired: "))

			for doc_id,score in scores_list[0:k]:
				print("--------------------------------------------------------------------------------------------------------------")
				print(doc_id,"    ",score)
				print(D.get_doc_text(doc_id)[0:150])

		else:
			print("Invalid Entry")


main()





