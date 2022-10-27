from river import linear_model
from river import metrics
from river import compose
from river import preprocessing
from river import optim
import os
import pickle

SAVE_MODEL_FREQUENCY = 50

class Iml:

    def __init__(self):
        self.model = compose.Pipeline(
            ('cat_scale', compose.SelectType(str) | preprocessing.OneHotEncoder()),
            ('scale', compose.SelectType(int,float) |   preprocessing.StandardScaler()),
            ('log_reg', linear_model.LinearRegression(optimizer=optim.SGD(0.05)))
        )
        self.modelName = 'model.plk'
        self.metricMAE = metrics.MAE()
        self.metricRMSE = metrics.RMSE()
        self.metricR2 = metrics.R2()
        # save every counter interations
        self.counter = SAVE_MODEL_FREQUENCY

    def learn(self, entryData, targetData):
        x, y = entryData, targetData
        self.model.learn_one(x, y)
        y_pred = self.model.predict_one(x)

        self.metricMAE.update(y, y_pred)
        self.metricRMSE.update(y, y_pred)
        self.metricR2.update(y, y_pred)

        self.counter -= 1
        if (self.counter <= 0):
            print("\nINFO: Saving Model...\n")
            self.counter = SAVE_MODEL_FREQUENCY
            self.save_model()

        return True
    
    def printMetrics(self):
        print("MAE: " + str(self.metricMAE.get()))
        print("RMSE: " + str(self.metricRMSE.get()))
        print("R2: " + str(self.metricR2.get()))

    def prediction(self, entryData): 
        return self.model.predict_one(entryData)

    def save_model(self):
        # by writing to tmp file operation becames atomic
        tmp = "tmp.plk"
        with open(tmp, 'wb') as f:
            pickle.dump(self,f)
        os.replace(tmp, self.modelName)

    def load_model(self):
        with open(self.modelName, 'rb') as f:
            return pickle.load(f)

def parse_response_data(inputData):
    inputData = inputData[2:]
    inputData = inputData[:-3]
    data_lst = inputData.split(",")

    data = {
        "age":int(data_lst[0]),
        "sex":data_lst[1],
        "bmi":float(data_lst[2]),
        "children":int(data_lst[3]),
        "smoker":data_lst[4],
        "region":data_lst[5]
    }

    # target are the charges int and float due to logistic regression
    return {"data": data, "target": float(data_lst[6])}