import time

def do(event, context):
    print(f"Input from the previous step: {event['result']}")
    print(f"Waiting...")
    time.sleep(90)

    if event['result']==1:
        return {
            "result": 2
        }