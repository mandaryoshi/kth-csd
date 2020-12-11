import json 
import sys
from tqdm import tqdm
import numpy as np
from datetime import date, timedelta
import ast 
from math import sqrt
import matplotlib.pyplot as plt
import matplotlib as mp


start_date = sys.argv[1].split('-')
end_date = sys.argv[2].split('-')

sdate = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))   # start date
edate = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))   # end date 

delta = edate - sdate  

hours = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13",
         "14","15","16","17","18","19","20","21","22","23"]

alarms = {}
diff_values = []
red_alarms = 0
yellow_alarms = 0

file_id = 0


for date in range(delta.days + 1):

    # "Calculate" what day is going to be looped through
    day = sdate + timedelta(days=date)

    print(day)
 
    for hour in hours:
        try:
            file = open("../traceroutes/" + str(day) + "/" + hour + "00/actual_rtt_sw_alarms")
        except FileNotFoundError:
            print('fnfe')

        alarm_file = json.load(file)

        # {"(53, 306)":[12.141,20.33833,6.57349],"(57, 53)":[3.94867,5.48933,1.22499],"(857, 18)":[2.21267,252.068,2.60434],"(18, 18)":[5.617,157.03133,0.55183]}

        for key, alarm in alarm_file.items():
            link = ast.literal_eval(key)
            link0 = str(link[0])
            link1 = str(link[1])

            diff_values.append((alarm[1] - alarm[0], link0, link1, str(day), hour, file_id))

        file.close()

        file_id = file_id + 1

#output_file = open("phase3_scripts/results/mse_values",'w')
#output_file.write(json.dumps(mse_values))
#output_file.close()

diff_values.sort(reverse = True)

#print(mse_values)

#output_file = open("phase3_scripts/results/mse_values",'w')
#output_file.write(json.dumps(mse_values))
#output_file.close()

diff_values_list = []
fac_list = []

for i in np.arange(50):
    text = "TOP " + str(i + 1) + " : " + str(diff_values[i])
    print(text)
    diff_values_list.append(diff_values[i][0])
    fac_list.append(str((diff_values[i][1], diff_values[i][2])))

fig, ax = plt.subplots(figsize=(7,5))

plt.title("Top 50 RTT Alarms")

plt.xlabel("Ranking")
plt.ylabel("RTT diff")

labels_1 = ['1'] + [None]*8

for x in np.arange(10, 50, 10):
    labels_1 = labels_1 + [str(x)] + [None]*9

labels_1 = labels_1 + ['50']

data_normalizer = mp.colors.Normalize()

color_map = mp.colors.LinearSegmentedColormap(
    "my_map",
    {
        "red": [(0, 1.0, 1.0),
                (1.0, .5, .5)],
        "green": [(0, 0.5, 0.5),
                  (1.0, 0, 0)],
        "blue": [(0, 0.50, 0.5),
                 (1.0, 0, 0)]
    }
)


x_ticks = np.arange(0, 50, 10)
x = np.arange(0, 50)
#ax.yaxis.set_major_formatter(formatter)
plt.bar(x, diff_values_list, color=color_map(data_normalizer(diff_values_list)))
plt.xticks(x, labels_1)
#plt.show()
plt.savefig("phase3_scripts/results/rtt_diff_graph.png")