"""
Name : Sahil Kumar
Date : 24/04/2024

Instructions to Run this python script:

1.To Run this Sript put the this python file(cosine_similarity_pair_wise.py) and data folder(named 25) in the same directory.
2.Now change the fpath(path of the data folder) variable with the path of the data folder(25)
3.open the terminal and go the directory of the as in 1.
4.run using the command : python cosine_similarity_pair_wise.py
"""
import time
s = time.time()
import os
import math
fpath = 'C:\\Users\\kumar\\Documents\\SEIR\\Project_3\\25'
def build_dict():
    """
    returns the dictionary of the all the doc files with doc id as the value
    """
    files = os.listdir(fpath)
    dictionary = {}
    for i in range(len(files)):
        dictionary[files[i]] = i+1
    # print(dictionary)
    return dictionary
build_dict()

def tokenize_doc(title_doc,text_doc):
    """
    returns the tokenized list for each docs
    """
    title_doc_tokens = title_doc.split()
    text_doc_tokens = text_doc.split()
    return title_doc_tokens+text_doc_tokens

token_dict = {}
def token_count_dict(token_lst):
    """
    returns the dictionary of the token with token id for each docs
    """
    global token_dict
    for i in range(len(token_lst)):
        if token_lst[i] not in token_dict:
            token_dict[token_lst[i]] = i+1
        else:
            token_dict[token_lst[i]] = token_dict[token_lst[i]]
    return token_dict

def term_freq(token_lst):
    """
    returns dictionary of term frequency for each docs
    """
    tf_dict = {}
    for token in token_lst:
        if token not in tf_dict:
            tf_dict[token] = 1
        else:
            tf_dict[token]+=1
    return tf_dict

def df_of_term(term,documents):
    """
    return the document frequency for every unique token
    """
    df = 0
    for doc_token in documents.values():
        if term in doc_token:
            df+=1
    return df

def idf_index_term(term,documents):
    """
    return the idf score for each index term
    """
    total_doc = len(documents)
    term_df=df_of_term(term,documents)
    if term_df == 0:
        return 0
    return math.log(total_doc/term_df)

def indexing():
    """
    return the tf*idf vector 
    """
    documents = {}
    doc_files = build_dict()
    for file_name,doc_id in doc_files.items():
        with open(os.path.join(fpath,file_name), 'r') as file:
            content = file.read()
            content = content.lower()
            start_index_title = content.find("<title>")+len("<title>")
            end_index_title = content.find("</title>")
            start_index_text = content.find("<text>")+len("<text>")
            end_index_text = content.find("</text>")
            title_content = content[start_index_title:end_index_title].strip()
            text_content = content[start_index_text:end_index_text].strip()
            tokenized_doc = tokenize_doc(title_content,text_content)
            documents[doc_id] = tokenized_doc
            # break
    idf_dict={}
    for doc_tokens in documents.values():
        for token in set(doc_tokens):
            if token not in idf_dict:
                idf_dict[token] = idf_index_term(token,documents)
    
    tfidf_vectors={}
    for doc_id,doc_tokens in documents.items():
        tfidf_vectors[doc_id]={}
        tf_dict = term_freq(doc_tokens)
        for token,tf in tf_dict.items():
            idf = idf_dict.get(token,0)
            tfidf_vectors[doc_id][token] = tf*idf
    

    #vector normalization
    for doc_id,doc_vector in tfidf_vectors.items():
        squared_sum = 0
        for value in doc_vector.values():
            squared_sum+=value**2
        mag_val = math.sqrt(squared_sum)
        
        if mag_val!=0:
            for token in doc_vector:
                doc_vector[token] = doc_vector[token]/mag_val
        else:
            for token in doc_vector:
                doc_vector[token] = 1
    return tfidf_vectors

def cosine_similarity_vectors(vector1,vector2):
    """
    compute the cosine similarity between the two vectors
    """
    dot_product = 0
    mag_vec1 = 0
    mag_vec2 = 0
    
    for token in vector1:
        if token in vector2:
            dot_product+=vector1[token]*vector2[token]
    for value in vector1.values():
        mag_vec1+=value**2
    for value in vector2.values():
        mag_vec2+=value**2
    
    mag_vec1 = math.sqrt(mag_vec1)
    mag_vec2 = math.sqrt(mag_vec2)
    
    if mag_vec1*mag_vec2!=0:
        return dot_product/(mag_vec1*mag_vec2)
    else:
        return 0

def top_similar_docs(tfidf_vectors):
    """
    returns the top 50 similar docs in the whole corpous 
    """
    similarity_matrix = {}
    doc_ids = list(tfidf_vectors.keys())
    for i in range(len(doc_ids)):
        for j in range(i+1, len(doc_ids)):
            doc_id1, doc_id2 = doc_ids[i],doc_ids[j]
            similarity = cosine_similarity_vectors(tfidf_vectors[doc_id1],tfidf_vectors[doc_id2])
            similarity_matrix[(doc_id1, doc_id2)] = similarity
    top_similarity = sorted(similarity_matrix.items(), key = lambda x: x[1],reverse = True)[:50]
    return top_similarity

if __name__=="__main__":
    doc_files = build_dict()
    tfidf_vectors = indexing()
    top_similarity = top_similar_docs(tfidf_vectors)
    for (doc_id1, doc_id2), similarity in top_similarity:
        doc_no1 = [key for key, val in doc_files.items() if val == doc_id1][0]
        doc_no2 = [key for key, val in doc_files.items() if val == doc_id2][0]
        print(f"Document {doc_no1} and Document {doc_no2} similarity: {similarity}")

e = time.time()
time_taken = e-s
print("total time taken is:")
print(e-s)
