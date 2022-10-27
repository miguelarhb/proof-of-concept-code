import hlf
import kafkaProducer
from timeProgram import delay
import datasetController as dtsc
import signal

KAFKA_TOPIC = "trainer"
KAFKA_PREDICTION_TOPIC = "analyzer"
KAFKA_ADDR = "ca.alpha.olympus.pt"

CONTROLLER_FOLDER_PATH = "/home/hera/CONTROLLER/"
DATA_FOLDER_PATH = CONTROLLER_FOLDER_PATH + "dataset_files/"
DATA_FOLDER_INDEX_PATH = DATA_FOLDER_PATH + "index.txt"
DATA_PREDICTION_FOLDER_PATH = CONTROLLER_FOLDER_PATH + "dataset_files_analysis/"
DATA_PREDICTION_FOLDER_INDEX_PATH = DATA_PREDICTION_FOLDER_PATH + "index.txt"

def handler(signum, frame):
    global flag
    res = input("ACTION: Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        flag = False

def add_datafiles():
    global flag
    flag = True
    signal.signal(signal.SIGINT, handler)
    hlf_id_tracker = 1

    dtsc.undo_selection()
    delay("Undo Selection")
    dtsc.random_selection_analysis(5)
    delay("Selection")
    
    with open(DATA_FOLDER_INDEX_PATH, "r") as indexFile:
        for line in indexFile:
            if(not flag):
                print("\nEXCEPTION: Stopped!\n")
                break
            filename = DATA_FOLDER_PATH + str(line)
            filename = filename[:-1] #removes last \n char
            add_data(hlf_id_tracker, filename)
            hlf_id_tracker += 1
            print("INFO: Added " + str(hlf_id_tracker) + " files\n")
    
    print("INFO: Last FileID Added is " + str(hlf_id_tracker))
    return hlf_id_tracker

def add_datafiles_prediction():
    with open(DATA_PREDICTION_FOLDER_INDEX_PATH, "r") as indexFile:
        for line in indexFile:
            filename = DATA_PREDICTION_FOLDER_PATH + str(line)
            filename = filename[:-1] #removes last \n char
            send_prediction_data(filename)
            print("")
    return

def add_data(id, filename):
    status = hlf.add_data_hlf(id, filename)
    if not status:
        print('ERR: HLF or IPFS Error')
        return
    print('INFO: File Added With Success to HLF and IPFS')

    print('INFO: Sending Data to Kafka Cluster')
    response = kafkaProducer.send_data(KAFKA_ADDR, KAFKA_TOPIC, filename)    
    if (response):
        print('INFO: Data Sent to Kafka Cluster')
    else:
        print('ERR: Data Not Sent to Kafka Cluster')
    return

def send_prediction_data(filename):
    if (kafkaProducer.send_data(KAFKA_ADDR, KAFKA_PREDICTION_TOPIC, filename)):
        print('INFO: Data Sent to Kafka Cluster')
    else:
        print('ERR: Data Not Sent to Kafka Cluster')
    return

def read_data(id):
    data_path = hlf.get_data_hlf(id)  
    print('INFO: Data Retrieved With Success from HLF and IPFS')
    print('INFO: Data Located in File: ' + data_path)
    return data_path

def read_all_data():
    data_path = hlf.get_all_data_hlf()  
    print('INFO: All Data Fetched With Success from HLF and IPFS')
    print('INFO: All Data Located in Folder: ' + data_path)
    return data_path

def delete_data(id):
    status = hlf.delete_data_hlf(id)
    if not status:
        print('ERR: HLF or IPFS Error')
        return  
    print('INFO: Data Deleted With Success from HLF and IPFS')
    return

def delete_all_data(id):
    id_counter = 1
    id = int(id)
    while (id_counter <= id):
        delete_data(id_counter)
        id_counter += 1
    print("INFO: All Data Deleted from HLF and IPFS")