import json
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
import math

word_dict = defaultdict(lambda: defaultdict(int))
docID_length = defaultdict(int)

def read_json():
    filePath = "WEBPAGES_RAW/bookkeeping.json"
    with open(filePath, "r") as file:
        json_data = json.load(file)
    file.close();
    return json_data

def read_into_dict(weight, token,fileID):
    global word_dict
    lemmatizer = WordNetLemmatizer()
    for word in token:
        try:
            word = lemmatizer.lemmatize(word.lower())
            fileID = str(fileID)
            # word_dict[word][fileID] += 1
            word_dict[word][fileID] += weight
            # weighted_dict[word][fileID] += weight
        except Exception as e:
            print(str(e))
            continue

def word_parser(soup,fileID):

    for e in soup.find_all('br'):
        e.extract()

    for a in soup.find_all('a'):
        a.extract()

    if soup.body != None and soup.body.string !=None:
        body_token = word_tokenize(soup.body.string)
        read_into_dict(1, body_token, fileID)
    if soup.title != None and soup.title.string != None:
        title_token = word_tokenize(soup.title.string)
        read_into_dict(2, title_token, fileID)

    for h1_tag in soup.find_all('h1'):
        if h1_tag.string != None:
            h1_token = word_tokenize(h1_tag.string)
            read_into_dict(7, h1_token, fileID)

    for h2_tag in soup.find_all('h2'):
        if h2_tag.string != None:
            h2_token = word_tokenize(h2_tag.string)
            read_into_dict(5, h2_token, fileID)

    for h3_tag in soup.find_all('h3'):
        if h3_tag.string != None:
            h3_token = word_tokenize(h3_tag.string)
            read_into_dict(3, h3_token, fileID)

    for b_tag in soup.find_all('b'):
        if b_tag.string != None:
            b_token = word_tokenize(b_tag.string)
            read_into_dict(2, b_token, fileID)

    for strong_tag in soup.find_all('strong'):
        if strong_tag.string != None:
            strong_token = word_tokenize(strong_tag.string)
            read_into_dict(2, strong_token, fileID)

    #   additional tags

    for p_tag in soup.find_all('p'):
        if p_tag.text != None:
            p_token = word_tokenize(p_tag.text)
            read_into_dict(1, p_token, fileID)

    for li_tag in soup.find_all('li'):
        if li_tag.string != None:
            li_token = word_tokenize(li_tag.string)
            read_into_dict(1, li_token, fileID)

    for span_tag in soup.find_all('span'):
        if span_tag.string != None:
            span_token = word_tokenize(span_tag.string)
            read_into_dict(1, span_token, fileID)


def tokenizer(docID, url):
    filePath = "".join(("WEBPAGES_RAW/",docID))
    file = open(filePath, encoding="utf-8").read()
    soup = BeautifulSoup(file, "html.parser")
    word_parser(soup, docID)

def sort_by_token(dictTuple):
    return dictTuple[0]

def main():
    global word_dict
    inverted_index = {}

    json_data = read_json()
    count = 1
    for docID, docURL in json_data.items():
        if (docURL.count("http") < 2 and ".." not in docURL and docURL.count("/") < 7):
            tokenizer(docID, docURL)
            print("count = ", count)
            count += 1

    # tokenizer("67/115", "fano.ics.uci.edu/cites/Location/Proc-10th-Genome-Informatics-Worksh.html")


    documentFreq = defaultdict(int)
    idf = defaultdict(int)
    tf_idf = defaultdict(lambda : defaultdict(float))

    tf_length = defaultdict(list)

    for token, doc_freq in word_dict.items():
        documentFreq[token] = len(doc_freq)
        inverse_doc_freq = math.log10(count / len(doc_freq))
        idf[token] = inverse_doc_freq
        for doc, freq in doc_freq.items():
            log_freq_weight = 1 + math.log10(freq)
            weight = log_freq_weight * inverse_doc_freq
            tf_idf[token][doc] = weight
            tf_length[doc].append(weight ** 2)


    doc_analytics = defaultdict(list)

    for docID, all_weights in tf_length.items():
        number_unique_tok = len(all_weights)
        doc_length = math.sqrt(sum(all_weights))
        doc_analytics[docID].append(number_unique_tok)
        doc_analytics[docID].append(doc_length)

    # inverted_index["analysis"]["docID"] = [number_unique_tok, doc_length]
    inverted_index["analysis"] = doc_analytics


    # inverted_index["documentFreq"][token] = number of document have this token
    # inverted_index["documentFreq"] = documentFreq

    # inverted_index["idf"][token] = inverse document frequency
    inverted_index["idf"] = idf

    # inverted_index["tf-idf"}[token] = {docID1: tf_idf1, docID2, tf_idf2}
    inverted_index["tf-idf"] = tf_idf

    # inverted_index["tokenized"]["token"] = {docID1 : Freq1, docID2: Freq2}
    inverted_index["tokenized"] = word_dict

    with open("wordFrequency.txt","w", encoding="utf-8") as file:
        json.dump(inverted_index, file, indent=4)
        print("Success")

    file.close()


if __name__ == "__main__":
    main();