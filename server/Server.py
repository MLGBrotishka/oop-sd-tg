import os
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
import torch
from kafka import KafkaProducer, KafkaConsumer
path_to_upper = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
path_to_media = "/media/"

model_id = "stabilityai/stable-diffusion-2-1-base"

scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler)
pipe = pipe.to(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))

producer = KafkaProducer(bootstrap_servers='localhost:9092')
consumer = KafkaConsumer('server',bootstrap_servers='localhost:9092')
for msg in consumer:
    print(msg)
    print(msg.key)
    print(msg.value)
    msg_text = msg.value.decode("utf-8")
    id_to_send = msg.key.decode("utf-8")
    message_id = msg_text.split(" ", 1)[0]
    prompt = msg_text.split(" ", 1)[1]
    image = pipe(prompt).images[0]
    image_name =path_to_upper + path_to_media + id_to_send + "-" + message_id + ".png"
    image.save(image_name)
    image_name = bytes(image_name, encoding='utf-8')
    producer.send('client',key=msg.key,value=image_name)
    producer.flush()