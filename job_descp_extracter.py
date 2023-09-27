import transformers
from transformers import AutoTokenizer,AutoModel
import numpy as np
from datasets import load_dataset
from sklearn.metrics.pairwise import cosine_similarity
from cv_extracter import cv_data

company_name = []
job_descriptions = []
cvs_embeddings = {}

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModel.from_pretrained("distilbert-base-uncased")
cv = cv_data
dataset = load_dataset("jacob-hugging-face/job-descriptions")

for i in range(0, 15):
    job_description = dataset["train"][i]['job_description']
    job_descriptions.append(job_description)
    job_description1 = dataset["train"][i]['company_name']
    company_name.append(job_description1)

job_descriptions_tokenized = [tokenizer(description, padding=True, truncation=True, return_tensors="pt") for description in job_descriptions]
job_descriptions_embeddings = [model(**tokens).last_hidden_state.mean(dim=1) for tokens in job_descriptions_tokenized]
#

for cv_id, cv_text in cv.items():
    # Tokenize and preprocess each CV
    cv_tokens = tokenizer(cv_text, padding=True, truncation=True, return_tensors="pt")

    # Convert text into embeddings
    cv_embedding = model(**cv_tokens).last_hidden_state.mean(dim=1).detach().numpy()

    # Store the CV embedding in the dictionary
    cvs_embeddings[cv_id] = cv_embedding


similarity_scores = {}

for jd_id, jd_tokens in enumerate(job_descriptions_tokenized):
    jd_embedding = model(**jd_tokens).last_hidden_state.mean(dim=1).detach().numpy()

    scores = {}
    for cv_id, cv_embedding in cvs_embeddings.items():
        score = cosine_similarity(jd_embedding, cv_embedding)[0][0]
        scores[cv_id] = score

    # Sort the CVs by similarity score (descending)
    sorted_scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))

    # Store the sorted scores in the similarity_scores dictionary
    similarity_scores[jd_id] = sorted_scores

# Get the top 5 CV matches for each job description
top_cv_matches = {}

for jd_id, scores in similarity_scores.items():
    top_cv_matches[jd_id] = list(scores.keys())[:5]

#
# print(similarity_scores)
# print(top_cv_matches)

for i in range(0,15):
    print(company_name[i])
    for ind, cvs in top_cv_matches.items():
        if(i==ind):
            print("IDs are: ")
            for j in cvs:
                print(j)

