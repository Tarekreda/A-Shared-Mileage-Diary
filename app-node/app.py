import redis
from time import sleep
from flask import Flask, render_template, request, Response 
from json import dumps, loads 
from kafka import KafkaProducer, KafkaConsumer
from threading import Thread

app = Flask(__name__)
r= redis.Redis(host='localhost', port=6379)   #setting the redis data base host and port locally on the host machine


producer = KafkaProducer(bootstrap_servers=['localhost:9092']) #connecting the producer to the broker contained in a docker container from the host machine


@app.route('/', methods = ['GET', 'POST'])  #the main index entry point to our app 

def main():
    if request.method == 'POST':  
        producer.send('mileage_journal',value= dumps({'name': request.form['name']  ,'car': request.form['car'] , 'mileage': int(request.form['mileage'])}).encode('utf-8'))
        producer.flush() 
        # the kafka-python producer publishes the data to the broker
    elif request.method == 'GET':
        return render_template('index.html', form=request.form)
    

    return render_template('index.html')




def stream_template(template_name, **context):          # Enabling streaming back results to app
    app.update_template_context(context)
    template = app.jinja_env.get_template(template_name)
    streaming = template.stream(context)
    return streaming

def threaded_task():                                      # continously updating the redis data base with the new events published to kafka in the background 
    consumer2 = KafkaConsumer(
    'mileage_journal',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group-id',
    value_deserializer=lambda x: loads(x.decode('utf-8')),
    consumer_timeout_ms=500
    )
    x=0
    for message in consumer2:
        r.hmset(str(x), message.value)
        x=x+1
    r.set('number', x)



@app.route('/getcalculation')                         # the entry point to get the entries registred in the diary 

def consume():                                            # the consumer consumes the events available at the topis specified  
    consumer = KafkaConsumer(
        'mileage_journal',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group-id',
        value_deserializer=lambda x: loads(x.decode('utf-8')),
        consumer_timeout_ms=500
    )

    def consume_msg():
        for message in consumer:
            print(message.value)
            yield [
                message.value["name"],
                message.value["car"],
                message.value["mileage"]]



    return Response(stream_template('diary.html', data=consume_msg()))    # the template will present the data returned by the consumer 



@app.route('/bill', methods = ['GET', 'POST'])

def bill():

    thread = Thread(target=threaded_task, args=())
    thread.daemon = True
    thread.start()

    if request.method == 'POST':  

        name=request.form['name']
        car=request.form['car']

        sum_user=0.0
        sum_total=0.0
        for x in range (int(r.get('number').decode())):
            if r.hget(str(x),'car').decode() == car:
                sum_total=sum_total+int(r.hget(str(x),'mileage').decode())
                if r.hget(str(x),'name').decode() == name:
                    sum_user=sum_user+int(r.hget(str(x),'mileage').decode())

        try:
            return name + ' drove the ' + car + ' for a total of: ' + str(sum_user)+ " out of "+ str(sum_total) + " and he owes " + str(round((sum_user/sum_total)*100,3))  +"% of the total gas value" 
        except:
            sleep(1)
            return name + ' drove the ' + car + ' for a total of: ' + str(sum_user)+ " out of "+ str(sum_total) + " and he owes " + str(round((sum_user/sum_total)*100,3))  +"% of the total gas value" 


    return render_template('bill.html')
