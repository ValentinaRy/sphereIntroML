import numpy
import pandas
import sklearn.ensemble
import time

train = pandas.read_csv('data/train.csv')

train = train.replace(numpy.nan, False)
train = train[(6 <= pandas.to_datetime(train['date']).dt.month) & (pandas.to_datetime(train['date']).dt.month <= 10)]
print("train")

holidays = pandas.read_csv('data/holidays_events.csv')
stores = pandas.read_csv('data/stores.csv')
cities = {el:i for i, el in enumerate(set(stores['city'].values))}
states = {el:i for i, el in enumerate(set(stores['state'].values))}
store_city = {el[0]:cities[el[1]] for el in stores.values}
city_state = {cities[el[1]]:states[el[2]] for el in stores.values}
types = {'Holiday':0, 'Event':1,'Additional':2,'Transfer':3,'Bridge':4,'Work Day':5}
locales = {'National':0, 'Regional':1, 'Local':2}
holdict = {el[0]:(types[el[1]],locales[el[2]],el[3],el[5]) for el in holidays.values}
is_holiday = []
for el in train.values:
    cur = holdict.get(el[1], (5,))
    if cur[0] != types['Work Day'] and not cur[3]:
        city = store_city.get(el[2], 0)
        place = cur[2]
        if cur[1] == locales['National'] \
        or cur[1] == locales['Regional'] and city_state[city] == states[place] \
        or cur[1] == locales['Local'] and city == cities[place]:
            is_holiday.append(True)
        else:
            is_holiday.append(False)
    elif not numpy.is_busday(el[1]):
        is_holiday.append(True)
    else:
        is_holiday.append(False)
train['is_holiday'] = is_holiday
print("holidays")

items = pandas.read_csv('data/items.csv')
families = {el:i for i, el in enumerate(items['family'].values)}
class_family = {c:families[f] for f,c in items[['family', 'class']].values}
itemnbr_class = {n:c for n,c in items[['item_nbr', 'class']].values}
itemnbr_perishable = {n:(c == 1) for n,c in items[['item_nbr', 'perishable']].values}
item_class = [itemnbr_class[n] for n in train['item_nbr'].values]
item_family = [class_family[n] for n in item_class]
item_perishable = [itemnbr_perishable[n] for n in train['item_nbr'].values]
train['item_class'] = item_class
train['item_family'] = item_family
train['item_perishable'] = item_perishable

train['is_AUTOMOTIVE'] = train['item_family'] == families['AUTOMOTIVE']
train['is_BABY_CARE'] = train['item_family'] == families['BABY CARE']
train['is_BEAUTY'] = train['item_family'] == families['BEAUTY']
train['is_BEVERAGES'] = train['item_family'] == families['BEVERAGES']
train['is_BOOKS'] = train['item_family'] == families['BOOKS']
train['is_BREAD_BAKERY'] = train['item_family'] == families['BREAD/BAKERY']
train['is_CELEBRATION'] = train['item_family'] == families['CELEBRATION']
train['is_CLEANING'] = train['item_family'] == families['CLEANING']
train['is_DAIRY'] = train['item_family'] == families['DAIRY']
train['is_DELI'] = train['item_family'] == families['DELI']
train['is_EGGS'] = train['item_family'] == families['EGGS']
train['is_FROZEN_FOODS'] = train['item_family'] == families['FROZEN FOODS']
train['is_GROCERY_I'] = train['item_family'] == families['GROCERY I']
train['is_GROCERY_II'] = train['item_family'] == families['GROCERY II']
train['is_HARDWARE'] = train['item_family'] == families['HARDWARE']
train['is_HOME_AND_KITCHEN_I'] = train['item_family'] == families['HOME AND KITCHEN I']
train['is_HOME_AND_KITCHEN_II'] = train['item_family'] == families['HOME AND KITCHEN II']
train['is_HOME_APPLIANCES'] = train['item_family'] == families['HOME APPLIANCES']
train['is_HOME_CARE'] = train['item_family'] == families['HOME CARE']
train['is_LADIESWEAR'] = train['item_family'] == families['LADIESWEAR']
train['is_LAWN_AND_GARDEN'] = train['item_family'] == families['LAWN AND GARDEN']
train['is_LINGERIE'] = train['item_family'] == families['LINGERIE']
train['is_LIQUOR_WINE_BEER'] = train['item_family'] == families['LIQUOR,WINE,BEER']
train['is_MAGAZINES'] = train['item_family'] == families['MAGAZINES']
train['is_MEATS'] = train['item_family'] == families['MEATS']
train['is_PERSONAL_CARE'] = train['item_family'] == families['PERSONAL CARE']
train['is_PET_SUPPLIES'] = train['item_family'] == families['PET SUPPLIES']
train['is_PLAYERS_AND_ELECTRONICS'] = train['item_family'] == families['PLAYERS AND ELECTRONICS']
train['is_POULTRY'] = train['item_family'] == families['POULTRY']
train['is_PREPARED_FOODS'] = train['item_family'] == families['PREPARED FOODS']
train['is_PRODUCE'] = train['item_family'] == families['PRODUCE']
train['is_SCHOOL_AND_OFFICE_SUPPLIES'] = train['item_family'] == families['SCHOOL AND OFFICE SUPPLIES']
train['is_SEAFOOD'] = train['item_family'] == families['SEAFOOD']
print("items")

oil = pandas.read_csv('data/oil.csv')
oil.set_index('date',drop=True,inplace=True)
oil.index = pandas.DatetimeIndex(oil.index)
oil = oil.reindex(pandas.date_range("2013-01-01", "2017-08-31"), fill_value=numpy.nan)
oil['date'] = pandas.DatetimeIndex(oil.index)
oil['dcoilwtico'] = oil['dcoilwtico'].fillna(method='bfill')
date_oil = {d.strftime('%Y-%m-%d'):p for d,p in oil[['date', 'dcoilwtico']].values}
oil_prices = [date_oil[d] for d in train['date'].values]
train['oil_prices'] = oil_prices
print("oil")

test = pandas.read_csv('data/test.csv')
is_holiday = []
for el in test.values:
    cur = holdict.get(el[1], (5,))
    if cur[0] != types['Work Day'] and not cur[3]:
        city = store_city.get(el[2], 0)
        place = cur[2]
        if cur[1] == locales['National'] \
        or cur[1] == locales['Regional'] and city_state[city] == states[place] \
        or cur[1] == locales['Local'] and city == cities[place]:
            is_holiday.append(True)
        else:
            is_holiday.append(False)
    elif not numpy.is_busday(el[1]):
        is_holiday.append(True)
    else:
        is_holiday.append(False)
test['is_holiday'] = is_holiday

item_class = [itemnbr_class[n] for n in test['item_nbr'].values]
item_family = [class_family[n] for n in item_class]
item_perishable = [itemnbr_perishable[n] for n in test['item_nbr'].values]
test['item_class'] = item_class
test['item_family'] = item_family
test['item_perishable'] = item_perishable

test['is_AUTOMOTIVE'] = test['item_family'] == families['AUTOMOTIVE']
test['is_BABY_CARE'] = test['item_family'] == families['BABY CARE']
test['is_BEAUTY'] = test['item_family'] == families['BEAUTY']
test['is_BEVERAGES'] = test['item_family'] == families['BEVERAGES']
test['is_BOOKS'] = test['item_family'] == families['BOOKS']
test['is_BREAD_BAKERY'] = test['item_family'] == families['BREAD/BAKERY']
test['is_CELEBRATION'] = test['item_family'] == families['CELEBRATION']
test['is_CLEANING'] = test['item_family'] == families['CLEANING']
test['is_DAIRY'] = test['item_family'] == families['DAIRY']
test['is_DELI'] = test['item_family'] == families['DELI']
test['is_EGGS'] = test['item_family'] == families['EGGS']
test['is_FROZEN_FOODS'] = test['item_family'] == families['FROZEN FOODS']
test['is_GROCERY_I'] = test['item_family'] == families['GROCERY I']
test['is_GROCERY_II'] = test['item_family'] == families['GROCERY II']
test['is_HARDWARE'] = test['item_family'] == families['HARDWARE']
test['is_HOME_AND_KITCHEN_I'] = test['item_family'] == families['HOME AND KITCHEN I']
test['is_HOME_AND_KITCHEN_II'] = test['item_family'] == families['HOME AND KITCHEN II']
test['is_HOME_APPLIANCES'] = test['item_family'] == families['HOME APPLIANCES']
test['is_HOME_CARE'] = test['item_family'] == families['HOME CARE']
test['is_LADIESWEAR'] = test['item_family'] == families['LADIESWEAR']
test['is_LAWN_AND_GARDEN'] = test['item_family'] == families['LAWN AND GARDEN']
test['is_LINGERIE'] = test['item_family'] == families['LINGERIE']
test['is_LIQUOR_WINE_BEER'] = test['item_family'] == families['LIQUOR,WINE,BEER']
test['is_MAGAZINES'] = test['item_family'] == families['MAGAZINES']
test['is_MEATS'] = test['item_family'] == families['MEATS']
test['is_PERSONAL_CARE'] = test['item_family'] == families['PERSONAL CARE']
test['is_PET_SUPPLIES'] = test['item_family'] == families['PET SUPPLIES']
test['is_PLAYERS_AND_ELECTRONICS'] = test['item_family'] == families['PLAYERS AND ELECTRONICS']
test['is_POULTRY'] = test['item_family'] == families['POULTRY']
test['is_PREPARED_FOODS'] = test['item_family'] == families['PREPARED FOODS']
test['is_PRODUCE'] = test['item_family'] == families['PRODUCE']
test['is_SCHOOL_AND_OFFICE_SUPPLIES'] = test['item_family'] == families['SCHOOL AND OFFICE SUPPLIES']
test['is_SEAFOOD'] = test['item_family'] == families['SEAFOOD']

oil_prices = [date_oil[d] for d in test['date'].values]
test['oil_prices'] = oil_prices
print("test")

COLUMNS = ['onpromotion', 'is_holiday', 'item_perishable', 'oil_prices', 'is_AUTOMOTIVE', 'is_BABY_CARE', 'is_BEAUTY', 'is_BEVERAGES', 'is_BOOKS', 'is_BREAD_BAKERY', 'is_CELEBRATION', 'is_CLEANING', 'is_DAIRY', 'is_DELI', 'is_EGGS', 'is_FROZEN_FOODS', 'is_GROCERY_I', 'is_GROCERY_II', 'is_HARDWARE', 'is_HOME_AND_KITCHEN_I', 'is_HOME_AND_KITCHEN_II', 'is_HOME_APPLIANCES', 'is_HOME_CARE', 'is_LADIESWEAR', 'is_LAWN_AND_GARDEN', 'is_LINGERIE', 'is_LIQUOR_WINE_BEER', 'is_MAGAZINES', 'is_MEATS', 'is_PERSONAL_CARE', 'is_PET_SUPPLIES', 'is_PLAYERS_AND_ELECTRONICS', 'is_POULTRY', 'is_PREPARED_FOODS', 'is_PRODUCE', 'is_SCHOOL_AND_OFFICE_SUPPLIES', 'is_SEAFOOD']

Xtr = train[COLUMNS].values
ytr = train['unit_sales'].values
Xts = test[COLUMNS].values
print("start learning and predicting")

mdl = sklearn.ensemble.RandomForestRegressor()
mdl.fit(Xtr, ytr)
preds = mdl.predict(Xts)
print("finish learning and predicting")

res = open('predictions.csv', 'w')
res.write("id,unit_sales\n")
for i in range(len(preds)):
    res.write(str(test['id'].values[i])+","+str(preds[i])+"\n")
res.close()
print("all have done")
