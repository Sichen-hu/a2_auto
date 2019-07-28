import asyncio
import logging
import subprocess
import json
import dict_bytes as db
import os
import time
# from .model import *
# from .measurement import *
# from .placement import Placement

logging.basicConfig(level=logging.DEBUG)


server_profile = {
    "mobile_dcp_0": {
        "port": [10101, 10102],
        "frac": 0.08,
        "batch": 2,
        "timeout": 10,
        "threads": 16,
        "device": "cpu"
    },
}

# controller　send decision


class auto_server():
    def __init__(self, addr="0.0.0.0", port="20020"):
        self.addr = addr
        self.port = port

        self.dict_tool = db.dict_bytes()
        self.process_pool = {}
        self.active_role = []
        self.output_dict = {}
        self.source_root = "/home/ubuntu/a2_source/"

        self.init_source()
        self.run = asyncio.run(self.main())

    def init_source(self):
        cmd = "git clone https://github.com/Sichen-hu/a2_auto %s" % self.source_root
        pass


    async def handle_socket(self, reader, writer):


        receive_data = await self.dict_tool.read_bytes2dict(reader, writer)
        print("receied: ", receive_data)
        return_data = None
        if receive_data['type'] == 'pull':
            return_data = self.pull_latest_source()

        elif receive_data['type'] == 'activate':
            act_config = receive_data["config"]
            return_data = self.activate_role(act_config)

        elif receive_data['type'] == 'terminate':
            return_data = self.terminate_process()

        elif receive_data['type'] == 'status':
            return_data = self.get_status()

        elif receive_data['type'] == 'output':
            ouput_config = receive_data["config"]
            return_data = self.get_output(ouput_config)


        await self.dict_tool.send_dict2bytes(return_data, writer)
        writer.close()

    def pull_latest_source(self):
        cmd = "cd %s; git pull" % self.source_root
        # p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        # p.wait()
        print(cmd)
        return {"result_code": 1,"result_info":"Pull Done"}

    def activate_role(self,config):
        role = config["role"]

        if role in self.process_pool.keys():
            return {"result_code": 0,"result_info":"Role already activated"}


        if role == "server":
            cmd = "python server.py"
        elif role == "client":
            cmd = "python client.py"
        elif role == "controller":
            cmd = "python controller.py"
        elif role == "scheduler":
            cmd = "python scheduler.py"
        elif role == "test":
            cmd = "python print_test.py"
        else:
            return {"result_code": 0,"result_info":"Undefined Type"}

        p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)

        # if role in self.process_pool.keys():
        #     self.process_pool[role].append(p)
        #     self.output_dict[role].append("")
        # else:
        self.process_pool[role] = p
        self.output_dict[role] = ""

        return {"result_code": 1,"result_info":"Activate Done"}


    def terminate_process(self):
        for role, p in self.process_pool.items():
            p.kill()

        self.process_pool = {}
        self.output_dict = {}
        return {"result_code": 1,"result_info":"Terminate Done"}

    def get_status(self):
        status_dict = {}
        for role, p in self.process_pool.items():
            returncode = p.poll()
            if returncode is None:
                status_dict[role] = "running"
            else:
                status_dict[role] = "exit"

        return status_dict

    def get_output(self,config):
        target = config["role"]
        return {"output":self.output_dict[target]}


    async def gather_process_output(self):
        while True:
            await asyncio.sleep(3)
            for role, p in self.process_pool.items():
                returncode = p.poll()
                if returncode is None:
                    self.output_dict[role] += p.stdout.readline().decode()


    async def socket(self):
        server = await asyncio.start_server(
            self.handle_socket, self.addr, self.port)

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()

    async def main(self):
        await asyncio.gather(self.socket(),self.gather_process_output())


if __name__ == "__main__":
    a2 = auto_server()
