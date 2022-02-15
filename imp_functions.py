import json


def get_discord_mention(aim_id):
        return f'<!@{int(aim_id)}>'


def isLink(string):
        check_list = ['https://', 'http://']
        if any([i in string for i in check_list]):
                return True



def append_json(new_data, filename):
        with open(filename,'r+') as file:
            file_data = json.load(file)
            file_data.update(new_data)
            file.seek(0)
            json.dump(file_data, file, indent = 4)

def start_json(data, filename):
        with open(filename, 'w+') as file:
                json_data = json.dumps(data)
                file.write(json_data)
                file.close()




def get_jailed_roles(target):
        with open('pre_jail_roles.json', 'r+') as file:
                file_data = json.load(file)
                if target in file_data:
                        pre_jail_roles = file_data[target]

                        return pre_jail_roles



def remove_from_json(target, filename):
        with open(filename, 'r+') as file:
                file_data = json.load(file)

                if target in file_data:
                        del file_data[target]

                        with open(filename, 'w') as file1:
                                json.dump(file_data, file1)







