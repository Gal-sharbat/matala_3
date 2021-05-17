import json 
phones_dict = dict()
current_id = 1


# def convert_chat_to_json(input_file_name, output_file_name):
#     dicts = read_file(input_file_name)
#     print(dicts["messages"])
#     print(dicts["metadata"])
#     # dump to json
    

         

def read_file(file_name):
    with open(file_name, "r", encoding="utf8") as file:
        global metadata
        lines = file.readlines()
        messages = get_messages(lines)
        metadata = get_metadata(lines)
        file.close()
        return {"messages": messages, "metadata": metadata}


def get_messages(lines):
    lines = make_data_anonymous(lines)
    dicts_data = translate_data_to_dicts(lines)
    return dicts_data


def make_data_anonymous(lines):
    global phones_dict, current_id
    anonymous_lines = []
    for line in lines:
        index_of_start_of_number = line.find(" - ")
        if index_of_start_of_number == -1:
            continue
        index_of_end_of_number = line.find(":", index_of_start_of_number)
        if index_of_end_of_number == -1:
            continue
        number = line[index_of_start_of_number+3:index_of_end_of_number]
        if number not in phones_dict:
            phones_dict[number] = current_id
            current_id = current_id + 1
        anonymous_lines.append(line.replace(number, str(phones_dict[number])))
    return anonymous_lines


def translate_data_to_dicts(lines):
    data = []
    for line in lines:
        time_end_index = line.find(" - ")
        time = line[:time_end_index]
        time = time.replace(".", "-")
        time = time.replace(",", "")
        number_id_end_index = line.find(":", time_end_index)
        number_id = line[time_end_index+3:number_id_end_index]
        txt = line[number_id_end_index+2:]
        data.append({"datatime": time, "id": int(number_id), "text": txt.replace("\n", "")})
    return data


def get_metadata(lines):
    global current_id
    for line in lines:
        if "הקבוצה" in line and "נוצרה על ידי" in line:
            line = line[line.index("הקבוצה"):]
            group_name = line[8:line.find("\"", 8)]
            creator_name = line[line.find("נוצרה על ידי")+15:-3]
            return {"chat_name": group_name, "creator": creator_name, "num_of_participants": "<"+str(current_id-1)+">"}

dicts=read_file('chat_2.txt')

file_json = json.dumps( dicts, ensure_ascii=False)
with open(metadata['chat_name'],'w',encoding=('utf8')) as final:
    final.writelines(file_json)
    final.close()
            