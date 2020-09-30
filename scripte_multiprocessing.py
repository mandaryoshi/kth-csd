from netaddr import IPNetwork, IPAddress
import json 
import time
from tqdm import tqdm
from scripta import IxpDetector
from multiprocessing import Process, Manager, Queue
import timeit
#start_time = timeit.default_timer()
#print(timeit.default_timer() - start_time)

def ixpdictionary(line, id, queue):
  ip_array = []
  iphop_dict = {}
  iphop_dict["id"] = id
  for i in json_line[str(id)]:
    ip_array.append(i["from"])
        
  ixp_ip2, ixp_id = ix_detector.ixpdetection(ip_array)
    
#If an IXP ip is detected, save it along with its previous and next hop IP addresses.        
  if ixp_ip2 :
    ixp_index = ip_array.index(str(ixp_ip2))

    iphop_dict["data"] = {
      'previous_hop' : ip_array[ixp_index-1] if (ixp_index-1 >= 0) else None,
      'ixp_hop' : ip_array[ixp_index],
      'next_hop' : ip_array[ixp_index+1] if (ixp_index+1 <= (len(ip_array)-1)) else None
    }
    queue.put(iphop_dict)

def writer(queue):
  file_object = open('json_results/hop_results', 'w')
  while True:
      try:
          dicionary = queue.get()
          file_object.write(json.dumps(dictionary))
          file_object.write('\n')
      except:
          break
  file_object.close()
  


if __name__ == "__main__":
  
  queue = Manager().Queue()
  ix_detector = IxpDetector()

  with open('json_results/traceroute_results','r') as readfile:
      id = 1
      writerp = Process(target = writer, args = (queue, ))
      writerp.start()
      for line in tqdm(readfile):
          json_line = json.loads(line)
          p = Process(target= ixpdictionary, args=(line, id, queue, ))
          p.start()
          id = id + 1

  