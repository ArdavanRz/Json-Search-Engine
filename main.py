from __future__ import unicode_literals

import hazm
from parsivar import *
import json as js

jfile = open('IR_data_news_12k.json')
docs = js.load(jfile)




def query():
    string_test = input()
    # print("your test")
    input_query = pre(string_test)
    for indexed_word in input_query:
        positional_index[indexed_word] = {}
        for x in range(processed_words_array.__len__()):
            positional_index[indexed_word][x] = []
            for y in range(processed_words_array[x].__len__()):
                queried_word = processed_words_array[x][y]
                # print(queried_word)
                if queried_word == indexed_word:
                    positional_index[queried_word][x].append(y)

    print(positional_index)
    printed_documents = []
    print('results:')
    for x in range(5):
        best_result = (-1, -1)
        for doc_id in range(processed_words_array.__len__()):
            doc_score = (doc_id, 0)
            for searched_word in input_query:
                doc_score = (doc_id, (positional_index[searched_word][doc_id]).__len__() + doc_score[1])
                print(doc_score)
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
        if not hazm.stopwords_list().__contains__(tokenized[x]):
            processed_words.append(tokenized[x])
    return processed_words






if __name__ == '__main__':
    contents = []
    titles = []
    positional_index = {}

    custom_normalizer = Normalizer()
    custom_tokenizer = Tokenizer()
    custom_stemmer = FindStems()

    processed_words_array = []
    for x in range(100):
        contents.append(docs[str(x)]['content'])
        titles.append(docs[str(x)]['title'])

    for x in range(100):
        processed_words_array.append(pre(contents[x]))
        print(str(x))

    query()
