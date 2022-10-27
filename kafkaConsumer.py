from executeCmd import execute_cmd

KAFKA_PATH = "~/KAFKA/bin/"

def create_topic(server_addr, replication_factor, partitions, topic_name):
    """
    creates topic
    usage example params ca.alpha.olypus.pt 1 3 health_data1
    """
    cmd = KAFKA_PATH + "kafka-topics.sh --create --bootstrap-server " + str(server_addr) + ":9092 --replication-factor " + str(replication_factor) + " --partitions " + str(partitions) + " --topic " + str(topic_name)
    execute_cmd(cmd)
    return 

def delete_topic(server_addr, topic_name):
    """
    creates topic
    usage example params ca.alpha.olypus.pt 1 3 health_data1
    """
    cmd = KAFKA_PATH + "kafka-topics.sh --bootstrap-server " + str(server_addr) + ":9092 --delete --topic " + str(topic_name)
    execute_cmd(cmd)
    return

def receive_data(server_addr, topic_name, max_messages):
    cmd = KAFKA_PATH + "kafka-console-consumer.sh --bootstrap-server " + str(server_addr) + ":9092 --topic " + str(topic_name) + " --from-beginning --max-messages " + str(max_messages)
    return execute_cmd(cmd)

def receive_data_offset(server_addr, topic_name, partition, offset):
    cmd = KAFKA_PATH + "kafka-console-consumer.sh --bootstrap-server " + str(server_addr) + ":9092 --topic " + str(topic_name) + " --max-messages 1 --partition " + str(partition) + " --offset " + str(offset)
    return execute_cmd(cmd)
