import csv
import json
with open ("cars.csv", "r") as f:
    reader =csv.reader(f)
    next(reader)
    
    data =[]
    for i in reader:
        data.append({"region": i[0],"category": i[1],"parameter":i[2],"mode":i[3],"powertrain":i[4],"year":i[5],"unit":i[6]})
    
print(data)

with open("names.json","w") as f:
    json.dump(data,f,indent=4)
#mode,powertrain,year,unit,value