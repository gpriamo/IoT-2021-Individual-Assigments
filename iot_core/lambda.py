import boto3
import json
from datetime import datetime, timezone

def lambda_handler(event, context):
        client = boto3.client('iot-data', region_name='us-east-1')
        
        UTC_SKEW = 2
        START_HOUR = 8
        END_HOUR = 19
        
        hour_now = int(datetime.now(timezone.utc).time().hour)
        hour_now += UTC_SKEW
        if (hour_now >= 24):
                hour_now = hour_now - 24
        
        enable_lux = 0
        if (int(event['lux']) < 15 and (hour_now >= START_HOUR and hour_now <= END_HOUR)):
                enable_lux = 1
                
        led_code = 2 # Green
        if (int(event['temp']) < 10):
                led_code = 1 # Blue
        elif (int(event['temp']) > 30):
                led_code = 0 # Red

        # Change topic, qos and payload
        response = client.publish(
                topic='awsiot_to_localgateway',
                qos=0,
                payload=json.dumps({"acts":"1", "lux":str(enable_lux), "led":str(led_code)})
            )

        return response