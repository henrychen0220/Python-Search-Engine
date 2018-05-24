import json
import re
from collections import defaultdict
from nltk.stem import WordNetLemmatizer
import math

def read_url():
    filename = "WEBPAGES_RAW/bookkeeping.json"
    with open(filename, "r") as f:
        url_data = json.load(f)
    f.close();
    return url_data

def rank_url(wordList, json_data):


    word_freq = defaultdict(int)
    doc_score_dict = defaultdict(int)
    query_length = 0
    lemmatizer = WordNetLemmatizer()
    for word in wordList:
        word_freq[word] += 1

    normalized_query_dict = defaultdict(int)

    for word, freq in word_freq.items():
        word = lemmatizer.lemmatize(word)
        log_freq_weight = 1 + math.log10(freq)
        try:
            word_weight = log_freq_weight * json_data["idf"][word]
            normalized_query_dict[word] = word_weight
            query_length += (freq ** 2)
        except Exception as e:
            normalized_query_dict[word] = log_freq_weight
            query_length += (freq ** 2)
            #  no such word existing in inverted index
            continue

    #  normalize
    for word, freq in word_freq.items():
        normalized_query_dict[word] = normalized_query_dict[word] * freq / math.sqrt(query_length)

    for word, normalized_query_weight in normalized_query_dict.items():
        word = lemmatizer.lemmatize(word.lower())
        print("After lemmatize, word =", word)
        try:
            for docID, tf_idf in json_data["tf-idf"][word].items():
                if docID in json_data["tokenized"][word]:
                    tf = json_data["tokenized"][word][docID]
                else:
                    tf = 0
                # normalizing

                normalized_doc = tf_idf * tf / math.sqrt(json_data["analysis"][docID][0])

                # cosine similarity
                doc_score_dict[docID] += normalized_query_weight * normalized_doc


        except Exception as e:
            #  when a word isn't available in the index
            continue
    # print("Finished calculating scores\n")
    return doc_score_dict

def print_url(score_dict, json_data):
    url_data = read_url()
    final_list = []
    count = 1

    print("Total parsed", len(json_data["analysis"]), " documents")
    print("Total got", len(json_data["idf"]) , " unique tokens")
    print("Total got", len(json_data["tf-idf"]) , " unique tokens")
    print("Top 10 documents: ")
    for docID, score in sorted(score_dict.items(), key=lambda x : -x[1]):
        url = url_data[docID]
        if url.count("http") < 2 and url.count("..") == 0:
            print("     ",count, ",", docID)
            print("         normalized tf-idf =", score)
            print("         # of unique tokens =", json_data["analysis"][docID][1])
            print("         url = ",url)
            final_list.append(url)
            count += 1
        if count == 11:
            break
    print("Found", len(final_list), " urls in total")

    if len(final_list) == 0:
        print("No URL Found")
    print("DONE!")
    return

def main():
    with open("wordFrequency.txt", "r") as file:
        json_data = json.load(file)
    file.close()
    searchQuery = input("Enter a word to search: ")
    wordList = re.split(r'[^A-Za-z0-9]', searchQuery)
    selected_dict = rank_url(wordList, json_data);
    print_url(selected_dict, json_data);

if __name__ == "__main__":
    main();
