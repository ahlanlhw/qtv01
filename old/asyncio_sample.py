import asyncio as aio

async def fetch_data():
    print("fetcing data")
    await aio.sleep(2)
    print('done')
    return {"some variable":1}

async def print_stuff():
    for k in range(5):
        print(k)
        await aio.sleep(0.25)

async def main():
    l = []
    t1 = aio.create_task(fetch_data())
    t2 = aio.create_task(print_stuff())
    # val = await t1
    for v in [t1,t2]:
        await v
        l.append(v)
    val =aio.gather(*l)
    return val
val,_ = aio.run(main())
val