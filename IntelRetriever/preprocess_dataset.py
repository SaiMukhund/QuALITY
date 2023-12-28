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

def read_quality_dataset(path_file):
    file=open(path_file,'r')
    quality_data=json.load(file)
    file.close()
    final_data=[]
    for data in quality_data:
        article=data["article"]
        questions=data["questions"]
        for q in questions:
            q.pop("question_unique_id")
            q.pop("writer_label")
            q.pop("validation")
            q.pop("speed_validation")

        final_data.append({"passage":article,"questions":questions})
    return final_data

if __name__=="__main__":
    parser = argparse.ArgumentParser(
                    prog='conversion_to_json',
                    description='converts a text file containing string jsons into a json file ',
                    epilog='Text at the bottom of help')
    parser.add_argument("source_path",type=str,help="text file path of the dataset ")
    parser.add_argument("dest_path" , type=str,help="json file path to store data")

    args=parser.parse_args()
    convert_dataset_json(args.source_path,args.dest_path)

