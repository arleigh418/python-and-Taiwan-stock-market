
from AES_Encryption.en_decrype import *
import json
import os
'''
用法:僅須在程式中使用:
conn,cursor = check_encrype('Any_string_you_define')
'''
def input_new_encrype(fuc_name,key_path,result_path):
    print(f'Starting input ......{fuc_name}')
    user_id = input('Please input gmail address:')
    password = input('Please input password:')
    result_file_path = (result_path+'encrype.config').replace('\n','')
    key = get_key(key_path,result_path)
    user_encrype = aes_encrypt(user_id, key)
    password_encrype = aes_encrypt(password, key)
    store_encrype = dict()
    store_encrype['name'] = fuc_name
    store_encrype['user_id'] = user_encrype
    store_encrype['password'] = password_encrype
    with open(result_file_path, 'a') as outfile:
        json.dump(store_encrype, outfile)
        outfile.write('\n')
    outfile.close()
    print('Encrype Over !')
    return user_id,password

def check_encrype(eng_name,key_path,result_path):
    status = 0
    key_file_path = (key_path+'key.key')
    result_file_path = (result_path+'encrype.config')

    if not os.path.exists(key_path):
            os.mkdir(key_path)
    if not os.path.exists(result_path):
            os.mkdir(result_path) 

    if os.path.isfile(result_file_path):
        pass
    else:      
        open(result_file_path,"a")

    with open(result_file_path,'r') as json_file:
        each_line = json_file.readlines()
        json_file.close()
        if len(each_line)!=0:
            for line in each_line:
                json_line = json.loads(line)
                if json_line['name'] ==eng_name:  
                    status+=1
                    key = get_key(key_path,result_path)
                    user_id = aes_decrypt(json_line['user_id'],key)
                    password = aes_decrypt(json_line['password'],key)
            if status ==0:
                user_id,password = input_new_encrype(eng_name,key_path,result_path)    
        else:
            user_id,password = input_new_encrype(eng_name,key_path,result_path)
    return user_id,password

