import numpy as np
import os
import sys

class client_generator():
    def __init__(self,region_id, client_number, zipf_param,
                dist_def = "random", min_acc=0.5, max_acc=0.9,
                max_lat=5.0, min_lat=1.0,
                comm_interval = 5,model_name_list=["mobile","res18"], ):
        self.region_id = region_id
        self.client_number = client_number
        self.comm_interval = comm_interval

        self.model_name_list = model_name_list
        zipf_list = np.random.zipf(zipf_param, len(model_name_list))
        self.model_prob_list = list(zipf_list.astype("float") / np.sum(zipf_list))
        print(self.model_prob_list)


        self.dist_def = dist_def
        self.min_acc = min_acc
        self.max_acc = max_acc
        self.max_lat = max_lat
        self.min_lat = min_lat

    def get_model_name(self):
        if self.model_prob_list == None:
            print("Prob None Error")
            exit(0)
        random_normalized_num = np.random.random()
        print(random_normalized_num)
        acc_prob = 0.0

        for item in zip(self.model_name_list, self.model_prob_list):
            acc_prob += item[1]
            if random_normalized_num < acc_prob:
                return item[0]

    def random_sample(self,min_value,max_value):
        return min_value + (max_value - min_value) * np.random.rand()

    def get_acc(self):
        if self.dist_def == "random":
            return self.random_sample(self.min_acc,self.max_acc)
        print("undefined distribution on accuracy")
        exit(0)

    def get_lat(self):
        if self.dist_def == "random":
            return self.random_sample(self.min_lat,self.max_lat)
        print("undefined distribution on latency")
        exit(0)

    def get_trace(self,model_name):
        trace_root = "traces/region_%s/%s.npy"%(self.region_id, model_name)
        return trace_root

    def command_gen(self):

        command_list = []
        client_path = "/home/ubuntu/a2_auto/client/client.py"
        base_command = "python %s %s %s %s %s %s %s %s "
        for i in range(self.client_number):
            model_name = self.get_model_name()
            acc_limit = self.get_acc()
            lat_limit = self.get_lat()
            trace_file = self.get_trace(model_name)
            command = base_command % (client_path, self.region_id, i, model_name, "%.3f"%acc_limit, "%.3f"%lat_limit, trace_file,self.comm_interval)
            command_list.append(command)

        return command_list


if __name__ == "__main__":
    args = sys.argv

    region_id = int(args[1])
    client_number = int(args[2])
    zipf_param = float(args[3])
    min_acc = float(args[4])
    max_acc = float(args[5])
    min_lat = float(args[6])
    max_lat = float(args[7])
    comm_interval = int(args[8])
    comm_interval = int(args[8])


    np.random.seed(1)
    c_g = client_generator(region_id = region_id, client_number=client_number,
                            zipf_param=zipf_param, min_acc=min_acc, max_acc=max_acc,
                            min_lat = min_lat, max_lat = max_lat,
                            comm_interval = comm_interval)
    cmds =  c_g.command_gen()
    [print(x) for x in cmds]
    # os.system(cmds[0])
