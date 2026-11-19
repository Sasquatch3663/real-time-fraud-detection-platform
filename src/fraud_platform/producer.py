import argparse, json, random, time
from kafka import KafkaProducer

def main():
    p=argparse.ArgumentParser(); p.add_argument('--bootstrap',default='localhost:9092'); p.add_argument('--topic',default='transactions'); p.add_argument('--count',type=int,default=10); a=p.parse_args()
    producer=KafkaProducer(bootstrap_servers=a.bootstrap, value_serializer=lambda v: json.dumps(v).encode())
    kinds=['PAYMENT','TRANSFER','CASH_OUT','CASH_IN','DEBIT']
    for i in range(a.count):
        tx={'step':i+1,'type':random.choice(kinds),'amount':round(random.uniform(10,10000),2),'oldbalanceOrg':12000.0,'newbalanceOrig':2000.0,'oldbalanceDest':0.0,'newbalanceDest':10000.0}
        producer.send(a.topic,tx); print('sent',tx); time.sleep(.2)
    producer.flush(); producer.close()
if __name__=='__main__': main()
