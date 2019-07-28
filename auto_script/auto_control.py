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

    act_test_dict = {
            'type': "activate",
            "config": {
                "role": "test"
            }
    }


    status_dict = {
        'type': "status",
    }

    pull_dict = {
        'type': "pull",
    }

    output_dict = {
        'type': "output",
        "config": {
            "role": "client"
        }
    }

    end_dict = {
        'type': "terminate",
    }

    print("start server, scheduler and client")
    asyncio.run(sendmsg('3.1.239.165',20020,act_scheduler_dict))
    asyncio.run(sendmsg('3.1.239.165',20020,act_server_dict))
    asyncio.run(sendmsg('3.1.239.165',20020,act_client_dict))
    input()
    print("\n\n")
    print("status")
    asyncio.run(sendmsg('3.1.239.165',20020,status_dict))
    input()
    print("output of client")
    asyncio.run(sendmsg('3.1.239.165',20020,output_dict))
    input()
    print("terminate")
    asyncio.run(sendmsg('3.1.239.165',20020,end_dict))
    asyncio.run(sendmsg('3.1.239.165',20020,status_dict))

    # asyncio.run(sendmsg('3.1.239.165',20020,act_server_dict))
    # asyncio.run(sendmsg('127.0.0.1',20020,end_dict))
