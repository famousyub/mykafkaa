import asyncio
import uvicorn 

from fastapi import FastAPI, Request 
from sse_starlette.sse import EventSourceResponse

from redis import Redis

app = FastAPI()
redis  = Redis(host='redis',port=6379)



@app.get("/msg")
async def root():

    return {"message":"work test"}


@app.get("/")
def start():
    redis.incr('hits')
    onther = str(redis.get('hits'),'utf-8')
    userdb = str(redis.get('userphp'),'utf-8')
    return  {'hits': 'webpage ' + onther +' hits','userdb':userdb}





STREAM_DELAY = 1  # second
RETRY_TIMEOUT = 15000  # milisecond

@app.get('/stream')
async def message_stream(request: Request):
    def new_messages():
        # Add logic here to check for new messages
        yield 'Hello World'
    async def event_generator():
        while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break

            # Checks for new messages and return them to client if any
            if new_messages():
                yield {
                        "event": "new_message",
                        "id": "message_id",
                        "retry": RETRY_TIMEOUT,
                        "data": "message_content"
                }

            await asyncio.sleep(STREAM_DELAY)

    return EventSourceResponse(event_generator())


#if __name__ =='__main__':
#    app.run(host='0.0.0.0',debug=True)
