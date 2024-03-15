import os
from .utils import load,dump,generate_token
import carla
from .sensor import parse_lidar_data,parse_radar_data

def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)

class LidarSeg:
    def __init__(self,root,version,load=False):
        self.root = root
        self.version = version
        self.json_dir = os.path.join(root,version)
        mkdir(self.root)
        mkdir(self.json_dir)
        mkdir(os.path.join(self.root,"lidarseg"))
        self.data = {
            "category":[],
            "lidarseg":[],
            "progress":{"current_world_index":0,
                        "current_capture_index":0,
                        "current_scene_index":0,
                        "current_scene_count":0
                        }
        }
        self.data_cache = {}
        if load:
            self.load()
        else:
            self.save()

    def load(self):
        for key in self.data:
            json_path = os.path.join(self.json_dir,key+".json")
            self.data[key] = load(json_path)

    def save(self):
        for key in self.data:
            json_path = os.path.join(self.json_dir,key+".json")
            dump(self.data[key],json_path)
            print(json_path)
            
    def get_item(self,key,token):
        for item in self.data[key]:
            if item["token"] == token:
                return item
        return None

    def update_category(self,name,description,index,replace=True):
        lidarseg_category_item = {}
        lidarseg_category_item["token"] = generate_token("category",name)
        lidarseg_category_item["name"] = name
        lidarseg_category_item["description"] = description
        lidarseg_category_item["index"] = index
        if self.get_item("category",lidarseg_category_item["token"]) is None:
            self.data["category"].append(lidarseg_category_item)
        elif replace:
            self.data["category"].remove(self.get_item("category",lidarseg_category_item["token"]))
            self.data["category"].append(lidarseg_category_item)
        return lidarseg_category_item["token"]

    def update_lidarseg(self,timestamp,replace=True):
        lidarseg_item = {}
        lidarseg_item["token"] = generate_token("lidarseg",str(timestamp))
        lidarseg_item["sample_data_token"] = lidarseg_item["token"]
        lidarseg_item["filename"] = self.json_dir + "/" + lidarseg_item["token"] + ".bin"
        if self.get_item("lidarseg", lidarseg_item["token"]) is None:
            self.data["lidarseg"].append(lidarseg_item)
        elif replace:
            self.data["lidarseg"].remove(self.get_item("category", lidarseg_item["token"]))
            self.data["lidarseg"].append(lidarseg_item)
        return lidarseg_item["token"]