# 中文word2vector词向量实现

说明：[word2vector](https://code.google.com/p/word2vec/)背后的原理暂时不做深究，
主要目的就是尽可能快的训练一个中文词向量模型。


# 环境
笔记本 i5-4210M CPU @ 2.60GHz × 4 , 8G RAM
- ubuntu16.04lts 独立系统, 
- python 3.6.1
- 依赖：numpy, scipy, gensim, opencc, jieba


# 1.获取语料库

# 1.1维基百科   https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2
原始语料文件：`zhwiki-latest-pages-articles.xml.bz2` 1.6G

# 1.2 SogouCA 全网新闻数据(SogouCA) http://www.sogou.com/labs/resource/ca.php 
原始语料文件：'news_tensite_xml.full.tar.gz' 746.3 M 



# 2.语料库预处理

# 2.1 搜狗新闻语料处理
来自若干新闻站点2012年6月—7月期间国内，国际，体育，社会，娱乐等18个频道的新闻数据，提供URL和正文信息
格式说明：
数据格式为
<doc>
<url>页面URL</url>
<docno>页面ID</docno>
<contenttitle>页面标题</contenttitle>
<content>页面内容</content>
</doc>
注意：content字段去除了HTML标签，保存的是新闻正文文本

刚下下来的语料是用gbk编码的，在mac或linux上都会呈乱码形式，需要将之转换为utf-8编码。而且我们只需要<content>里面的内容。因此先转换编码和获取content内容

cat news_tensite_xml.dat | iconv -f gbk -t utf-8 -c | grep "<content>"  > corpus.sogou.txt

生成 corpus.sogou.txt 1.9G
分词-用空格隔开 用时40分钟

python3 sogou_corpus_seg.py data/corpus.sogou.txt data/corpus_sogou_seg.txt

生成 corpus_sogou_seg.txt 2.2G


# 2.2 维基百科语料处理

-gensim解析bz2语料
 
python3 parse_wiki_xml2txt.py data/zhwiki-latest-pages-articles.xml.bz2 data/corpus.zhwiki.txt
 
生成 `corpus.zhwiki.txt` 1.1G 用时40分钟
 
- 简繁体转换(opencc)
 把语料中的繁体转换成简体 
 用时1分钟

sudo apt-get install opencc
opencc -i data/corpus.zhwiki.txt -o data/corpus.zhwiki.simplified.txt -c zht2zhs.ini


- 去除英文和空格
文档中还是有很多英文的，一般是文章的reference。里面还有些日文,罗马文等，这些对模型影响效果可以忽略，
只是简单的去除了空格和英文。用时1分钟

python3 remove_en_blank.py data/corpus.zhwiki.simplified.txt data/corpus.zhwiki.simplified.done.txt 

生成 corpus.zhwiki.simplified.done.txt （937.7M）

- 分词
这里以空格做分割符  `-d ' '` 


pip install jieba
python3 -m jieba -d ' ' data/corpus.zhwiki.simplified.done.txt > data/corpus_zhwiki_seg.txt


生成 `corpus.zhwiki.seg.txt` 1.1G 用时30分钟



# 2.3 将百科数据和搜狗数据和并到一个文件
用时2分钟
cat data/corpus_zhwiki_seg.txt data/corpus_sogou_seg.txt > data/corpus_seg.txt


# 3训练
python3 train_word2vec_model.py data/corpus_seg.txt model/word2vec.model model/corpus.vector

详细api参考：http://radimrehurek.com/gensim/models/word2vec.html

生成 word2vec.model 56M corpus.vector 4.1G 用时100分钟

# 4使用

python3 word2vec_test.py



### 参考与致谢

1. https://code.google.com/archive/p/word2vec/
2. https://github.com/piskvorky/gensim
3. http://radimrehurek.com/gensim/models/word2vec.html
4. https://github.com/fxsjy/jieba
5. https://code.google.com/archive/p/opencc/wikis/Introduction.wiki
6. http://licstar.net/archives/262
7. http://www.52nlp.cn/
8. https://github.com/zishuaiz/ChineseWord2Vec

# inmport gensim 出现 ModuleNotFoundError: No module named '_bz2'
# 解决方法

1、on Ubuntu/Debian:

sudo apt-get install libbz2-dev

Fedora:

sudo yum install bzip2-devel

2、重新编译python3

./configure
make
sudo make install

# 待优化
1、增量训练，
2、训练时数据按行喂给模型，避免内存占用过大

