def do(event, context):
    print(f"Input from the previous step: {event['result']}")

    if event['result']==0:
        return {
            "result": 1
        }