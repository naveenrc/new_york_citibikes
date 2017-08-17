# Multilayer Perceptron
import numpy
import math
from keras.models import Sequential
from keras.layers import Dense

# fix random seed for reproducibility
numpy.random.seed(7)


def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back - 1):
        a = dataset[i:(i + look_back)]
        dataX.append(a)
        dataY.append(dataset[i + look_back])
    return numpy.array(dataX), numpy.array(dataY)


def model_base(dataset, idx, first_layer, sec_layer, epochs, look_back = 1):
    train, test = dataset[0:idx], dataset[idx:]
    print(len(train), len(test))
    # convert an array of values into a dataset matrix
    # reshape into X=t and Y=t+1
    trainX, trainY = create_dataset(train, look_back)
    testX, testY = create_dataset(test, look_back)

    # create and fit Multilayer Perceptron model
    model = Sequential()
    model.add(Dense(first_layer, input_dim=look_back, activation='relu'))
    model.add(Dense(sec_layer, activation='relu'))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, epochs=epochs, batch_size=2, verbose=2)
    # Estimate model performance
    trainScore = model.evaluate(trainX, trainY, verbose=0)
    print('Train Score: %.2f MSE (%.2f RMSE)' % (trainScore, math.sqrt(trainScore)))
    testScore = model.evaluate(testX, testY, verbose=0)
    print('Test Score: %.2f MSE (%.2f RMSE)' % (testScore, math.sqrt(testScore)))
    # generate predictions for training
    trainPredict = model.predict(trainX)
    testPredict = model.predict(testX)
    # shift train predictions for plotting
    trainPredictPlot = numpy.empty_like(dataset)
    trainPredictPlot[:] = numpy.nan
    trainPredictPlot = trainPredict
    # shift test predictions for plotting
    testPredictPlot = numpy.empty_like(dataset)
    testPredictPlot[:] = numpy.nan
    testPredictPlot[idx + look_back:len(dataset) - 1] = testPredict[:, 0]

    return trainPredictPlot, testPredictPlot