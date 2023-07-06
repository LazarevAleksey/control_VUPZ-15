import json
with open('./stp_conf/stp_3.json', 'r') as f:
    data = json.load(f)

list_of_bmk: dict[str, str] = data['stp_names']
list_of_control_com: list[str] = data['list_of_control_com']
buks_at_each_way: list[int] = data['stp_config']
current_buks_list: list[str] = []
# list_of_bmk = {
#         "009": "СТП 5",
#         "010": "СТП 6",
#         "011": "СТП 7",
#         "012": "СТП 8",
#         "013": "СТП 9A",
#         "014": "СТП 9",
#         "015": "СТП 10",
#         "016": "СТП 11A",
#         "017": "СТП 11",
#         "018": "СТП 12",
#         "020": "СТП 13",
#         "021": "СТП 14"
#     }
