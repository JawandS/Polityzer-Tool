import os
import chardet

# consider the use of policy templates by comparing similarity of words in the policies.

# generate a word index for each policy
def gen_candidates_word_usage():
    # go through policy text
    for office in os.listdir('./policy_annotation/policy_text'):
        for filename in os.listdir(f'./policy_annotation/policy_text/{office}'):
            with open(f'./policy_annotation/policy_text/{office}/{filename}', 'r', encoding="utf8") as f:
                text = f.read()
                # split the text into words
                words = [word.replace(',' , '').replace('�', '').replace('(', '').replace(')', '').replace('.', '').lower() for word in text.split()]
                # create a set of words
                word_set = set(words)
                # write the set to a file
                with open(f'./policy_annotation/policy_words/{office}/{filename}', "w") as f:
                    for word in word_set:
                        f.write(word + "\n")

# calculate the similarity index between two policies
def calculate_similarity_index(candidate_one, candidate_two):
    # Detect file encoding and read the word sets of the two policies
    with open(f'./policy_annotation/policy_words/{candidate_one}', 'rb') as f:
        result = chardet.detect(f.read())
    with open(f'./policy_annotation/policy_words/{candidate_one}', 'r', encoding=result['encoding']) as f:
        candidate_one_words = set(f.read().splitlines())

    with open(f'./policy_annotation/policy_words/{candidate_two}', 'rb') as f:
        result = chardet.detect(f.read())
    with open(f'./policy_annotation/policy_words/{candidate_two}', 'r', encoding=result['encoding']) as f:
        candidate_two_words = set(f.read().splitlines())

    # calculate the similarity index
    intersection_len = len(candidate_one_words.intersection(candidate_two_words))
    union_len = len(candidate_one_words.union(candidate_two_words))
    similarity_index = intersection_len / union_len
    return similarity_index

# generate a similarity index for each pair of policies
def gen_similarity_index():
    # generate list of candidates
    candidate_list = []
    for office in os.listdir('./policy_annotation/policy_words'):
        for filename in os.listdir(f'./policy_annotation/policy_words/{office}'):
            candidate_list.append(office + "/" + filename)
    # calculate similarity index for each pair of candidates
    similarity_indices = {}
    for i in range(len(candidate_list)):
        for j in range(i + 1, len(candidate_list)):
            candidate_one = candidate_list[i]
            candidate_two = candidate_list[j]
            similarity_index = calculate_similarity_index(candidate_one, candidate_two)
            similarity_indices[(candidate_one, candidate_two)] = similarity_index
            # print
            print(f"{candidate_one} {candidate_two} {similarity_index}")
    # write to file
    with open(f'./policy_annotation/similarity_indices.txt', "w") as f:
        for pair in similarity_indices:
            f.write(f"{pair[0]} {pair[1]} {similarity_indices[pair]}\n")

# filter the high similarity indices
def filter_high_similarity():
    with open('./policy_annotation/similarity_indices.txt', 'r') as f:
        similarity_indices = f.read().splitlines()
    high_similarity_indices = []
    for index in similarity_indices:
        if float(index.split()[2]) > 0.7:
            high_similarity_indices.append(index)
    # write to file
    with open(f'./policy_annotation/high_similarity_indices.txt', "w") as f:
        for index in high_similarity_indices:
            f.write(f"{index}\n")

# count unique candidates
def count_unique_candidates():
    with open('./policy_annotation/high_similarity_indices.txt', 'r') as f:
        similarity_indices = f.read().splitlines()
    candidates = set()
    for index in similarity_indices:
        candidates.add(index.split()[0])
        candidates.add(index.split()[1])
    print(len(candidates))

# generate the similarites between candidates in the clusters
def gen_cluster_similarity():
    # get the jaccard similarities between candidates
    similarity_dict = {}
    with open('./policy_annotation/similarity_indices.txt', 'r') as f:
        similarity_indices = f.read().splitlines()
        for index in similarity_indices:
            candidate_one = index.split()[0]
            candidate_two = index.split()[1]
            similarity_index = index.split()[2]
            similarity_dict[(candidate_one, candidate_two)] = similarity_index
            similarity_dict[(candidate_two, candidate_one)] = similarity_index
    # go through clusters
    for cluster in os.listdir('./clusters'):
        # get the candidates in the cluster
        with open(f'./clusters/{cluster}', 'r') as f:
            candidates = f.read().splitlines()
        # write the similarities to a file
        with open(f'./cluster_similarity/{cluster}', 'w') as f:
            for i in range(len(candidates)):
                for j in range(i + 1, len(candidates)):
                    candidate_one = candidates[i]
                    candidate_two = candidates[j]
                    print(f"{candidate_one} {candidate_two} {similarity_dict[(candidate_one, candidate_two)]}")
                    f.write(f"{candidate_one} {candidate_two} {similarity_dict[(candidate_one, candidate_two)]}\n")

# filter the similarity in clusters
def gen_high_sim_clusters():
    for cluster in os.listdir('./cluster_similarity'):
        with open(f'./cluster_similarity/{cluster}', 'r') as f:
            similarities = f.read().splitlines()
        high_similarities = []
        for similarity in similarities:
            if float(similarity.split()[2]) > 0.9:
                high_similarities.append(similarity)
        with open(f'./high_sim_clusters/{cluster}', 'w') as f:
            for similarity in high_similarities:
                f.write(f"{similarity}\n")

# count the differences between cluster similarity and high cluter similarity
def count_significant_clusters():
    for idx, cluster in enumerate(os.listdir('./cluster_similarity')):
        with open(f'./cluster_similarity/{cluster}', 'r') as f:
            similarities_count = len(f.read().splitlines())
        with open(f'./high_sim_clusters/{cluster}', 'r') as f:
            high_similarities_count = len(f.read().splitlines())
        print(f'cluster {cluster} difference: {(similarities_count - high_similarities_count) / (similarities_count + 1)}')

if __name__ == "__main__":
    # gen_candidates_word_usage()
    # gen_similarity_index()
    # filter_high_similarity()
    # count_unique_candidates()
    # gen_cluster_similarity()
    # gen_high_sim_clusters()
    count_significant_clusters()