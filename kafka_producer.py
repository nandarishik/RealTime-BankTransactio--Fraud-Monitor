import pandas as pd
from kafka import KafkaProducer
import json
import time

def json_serializer(data):
    """Function to serialize Python dicts to JSON for Kafka."""
    return json.dumps(data).encode('utf-8')

def stream_transactions(file_path, topic_name):
    """Reads transaction data and streams it to a Kafka topic."""
    # Connect to the Kafka service running on localhost (port mapped in docker-compose)
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=json_serializer
    )

    # Load the transaction data
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        print("Please run `data_generator.py` first.")
        return

    print(f"Streaming transactions from '{file_path}' to Kafka topic '{topic_name}'...")

    # Loop through the dataframe and send each transaction
    for index, row in df.iterrows():
        transaction_data = row.to_dict()
        print(f"Sending: {transaction_data}")

        # Send data to Kafka
        producer.send(topic_name, value=transaction_data)

        # Simulate a real-time stream with a small delay
        time.sleep(1)

    print("Finished streaming all transactions.")
    producer.flush() # Ensure all messages are sent before exiting
    producer.close()


if __name__ == "__main__":
    TRANSACTIONS_CSV_PATH = 'transactions.csv'
    KAFKA_TOPIC = 'transactions'

    stream_transactions(TRANSACTIONS_CSV_PATH, KAFKA_TOPIC)