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
    act_client_dict = {
            'type': "activate",
            "config": {
                "role": "client",
                "region_id": 0,
                "client_number": 10,
                "zipf_param": 2,
                "min_acc": 0.5,
                "max_acc": 0.9,
                "min_lat": 1.0,
                "max_lat": 5.0,
                "comm": 5,
                "seed": 0
            }
    }

    act_scheduler_dict = {
            'type': "activate",
            "config": {
                "role": "scheduler",
                "gpu_server":["127.0.0.1", "127.0.0.2"],
                "cpu_server":["127.0.0.3", "127.0.0.4"],
            }
    }

    act_server_dict = {
            'type': "activate",
            "config": {
                "role": "server",
                "device": "gpu"
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
    asyncio.run(sendmsg('3.1.239.165',20020,act_server_dict))
