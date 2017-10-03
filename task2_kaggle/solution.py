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
    key = word1[:4]
    if key not in word_stat_dict:
        word_stat_dict[key] = {}
    if word1 not in word_stat_dict[key]:
        word_stat_dict[key][word1] = 0
    word_stat_dict[key][word1] += 1
    key = word2[:4]
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
    Id, Sample = line.strip().split(',')
    word1, word2_chunk = Sample.split(' ')
    key = word2_chunk[:4]
    if key in most_freq_dict:
        out_fl.write('%s,%s %s\n' % (Id, word1, most_freq_dict[key]) )
    else:
        out_fl.write('%s,%s %s\n' % (Id, word1, word2_chunk) )

fl.close()
out_fl.close()
