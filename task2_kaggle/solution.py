#coding=utf8
PATH_TRAIN = 'input/train.csv'
PATH_TEST = 'input/test.csv'

PATH_PRED = 'pred.csv'


word_stat_dict = {}
word_stat_dict_last = {}

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
    for i in range(2, len(word1)+1, 2):
        last = word1[-i:]
        if last not in word_stat_dict_last:
            word_stat_dict_last[last] = {}
        for j in range(4, len(word2)+1, 2):
            key = word2[:j]
            if key not in word_stat_dict_last[last]:
                word_stat_dict_last[last][key] = {}
            if word2 not in word_stat_dict_last[last][key]:
                word_stat_dict_last[last][key][word2] = 0
            word_stat_dict_last[last][key][word2] += 1

fl.close()

most_freq_dict = {}
most_freq_dict_last = {}

for key in word_stat_dict:
    most_freq_dict[key] = max(word_stat_dict[key], key=word_stat_dict[key].get)
for last in word_stat_dict_last:
    most_freq_dict_last[last] = {}
    for key in word_stat_dict_last[last]:
        most_freq_dict_last[last][key] = max(word_stat_dict_last[last][key], key=word_stat_dict_last[last][key].get)


fl = open(PATH_TEST, 'rt')

fl.readline()

out_fl = open(PATH_PRED, 'wt')

out_fl.write('Id,Prediction\n')

for line in fl:
    Id, Sample = line.strip().split(',')
    word1, word2_chunk = Sample.split(' ')
    
    max_word2_chars = 0
    max_word2 = word2_chunk
    
    for i in range(2, len(word1)+1, 2):
        last = word1[-i:]
        if last in most_freq_dict_last:
            for j in range(len(word2_chunk), 3, -2):
                key = word2_chunk[:j]
                if key in most_freq_dict_last[last]:
                    if j >= max_word2_chars:
                        max_word2_chars = j
                        max_word2 = most_freq_dict_last[last][key]
                    break
    if max_word2_chars == 0:
        for j in range(len(word2_chunk), 3, -2):
            key = word2_chunk[:j]
            if key in most_freq_dict:
                max_word2_chars = j
                max_word2 = most_freq_dict[key]
                break
    out_fl.write('%s,%s %s\n' % (Id, word1, max_word2) )

fl.close()
out_fl.close()
