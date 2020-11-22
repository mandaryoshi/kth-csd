import sys
import ujson
from tqdm import tqdm
import time
import collections
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, '/home/csd/IK2200HT201-IXP')
#sys.path.insert(0, 'D:\\Documents\\IK2200HT201-IXP')

from phase2_scripts.phase2_impl import *

date = sys.argv[1]

#hours = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13",
#         "14","15","16","17","18","19","20","21","22","23"]

hours = ["1200","1300"]


#sys.path.insert(0, 'D:\\Documents\\IK2200HT201-IXP')

near_end_average = []
far_end_average = []
near_end_scatter = []
far_end_scatter = []

percentages = np.arange(0.45, 1, 0.05)

for thld in tqdm(percentages):
    daily_list_near = []
    daily_list_far = []
    for hour in tqdm(hours):
        
        
        input_path = "../traceroutes/" + date + "/" + hour + "/hop_results"
        hop_result_file = open(input_path)
        hop_results = ujson.load(hop_result_file)

        cfs = CFS(hop_results, date, hour)

        near_end_map = cfs.NearEnd(thld)
        far_end_map = cfs.FarEnd(thld)

        daily_list_near.append(cfs.step4_near)
        daily_list_far.append(cfs.step4_far)

    near_end_average.append(np.mean(daily_list_near))
    far_end_average.append(np.mean(daily_list_far))
    near_end_scatter.append(daily_list_near)
    far_end_scatter.append(daily_list_far)


#plt.plot(percentages, values)
fig, ax = plt.subplots()
ax.plot(percentages, near_end_average, label = 'Near-end')
ax.plot(percentages, far_end_average, label= 'Far-end')
ax.set_title('Total Facilities Identified for Varying Threshold Values')
ax.set_xlabel('Threshold Values')
ax.set_xticks(np.arange(0.45, 1, 0.05))
ax.set_ylabel('Total Facilities Identified')

for xe, ye in zip(percentages, near_end_scatter):
    plt.scatter([xe] * len(ye), ye, c="green")
for xe, ye in zip(percentages, far_end_scatter):
    plt.scatter([xe] * len(ye), ye, c="red")

ax.legend()
plt.grid()
plt.save("phase3_scripts/results/threshold_test.png")
