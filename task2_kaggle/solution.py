#coding=utf8
PATH_TRAIN = 'input/train.csv'
PATH_TEST = 'input/test.csv'

PATH_PRED = 'pred.csv'


word_stat_dict = {}

fl = open(PATH_TRAIN, 'rt')

fl.readline()

for line in fl:
    Id, Sample, Prediction = line.strip().split(',')
    word1, word2 = Prediction.split(' ')
    for i in range(4, len(word1)+1, 2):
        key = word1[:i]
        if key not in word_stat_dict:
            word_stat_dict[key] = {}
        if word1 not in word_stat_dict[key]:
            word_stat_dict[key][word1] = 0
        word_stat_dict[key][word1] += 1
    for i in range(4, len(word2)+1, 2):
        key = word2[:i]
        if key not in word_stat_dict:
            word_stat_dict[key] = {}
        if word2 not in word_stat_dict[key]:
            word_stat_dict[key][word2] = 0
        word_stat_dict[key][word2] += 1

fl.close()

most_freq_dict = {}

for key in word_stat_dict:
    most_freq_dict[key] = max(word_stat_dict[key], key=word_stat_dict[key].get)


fl = open(PATH_TEST, 'rt')

fl.readline()

out_fl = open(PATH_PRED, 'wt')

out_fl.write('Id,Prediction\n')

for line in fl:
    flag = True
    Id, Sample = line.strip().split(',')
    word1, word2_chunk = Sample.split(' ')
    for i in range(len(word2_chunk), 3, -2):
        key = word2_chunk[:i]
        if key in most_freq_dict:
            flag = False
            out_fl.write('%s,%s %s\n' % (Id, word1, most_freq_dict[key]) )
            break
    if (flag):
        out_fl.write('%s,%s %s\n' % (Id, word1, word2_chunk) )

fl.close()
out_fl.close()
