from executeCmd import execute_cmd

KAFKA_PATH = "~/KAFKA/bin/"

def send_data(server_addr, topic_name, datafile):
    """
    send data to kafka topic
    server_addr can be 1 or more ip addrs serverA or serverA serverB
    data will be read each line at time
    """
    cmd = KAFKA_PATH + "kafka-console-producer.sh --broker-list " + str(server_addr) + ":9092 --topic " + str(topic_name) + " < " + str(datafile)
    execute_cmd(cmd)
    return True