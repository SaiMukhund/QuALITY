import os
import json 
import argparse
def convert_dataset_json(path_file,dest_path):
    print(path_file,dest_path)
    with open(path_file,'r',encoding="utf8") as f:
        x=f.readlines()
    final_data=[]
    for data in x:
        json_data=json.loads(data)
        final_data.append(json_data)
    with open(dest_path,'w') as f:
        json.dump(final_data,f,indent=4)

if __name__=="__main__":
    parser = argparse.ArgumentParser(
                    prog='conversion_to_json',
                    description='converts a text file containing string jsons into a json file ',
                    epilog='Text at the bottom of help')
    parser.add_argument("source_path",type=str,help="text file path of the dataset ")
    parser.add_argument("dest_path" , type=str,help="json file path to store data")

    args=parser.parse_args()
    convert_dataset_json(args.source_path,args.dest_path)

