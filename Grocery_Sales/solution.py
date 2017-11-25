import numpy
import pandas
import sklearn.ensemble
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error


train = pandas.read_csv('Train.csv')

train = train.replace(numpy.nan, -999)

COLUMNS = ['street_id', 'build_tech', 'floor', 'area', 'rooms', 'balcon', 'metro_dist', 'g_lift',  'kw1', 'kw2', 'kw3', 'kw4', 'kw5', 'kw6', 'kw7', 'kw8', 'kw9', 'kw10', 'kw11', 'kw12', 'kw13']

y = train['price'].values
X = train[COLUMNS].values

kf = KFold(n_splits=2)
for train_index, test_index in kf.split(X):
    Xtr = X[train_index]
    ytr = y[train_index]
    Xts = X[test_index]
    yts = y[test_index]

    #mdl = sklearn.ensemble.RandomForestRegressor()
    mdl = sklearn.ensemble.GradientBoostingRegressor(n_estimators=300, max_depth=5)

    mdl.fit(Xtr, ytr)

    preds = mdl.predict(Xts)

    print(mean_absolute_error(yts, preds))

