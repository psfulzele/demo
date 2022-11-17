DEV-117390-psr-log-ingestion-libraryfile_path = "/Users/paragfulzele/Downloads/decoded_logs/three_times_numbers.txt"

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

