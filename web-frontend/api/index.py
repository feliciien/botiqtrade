import json

def handler(request):
    return (
        json.dumps({'message': 'Trading Assistant API is running.'}),
        200,
        {'Content-Type': 'application/json'}
    )