import asyncio
from lib.cortex import Cortex


async def do_stuff(cortex):
    # await cortex.inspectApi()
    print("** USER LOGIN **")
    await cortex.get_user_login()
    print("** GET CORTEX INFO **")
    await cortex.get_cortex_info()
    print("** HAS ACCESS RIGHT **")
    await cortex.has_access_right()
    print("** REQUEST ACCESS **")
    await cortex.request_access()
    print("** AUTHORIZE **")
    await cortex.authorize()
    print("** GET LICENSE INFO **")
    await cortex.get_license_info()
    print("** QUERY HEADSETS **")
    await cortex.query_headsets()
    if len(cortex.headsets) > 0:
        print("** CREATE SESSION **")
        # activate is False since we do not want to use high performance features (available on paid license)
        await cortex.create_session(activate=False,
                                    headset_id=cortex.headsets[0])
        #print("** CREATE RECORD **")
        #await cortex.create_record(title="test record 1")
        print("** SUBSCRIBE FACIAL EXPRESSIONS AND MOTION SENSOR DATA **")
        await cortex.subscribe(['com', 'mot'])
        while cortex.packet_count < 10:
            await cortex.get_data()
        await cortex.inject_marker(label='halfway', value=1,
                                   time=cortex.to_epoch())
        while cortex.packet_count < 20:
            await cortex.get_data()
        await cortex.close_session()


def test():
    print("hello world")
    cortex = Cortex('credentials.txt')
    asyncio.run(do_stuff(cortex))
    cortex.close()


if __name__ == '__main__':
    test()