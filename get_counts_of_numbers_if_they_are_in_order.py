"""
if file has data in  order
11
12
13
15
16
35
40
41
42
43
44
then return output as {11:3, 15:2, 35:1, 40: 5 }
"""
file_path = "/Users/paragfulzele/Downloads/decoded_logs/three_times_numbers.txt"

with open(file_path) as f:
    data = f.readlines()

number_dict = dict()

i = 0
k = 0
while i < len(data)-1:
    j = i + 1
    if int(data[j]) - int(data[i]) == 1:
        if data[k].strip() in number_dict:
            number_dict[data[k].strip()] += 1
        else:
            number_dict[data[k].strip()] = 1
    else:
        k = i
    i = i + 1

for key, value in number_dict.items():
    print(F"{key}:{value}")

