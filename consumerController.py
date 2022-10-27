import kafkaConsumer as kafka
import iml
import signal
from executeCmd import execute_cmd

KAFKA_TOPIC = "trainer"
KAFKA_PREDICTION_TOPIC = "analyzer"
KAFKA_ADDR = "localhost"
KAFKA_PARTITIONS = "1"
KAFKA_REPLICATION = "1"

def init():
    # Create Learn Data Topic
    kafka.create_topic(KAFKA_ADDR, KAFKA_REPLICATION, KAFKA_PARTITIONS, KAFKA_TOPIC)
    # Create Prediction Data Request Topic
    kafka.create_topic(KAFKA_ADDR, KAFKA_REPLICATION, KAFKA_PARTITIONS, KAFKA_PREDICTION_TOPIC)
    # Init Model
    global learner 
    learner = iml.Iml()
    print('INFO: Init Data Topic and Model Sucess')
    return True

def clean():
    # Delete Learn Data Topic
    print("INFO: Deleting " + KAFKA_TOPIC + " topic...")
    kafka.delete_topic(KAFKA_ADDR, KAFKA_TOPIC)
    # Delete Prediction Data Request Topic
    print("INFO: Deleting " + KAFKA_PREDICTION_TOPIC + " topic...")
    kafka.delete_topic(KAFKA_ADDR, KAFKA_PREDICTION_TOPIC)
    # Delete Model
    print("INFO: Topics Deleted. Deleting Model...")
    cmd = "rm model.plk"
    execute_cmd(cmd)
    print('INFO: Cleaning Sucess')
    return True

def handler(signum, frame):
    global flag
    res = input("ACTION: Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        flag = False

def continuous_analysis(offset, partition):
    global flag 
    flag = True
    signal.signal(signal.SIGINT, handler)
    global learner
    print('INFO: Continuous Analysis Started. Waiting...')
    # init: data needs to be loaded to access by offset atfer
    kafka.receive_data(KAFKA_ADDR, KAFKA_TOPIC, offset + 2)
    while(flag):        
        print('\nINFO: Waiting Data From Kakfa')
        response = str(kafka.receive_data_offset(KAFKA_ADDR, KAFKA_TOPIC, partition, offset))
        offset += 1
        print('INFO: Data Received From Kakfa')
        if(response != "b\'\'"):
            data = iml.parse_response_data(response)
            print('INFO: Analysing Data With Incremental Learning Model')
            if (not learner.learn(data["data"], data["target"])):
                print('ERR: Incremental Learning Model Did Not Learn')
            print('INFO: Data Analysed')
        else:
            print("ERR: Kafka Response Empty")
            return
    print("INFO: Saving Model...")
    learner.save_model()
    print('INFO: Analysis Stopped\n')
    return offset

def predictions_request(offset, partition):
    global flag
    flag = True
    signal.signal(signal.SIGINT, handler)
    print('INFO: Loading Model')
    predictor = iml.Iml().load_model()
    print('INFO: Waiting Prediction Data From Kakfa')
    kafka.receive_data(KAFKA_ADDR, KAFKA_PREDICTION_TOPIC, offset + 2)
    while(flag):    
        print('\nINFO: Getting Data From Kakfa')
        response = str(kafka.receive_data_offset(KAFKA_ADDR, KAFKA_PREDICTION_TOPIC, partition, offset))
        print('INFO: Data Received From Kakfa')
        offset += 1
        if(response != "b\'\'"):
            data = iml.parse_response_data(response)
            print('INFO: Predicting from Data With Incremental Learning Model')        
            prediction_result = predictor.prediction(data["data"])
            print("INFO: Prediction Result of Data " + str(prediction_result) + " \n From Data: " + str(data))
        else:
            print("ERR: Kafka Response Empty")
            return
    predictor.printMetrics()
    return offset
