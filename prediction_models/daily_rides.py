import numpy
import pylab as plt
import pandas
import os
import math
from model import model_base

cwd = os.getcwd()
data = pandas.read_csv(os.path.join('../data/rides/')+'rides_count.csv', usecols=[0, 1, 2, 3],
                       parse_dates=[0], infer_datetime_format=True, index_col=0)
data = data.groupby(data.index).agg('sum')
data['total'] = data['un_rides']+data['male_rides']+data['female_rides']
data.index.names = ['Date']
series = data['total']
dataset = series.values

# test data size
test_split = -400
# window size to take into account for predicting next step
look_back = 3
# neural network 2 layers size
first_layer = 12
sec_layer = 8
# iterations
epochs = 12

train_predict, test_predict = model_base(dataset, test_split, first_layer, sec_layer, epochs, look_back=look_back)

plt.plot(dataset, label='Actual')
plt.plot(train_predict, label='Train prediction')
plt.plot(test_predict, label='Test prediction')
plt.legend(loc='upper left')
plt.title('Train and test prediction')
plt.xlabel('Day')
plt.ylabel('Rides')
plt.show()

ratios = numpy.divide(dataset, test_predict)
plt.plot(ratios)
plt.title('Ratio between actual and test predictions')
plt.show()

ratios = numpy.array([value for value in ratios if not math.isnan(value)])
se = numpy.std(ratios)
ci = numpy.percentile(ratios, [34, 68])
acc = numpy.where((ratios>=ci[0]) & (ratios<=ci[1]))
accuracy = len(acc[0])/len(ratios) * 100
plt.hist(ratios, bins=20, rwidth=0.5)
plt.title('Standard deviation: ' + str(se) +', Confidence interval:' + str(ci) + ', Accuracy:' + str(accuracy))
plt.xlabel('Ratio between actual and test predictions')
plt.ylabel('Frequency')
plt.show()

ci = [0.7, 1.4]
acc = numpy.where((ratios>=ci[0]) & (ratios<=ci[1]))
accuracy = len(acc[0])/len(ratios) * 100
plt.hist(ratios, bins=20, rwidth=0.5)
plt.title('Standard deviation: ' + str(se) +', Confidence interval:' + str(ci) + ', Accuracy:' + str(accuracy))
plt.xlabel('Ratio between actual and test predictions')
plt.ylabel('Frequency')
plt.show()
