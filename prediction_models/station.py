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
trans = data[data['station'] == int(input('Enter station number: '))]['count']
series = trans.resample('360Min').sum()
series.fillna(0, inplace=True)
dataset = series.values

# test data size
test_split = -1642
# window size to take into account for predicting next step
look_back = 8
# neural network 2 layers size
first_layer = 14
sec_layer = 8
# iterations
epochs = 14

train_predict, test_predict = model_base(dataset, test_split, first_layer, sec_layer, epochs, look_back=look_back)

plt.plot(dataset, label='Actual')
plt.plot(train_predict, label='Train prediction')
plt.plot(test_predict, label='Test prediction')
plt.legend(loc='upper left')
plt.title('Train and test prediction')
plt.xlabel('6 hour periods')
plt.ylabel('Transportation needed')
plt.show()

ratios = numpy.divide(dataset, test_predict)
plt.plot(ratios)
plt.title('Ratio between actual and test predictions')
plt.show()

ratios = numpy.array([value for value in ratios if not math.isnan(value)])
ci = [0, 4.0]
acc = numpy.where((ratios >= ci[0]) & (ratios <= ci[1]))
accuracy = len(acc[0])/len(ratios) * 100
plt.hist(ratios, bins=20, rwidth=0.5, log=True)
plt.title('Confidence interval:[{0:f},{1:f}], Accuracy: {2:f}'.format(ci[0], ci[1], accuracy))
plt.xlabel('Ratio between actual and test predictions')
plt.ylabel('Frequency')
plt.show()
