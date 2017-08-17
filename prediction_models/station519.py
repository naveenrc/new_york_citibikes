import numpy
import pylab as plt
import pandas
import os
import math
from model import model_base

cwd = os.getcwd()
data = pandas.read_csv(os.path.join('../data/rides/')+'transported_hour_data.csv', usecols=[0, 1, 2],
                       parse_dates=[1], infer_datetime_format=True, index_col=1)
data.index.names = ['Date']
trans519 = data[data['station'] == 519]['count']
series = trans519.resample('240Min').sum()
series.fillna(0, inplace=True)
dataset = series.values

test_split = -72
look_back = 6
first_layer = 12
sec_layer = 8
epochs = 7

train_predict, test_predict = model_base(dataset, test_split, first_layer, sec_layer, epochs, look_back)

plt.plot(dataset, label='Actual')
plt.plot(train_predict, label='Train prediction')
plt.plot(test_predict, label='Test prediction')
plt.legend(loc='upper left')
plt.title('Train and test prediction')
plt.xlabel('4 hour periods')
plt.ylabel('Transportation needed')
plt.show()

ratios = numpy.divide(dataset, test_predict)
plt.plot(ratios)
plt.title('Ratio between actual and test predictions')
plt.show()

ratios = numpy.array([value for value in ratios if not math.isnan(value)])
se = numpy.std(ratios)
ci = numpy.percentile(ratios, [70, 90])
acc = numpy.where((ratios >= ci[0]) & (ratios <= ci[1]))
accuracy = len(acc[0])/len(ratios) * 100
plt.hist(ratios, bins=20)
plt.title('Confidence interval:[{0:f},{1:f}], Accuracy: {2:f}'.format(ci[0], ci[1], accuracy))
plt.xlabel('Ratio between actual and test predictions')
plt.ylabel('Frequency')
plt.show()
