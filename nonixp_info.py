import json

filename = 'json_results/example_nonixp.pfx2as'

#nonixpip dictionary
dict1 = {}

fields = ['nonixpip','prefix_len','asn']

#Creating dictionary for ip
with open(filename) as fp:
    a=1
    for line in fp:
        #Readling line by line from text file
        describe = list(line.strip().split(None,2))
        print(describe)
        ip_no='ip'+str(a)

        b=0

        #nonixpip info dictionary
        dict2 = {}
        while b<3:
            dict2[fields[b]] = describe[b]
            b = b +1

        dict1[ip_no] = dict2
        a = a+1

output_file = open("json_results/nonixp_info_results.json", "w")
json.dump(dict1, output_file, indent = 4)