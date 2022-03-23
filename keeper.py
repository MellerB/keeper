import os
import json
import copy
import time
import pickle


def _load_jdata(filename,data_structure):
    jdata = None
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            jdata = pickle.loads(file.read())
    else:
        ds={}
        ds["data"]=copy.deepcopy(data_structure)
        ds["current_iteration"] = 0
        jdata = ds
    return jdata


def _save_jdata(jdata,filename):
    with open(filename, "wb") as file:
      file.write(pickle.dumps(jdata))
       

def run(fun, data_structure, filename ,iterations_number = 5000, save_period=60):
    jdata = _load_jdata(filename,data_structure)
    current_iteration = jdata["current_iteration"]
    data = jdata["data"]
    start = time.time()

    for i in range(current_iteration,iterations_number):
        data=fun(data)

        if  time.time()-start >= save_period or i == iterations_number-1: 
            jdata["data"] = data
            jdata["current_iteration"] = i
            _save_jdata(jdata,filename)
            start = time.time()
            print("data saved:",time.ctime(int(start)),"iteration:",i)

    return data
        
def get(filename):
    jdata = None
    with open(filename, 'rb') as file:
            jdata = pickle.loads(file.read())

    print("current_iteration:",jdata["current_iteration"])
    return jdata["data"]