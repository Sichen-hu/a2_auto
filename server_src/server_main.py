from server.a2_ml_server import a2_ml_server
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-a",default='0.0.0.0',) #server ip addr
parser.add_argument("-p",default=9949) # server port

args = parser.parse_args()

a2_ml_server(args.a,args.p)
