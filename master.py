import vector_ranker as vr
import index_creator as idx
from operator import itemgetter


def main():
	D=idx.Docs()
	
	D.populate("wiki_09_AN TRIAL")

	index=idx.Index()

	index.generate_index(D)

	bi_index=idx.Bi_Index()
	
	bi_index.generate_bi_index(D)

	R_Pro=vr.Ranker()

	while(1):

		query=input("Enter your Query Here: ")

		choice=int(input("Press 0 for normal query, Press 1 for advance query:  "))

		if(choice==0 or choice==1):
			
			scores=R_Pro.rank_advance(index,bi_index,query,choice)

			scores_list=sorted(scores.items(), key=itemgetter(1), reverse= True)

			k=int(input("Enter Number of Documents Desired: "))

			for doc_id,score in scores_list[0:k]:
				print(doc_id,"    ",score)
				print(D.get_doc_text(doc_id))

		else:
			print("Invalid Entry")



main()





