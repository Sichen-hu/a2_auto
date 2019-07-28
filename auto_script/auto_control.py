import  asyncio
from dict_bytes import dict_bytes

async def sendmsg(host, port, act_dict):  #
    reader, writer = await asyncio.open_connection (
        host, port)


    test_dict = act_dict

    await dict_bytes().send_dict2bytes (test_dict, writer)
    print(f'send msg:{test_dict}')
    text = await dict_bytes().read_bytes2dict(reader,writer)
    print(text)
    writer.close()


if __name__ == "__main__":
    act_dict = {
            'type': "activate",
            "config": {
                "role": "test"
            }
    }

    status_dict = {
        'type': "status",
    }

    output_dict = {
        'type': "output",
        "config": {
            "role": "test"
        }
    }

    end_dict = {
        'type': "terminate",
    }
    asyncio.run(sendmsg('127.0.0.1',20020,status_dict))
