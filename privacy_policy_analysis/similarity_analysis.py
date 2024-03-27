# get list of privacy policies
import chardet
import os
policies = {}
for office in os.listdir('./policy_annotation/policy_words'):
    for filename in os.listdir(f'./policy_annotation/policy_words/{office}'):
        # Detect file encoding and read the word sets of the two policies
        with open(f'./policy_annotation/policy_words/{office}/{filename}', 'rb') as f:
            result = chardet.detect(f.read())
        with open(f'./policy_annotation/policy_words/{office}/{filename}', 'r', encoding=result['encoding']) as f:
            policies[office + "/" + filename] = f.read()

# convert privacy policies to vectors
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(policies.values()).toarray().tolist()

# dictionary mapping names to vectors
policy_vectors = {policy_name: vector for policy_name, vector in zip(policies.keys(), vectors)}

# get the vectors value
vector_values = list(policy_vectors.values())

from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans

def k_means(num_clusters, update_file=False):
    # calculate the similarity index
    kmeans = KMeans(n_clusters=num_clusters)

    # fit the kmeans model
    kmeans.fit(vector_values)

    # predict the clusters
    cluster_centers = kmeans.predict(vector_values)

    if update_file:
        # Group vectors by cluster
        clusters = {i: [] for i in range(num_clusters)}
        for i, cluster in enumerate(cluster_centers):
            clusters[cluster].append(list(policy_vectors.keys())[i])

        # Write each cluster to a separate file
        for cluster, policy_names_in_cluster in clusters.items():
            with open(f'./clusters/cluster_{cluster}.txt', "w") as f:
                for policy_name in policy_names_in_cluster:
                    f.write(f"{policy_name}\n")

    # calculate score
    score = silhouette_score(vector_values, cluster_centers)
    return score

# calculate the silhouette score for different number of clusters
# scores = []
# for i in range(2, 11):
#     score = k_means(i)
#     scores.append(score)
#     print(f"Silhouette score for {i} clusters: {score}")

k_means(num_clusters=8, update_file=True) 