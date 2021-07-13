import os
import re
import pdb


base_path = "../../empirical_results/"

devices = ["GeForce 940M", "Quadro RTX 4000", "A14", "A12", "Intel HD620", "Mali-G77", "Adreno 620", "Tegra X1"]

device_alias = {"Quadro RTX 4000": "CUDA/toucan_quadro_rtx4000-inter-workgroup.csv",
                "GeForce 940M" : "CUDA/laptop_940m-inter-workgroup.csv",
                "A14" : "Apple/iphone_12_a14-inter-workgroup.csv",
                "A12" : "Apple/ipad_air_3_a12-inter-workgroup.csv",
                "Mali-G77": "Vulkan/galaxy-s20-mali-2021-02-07.csv",
                "Adreno 620" : "Vulkan/pixel5-adreno-2021-02-06.csv",
                "Tegra X1" : "Vulkan/results-NVIDIA-SHIELD-Android-TV.csv",
                "Intel HD620": "Vulkan/intelHD620-2021-03-16.csv"}


config = ["2_thread_2_instruction",
          "2_thread_3_instruction",
          "2_thread_4_instruction",
          "3_thread_3_instruction",
          "3_thread_4_instruction"]

d_result_failed_plain_det = {}
d_result_failed_plain_non = {}
d_result_failed_chunked_det = {}
d_result_failed_chunked_non = {}
d_result_failed_roundr_det = {}
d_result_failed_roundr_non = {}

for d in devices:
    d_result_failed_plain_det[d] = 0
    d_result_failed_plain_non[d] = 0
    d_result_failed_chunked_det[d] = 0
    d_result_failed_chunked_non[d] = 0
    d_result_failed_roundr_det[d] = 0
    d_result_failed_roundr_non[d] = 0

def get_data(fname):
    f = open(fname, 'r')
    ret = f.read()
    f.close()
    return ret

def split_d(d):
    d = d.split("\n")
    while d[-1] == '':
        d = d[:-1]
    assert("Total" in d[-1])
    assert("Test File" in d[0])
    return d[1:-1]

def get_failed_and_total(s):
    tt = re.match('.*\((\d+)/(\d+)\).*',s)
    if tt is None:
        pdb.set_trace()
    assert(tt)
    return int(tt[1]),int(tt[2])

def update_results(l,d):
    l_vals = l.split(",")[1:-1]
    
    if 'P' not in l_vals[0]:
        f,t = get_failed_and_total(l_vals[0])
        if f == t:
            d_result_failed_plain_det[d] += 1
        else:
            d_result_failed_plain_non[d] += 1
            
    if 'P' not in l_vals[2]:
        f,t = get_failed_and_total(l_vals[2])
        if f == t:
            d_result_failed_chunked_det[d] += 1
        else:
            d_result_failed_chunked_non[d] += 1
            
    if 'P' not in l_vals[1]:
        f,t = get_failed_and_total(l_vals[1])
        if f == t:
            d_result_failed_roundr_det[d] += 1
        else:
            d_result_failed_roundr_non[d] += 1

def get_csv_path(d,c):
    da = device_alias[d]
    return os.path.join(base_path,c,da)
        
for d in devices:
    for c in config:
        csv_file = get_csv_path(d,c)
        #print(csv_file)
        data = get_data(csv_file)
        lines = split_d(data)
        for l in lines:
            update_results(l,d)

header = ",".join(["device","plain-det","plain-nd","chunk-det","chunk-nd","rr-det","rr-nd"])
final = [header]
for d in devices:
    line = [d]
    line.append(d_result_failed_plain_det[d])
    line.append(d_result_failed_plain_non[d])
    line.append(d_result_failed_chunked_det[d])
    line.append(d_result_failed_chunked_non[d])
    line.append(d_result_failed_roundr_det[d])
    line.append(d_result_failed_roundr_non[d])
    line = [str(l) for l in line]
    final.append(",".join(line))

dat_file = "output.dat"
fhandle = open(dat_file, 'w')
fhandle.write("\n".join(final) + "\n")
fhandle.close()

        
