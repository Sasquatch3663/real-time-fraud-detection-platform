import argparse, json, os
from kafka import KafkaConsumer
import requests

def main():
    p=argparse.ArgumentParser(); p.add_argument('--bootstrap',default=os.getenv('KAFKA_BOOTSTRAP_SERVERS','localhost:9092')); p.add_argument('--topic',default=os.getenv('KAFKA_TOPIC','transactions')); p.add_argument('--api',default='http://localhost:8000'); a=p.parse_args()
    consumer=KafkaConsumer(a.topic,bootstrap_servers=a.bootstrap,auto_offset_reset='earliest',enable_auto_commit=True,value_deserializer=lambda b:json.loads(b.decode()))
    print('Listening for transactions...')
    for msg in consumer:
        try: print(requests.post(a.api+'/predict',json=msg.value,timeout=10).json())
        except requests.RequestException as e: print('Scoring error:',e)
if __name__=='__main__': main()
