from __future__ import print_function
import os, sys
import yaml
import re
import collections
import requests
import json
from tqdm import tqdm

this_path, _ = os.path.split(__file__)
config_path = os.path.join(this_path, "config.yaml")

def read():

    global definition
    global config
    global sentences

    try:
        dataset_name = sys.argv[1]
        dataset_path = os.path.join(this_path, dataset_name+".yaml")
        d = open(dataset_path,"r")
        c =  open(config_path,"r")
    except IndexError:
        print("Please run with dataset name: python app.py dataset_name")
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(0)
    else:
        conf_file = yaml.load(c)
        dataset_file = yaml.load(d)
        config = conf_file["config"]
        definition = dataset_file["definition"]
        sentences = dataset_file["data"]

        if type(sentences) is dict:    
            sentences = []
            start = dataset_file["start"]
            end = len(s) if dataset_file["end"]==-1 else dataset_file["end"]

            for i in list(range(start, end+1)):
                try:
                    sentences.append(dataset_file["data"][i])
                except Exception as e:
                    print(e)

    return config, definition, sentences

def mapper(code, reverse=False):

    inv_definition = {v: k for k, v in definition.items()}
    if reverse:
        return inv_definition[code]
    return definition[code]

def parse(s):

    entities = []
    
    # intent, capture intent if exist
    if s[0]=='\\':
        s = re.search(r"\\(\w+)\{(.+)\}",s,re.M|re.I)
        entities.append({
            "entity":"intent",
            "value": str(mapper(s.group(1)))
        })
        s = s.group(2)

    # clean sentence without symbol
    #                   code  firstvalue   secondvalue if exist
    clean = re.sub(r"\\(\w+)\{([^\{\}]+)\}(?:\{([^\{\}]+)\})?", r"\2", s)

    # entities, capture entity code and any character except curly bracket
    #                     code  firstvalue   secondvalue if exist
    k_s = re.findall(r"\\(\w+)\{([^\{\}]+)\}(?:\{([^\{\}]+)\})?", s, re.I)

    last_search = 0
    for k in k_s:
        # k is (entity_code, written value, real value)
        data = {}
        data["value"] = k[1] if k[2]=="" else k[2]
        data["start"] = clean.find(k[1], last_search)
        data["entity"] = mapper(k[0])
        data["end"] = data["start"] + len(k[1])
        last_search = data["start"]+1
        entities.append(data)

    return clean, entities

def main():
    print("Load data...")
    c, d, ss = read()

    train_url = "https://api.wit.ai/samples?v=" + str(c["version"])
    post_headers = {"Authorization":"Bearer " + str(c["bearer"]), "Content-Type": "application/json"}
    get_headers = {"Authorization":"Bearer " + str(c["bearer"])}
    entities_url = "https://api.wit.ai/entities?v=" + str(c["version"])

    print("Check all entities...")
    entities = requests.get(entities_url, headers=get_headers)
    for key, ent in d.items():
        if ent not in entities and key[0]!='i':
            requests.post(entities_url, headers=post_headers, data=json.dumps(
                {"id" : str(ent)}
            ))

    print("Start Training...")
    total_req = 0
    for s in tqdm(ss):
        clean, res = parse(s)
        req = requests.post(train_url, headers=post_headers, data=json.dumps(
            [{
                "text": clean,
                "entities": res
            }]
        ))
        if req.status_code == requests.codes.ok:
            total_req = (total_req + 1) 

    print("Total trained data:",total_req)

if __name__=="__main__":
    main()