import gensim


model = gensim.models.Word2Vec.load("model/word2vec.model")

while True:

    line = input("请输入测试句子:")
    try:
        result = model.most_similar(line)

        for word in result:
            print(word[0], word[1])

    except:
        print('没有匹配到相似的词')
        continue
