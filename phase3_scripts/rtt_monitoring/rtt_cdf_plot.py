import ujson 
import numpy as np
import matplotlib.pyplot as plt

def cdf_plot(cdf_x_labels1,cdf_x_labels2,cdf_x_labels3,cdf_x_labels4):
    #Plot CDF value for number of alarms
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16, 8))
    sortedlabels = np.sort(cdf_x_labels1)
    p = 1. * np.arange(len(cdf_x_labels1))/(len(cdf_x_labels1) - 1) 
    f1 = ax.plot(sortedlabels, p, color='g')
    sortedlabels = np.sort(cdf_x_labels2)
    p = 1. * np.arange(len(cdf_x_labels2))/(len(cdf_x_labels2) - 1) 
    f2 = ax.plot(sortedlabels,p, color='r')
    sortedlabels = np.sort(cdf_x_labels3)
    p = 1. * np.arange(len(cdf_x_labels3))/(len(cdf_x_labels3) - 1) 
    f3 = ax.plot(sortedlabels, p, color='b')
    sortedlabels = np.sort(cdf_x_labels4)
    p = 1. * np.arange(len(cdf_x_labels4))/(len(cdf_x_labels4) - 1) 
    f4 = ax.plot(sortedlabels, p, color='orange')
    plt.legend(('12/12','18/6', '21/3', '24/0'), loc = 'upper left', shadow=False, fancybox=True)
    plt.xlabel("No of alarms")
    plt.xscale('log', basex=2)
    plt.xlim(1,128)
    plt.ylabel("CDF")
    #plt.xticks(np.arange(0, len(cdf_x_labels1), 5))
    plt.yticks(np.arange(0, 1.05, 0.1))
    plt.grid(True)
    plt.savefig("../results/cdf.png", bbox_inches='tight')
    plt.close()

file1 = open("../results/rtt_cdf_12",'r')
ref_links1 = ujson.load(file1)
file1.close()
file2 = open("../results/rtt_cdf_6",'r')
ref_links2 = ujson.load(file2)
file2.close()
file3 = open("../results/rtt_cdf_3",'r')
ref_links3 = ujson.load(file3)
file3.close()    
file4 = open("../results/rtt_cdf_0",'r')
ref_links4 = ujson.load(file4)
file4.close()  

zero_alarm = []
for item in ref_links1.keys():
    if ref_links1[item] == 0  and ref_links2[item] == 0 and  ref_links3[item] == 0 and ref_links4[item] == 0:
        zero_alarm.append(item)

print(len(zero_alarm))
for item in zero_alarm:
    ref_links1.pop(item)
    ref_links2.pop(item)
    ref_links3.pop(item)
    ref_links4.pop(item)

cdf_x_labels1 = list(ref_links1.values())
print(len(cdf_x_labels1))
cdf_x_labels2 = list(ref_links2.values())
print(len(cdf_x_labels2))
cdf_x_labels3 = list(ref_links3.values())
print(len(cdf_x_labels3))
cdf_x_labels4 = list(ref_links4.values())
print(len(cdf_x_labels4))

cdf_plot(cdf_x_labels1,cdf_x_labels2,cdf_x_labels3,cdf_x_labels4)

