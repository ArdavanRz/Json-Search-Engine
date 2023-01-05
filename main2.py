from __future__ import unicode_literals

import math

# import hazm
from parsivar import *
import json as js

jfile = open('IR_data_news_12k.json')
docs = js.load(jfile)




custom_normalizer = Normalizer()
custom_tokenizer = Tokenizer()
custom_stemmer = FindStems()

def tfidf(term, document):
    if ((not frequencies.keys().__contains__(term)) or frequencies[term][document] == 0) or ((not terms_doc_frequency.keys().__contains__(term)) or terms_doc_frequency[term] == 0):
        return 0
    return (1 + math.log(frequencies[term][document], 10)) * (math.log(processed_words_array.__len__() / terms_doc_frequency[term], 10))


def query():
    string_test = input()
    # print("your test")
    input_query = pre(string_test)
    for indexed_word in input_query:
        for x in range(processed_words_array.__len__()):
            for y in range(processed_words_array[x].__len__()):
                queried_word = processed_words_array[x][y]
                # print(queried_word)
                if queried_word == indexed_word:
                    # positional_index[queried_word][x].append(y)
                    if not frequencies.keys().__contains__(indexed_word):
                        frequencies[indexed_word] = {}
                        table[indexed_word] = {}
                        terms_doc_frequency[indexed_word] = 0
                        for i in range(processed_words_array.__len__()):
                            frequencies[indexed_word][i] = 0
                            table[indexed_word][i] = 0
                    frequencies[indexed_word][x] += 1
            if frequencies.keys().__contains__(indexed_word) and frequencies[indexed_word][x] > 0:
                terms_doc_frequency[indexed_word] += 1
                # for index elimination, we save all the document ids that have non-zero scores
                non_zero_docs.append(x)
            if not table.keys().__contains__(indexed_word):
                table[indexed_word] = {}
            table[indexed_word][x] = tfidf(indexed_word, x)
    query_vector = [1] * input_query.__len__()
    for valid_doc_id in non_zero_docs:
        cosine_results[valid_doc_id] = cosine(query_vector, document_vector(valid_doc_id))

    # print(positional_index)
    printed_documents = []
    print('results:')
    for x in range(5):
        best_result = (-1, -1)
        for doc_id in non_zero_docs:
            doc_score = (doc_id, cosine_results[doc_id])
            if doc_score[1] > best_result[1] and (not printed_documents.__contains__(doc_score[0])):
                best_result = doc_score
        print(titles[best_result[0]])
        printed_documents.append(best_result[0])


######################################################
def pre(input_text):
    processed_words = []
    normalized = custom_normalizer.normalize(input_text)
    tokenized = custom_tokenizer.tokenize_words(normalized)

    for x in range(tokenized.__len__()):
        tokenized[x] = custom_stemmer.convert_to_stem(tokenized[x])
        # if not hazm.stopwords_list().__contains__(tokenized[x]):
        processed_words.append(tokenized[x])
    return processed_words


def cosine(a, b):
    # if a.__len__() != b.__len__():
    #     print("The size of the vectors are not the same")
    #     return
    fraction_top = len_a = len_b = 0
    for i in range(a.__len__()):
        fraction_top += a[i] * b[i]
        len_a += a[i] * a[i]
        len_b += b[i] * b[i]
    if len_a * len_b == 0:
        return -1
    return fraction_top / (math.sqrt(len_a) * math.sqrt(len_b))


def distance(a, b):
    output = 0
    for i in a.__len__():
        output += math.pow(a[i] - b[i], 2)
    return math.sqrt(output)


def count_to_tfidf(f, n):
    output = [0] * f.__len__()
    N = processed_words_array.__len__()
    for i in range(output.__len__()):
        output[i] = (1 + math.log(f[i], 10)) * (math.log(N / n[i]))
    return output


def document_score(doc_id):
    output = 0.0
    for i in range(table.__len__()):
        output += table[i][doc_id]
    return output


def vector_score(vector):
    output = 0.0
    for i in range(vector.__len__()):
        output += vector[i]
    return output


def document_vector(doc_id):
    output = []
    for w in table.keys():
        output.append(table[w][doc_id])
    return output





######################################################

######################################################



######################################################


if __name__ == '__main__':
    contents = []
    titles = []
    frequencies = {}
    terms_doc_frequency = {}
    table = {}
    non_zero_docs = []
    cosine_results = {}

    processed_words_array = []
    for x in range(12000):
        contents.append(docs[str(x)]['content'])
        titles.append(docs[str(x)]['title'])

    for x in range(12000):
        processed_words_array.append(pre(contents[x]))
        print(str(x))

    query()

