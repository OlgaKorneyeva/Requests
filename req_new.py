import requests
import json
from datetime import datetime
import os
#--------------------------------------------------------------------------------------------
def make_result(res):
    if (res.status_code == 200):
        return res.status_code, json.loads(res.text)
    else:
        print(res)        
        return res.status_code, {}    
#--------------------------------------------------------------------------------------------
# PET API    
#--------------------------------------------------------------------------------------------
def create_pet_obj(pet_id, pet_name, status):
    return {
        "id": pet_id,
        "category": {
            "id": 0,
            "name": "unknown"
        },
        "name": pet_name,
        "photoUrls": [],
        "tags": [
            {
                "id": 0,
                "name": "untagged"
            }
        ],
        "status": status
    }
#--------------------------------------------------------------------------------------------
def pet_upload_image(pet_id, image_path):
    files = {'file': open(image_path,'rb'), 'type':'image/jpeg'}

    res = requests.post(f"https://petstore.swagger.io/v2/pet/{pet_id}/uploadImage", files=files, headers={'accept': 'application/json'})
    return make_result(res)
#--------------------------------------------------------------------------------------------
def pet_delete(pet_id):
    res = requests.delete(f"https://petstore.swagger.io/v2/pet/{pet_id}", 
                       headers={'accept': 'application/json'})
    
    return make_result(res)
#--------------------------------------------------------------------------------------------
def pet_find(pet_id):
    res = requests.get(f"https://petstore.swagger.io/v2/pet/{pet_id}", 
                       headers={'accept': 'application/json'})
    
    return make_result(res)
#--------------------------------------------------------------------------------------------
def pet_list(status):
    res = requests.get(f"https://petstore.swagger.io/v2/pet/findByStatus?status={status}", 
                       headers={'accept': 'application/json'})
    
    return make_result(res)
#--------------------------------------------------------------------------------------------
def pet_add(pet_id, pet_name, status):
    add_obj = create_pet_obj(pet_id, pet_name, status)

    res = requests.post(f"https://petstore.swagger.io/v2/pet", data = json.dumps(add_obj), 
                        headers={'accept': 'application/json', "Content-Type": "application/json"})
    
    return make_result(res)
#--------------------------------------------------------------------------------------------
def pet_update2(pet_id, new_name, new_status):
    upd_obj = { "name":new_name, "status":new_status }

    res = requests.post(f"https://petstore.swagger.io/v2/pet/{pet_id}", data = upd_obj, 
                        headers={'accept': 'application/json', "Content-Type": "application/x-www-form-urlencoded"})
    
    return make_result(res)
#--------------------------------------------------------------------------------------------
def pet_update(pet_id, new_name, new_status):
    upd_obj = create_pet_obj(pet_id, new_name, new_status)

    res = requests.put(f"https://petstore.swagger.io/v2/pet", data = json.dumps(upd_obj), 
                        headers={'accept': 'application/json', "Content-Type": "application/json"})
    
    return make_result(res)
#--------------------------------------------------------------------------------------------    
def run_pet_api():
    code, obj = pet_add(777, "Kumysay", "pending")
    if (code == 200):
        print('pet_add:', obj)

    code, obj = pet_find(777)
    if (code == 200):
        print('pet_find:', obj)   

    code, obj = pet_upload_image(777, 'cat1.jpg')
    if (code == 200):
        print('pet_upload_image:', obj)
          
    code, obj = pet_update2(777, "Kumysay-cat", "sold")
    if (code == 200):
        print('pet_update2:', obj)

    code, obj = pet_update(777, "Kumysay-cat", "avaliable")
    if (code == 200):
        print('pet_update:', obj)                
        
    code, obj = pet_list('sold')
    if (code == 200):
        print('pet_list(sold):', len(obj))

    code, obj = pet_list('pending')
    if (code == 200):
        print('pet_list(pending):', len(obj))

    code, obj = pet_delete(777)
    if (code == 200):
        print('pet_delete(777): ', obj)     
#--------------------------------------------------------------------------------------------
# STORE API
#--------------------------------------------------------------------------------------------
def order_create(ord_id, pet_id, qty):
    now = datetime.now()
    
    post_data = {
                    "id": ord_id,
                    "petId": pet_id,
                    "quantity": qty,
                    "shipDate": now.strftime("%Y-%m-%dT%H:%M:%S.000Z"), #"2023-03-30T15:37:44.430Z",
                    "status": "placed",
                    "complete": False
                }

    res = requests.post(f"https://petstore.swagger.io/v2/store/order", data = json.dumps(post_data), 
                        headers={'accept': 'application/json', "Content-Type": "application/json"})
    
    return make_result(res)
#--------------------------------------------------------------------------------------------    
def order_find_by_id(order_id):
    res = requests.get(f"https://petstore.swagger.io/v2/store/order/{order_id}", 
                       headers={'accept': 'application/json'})
    
    return make_result(res)
#--------------------------------------------------------------------------------------------    
def order_delete(order_id):
    res = requests.delete(f"https://petstore.swagger.io/v2/store/order/{order_id}", 
                       headers={'accept': 'application/json'})
    
    return make_result(res)
#--------------------------------------------------------------------------------------------       
def inventory_status():
    res = requests.get(f"https://petstore.swagger.io/v2/store/inventory", 
                       headers={'accept': 'application/json'})
    
    return make_result(res)
#--------------------------------------------------------------------------------------------    
def run_store_api():
    code, obj = order_create(100, 777, 10)
    if (code == 200):
        print('order_create(100, 777, 10): ', obj)

    code, obj = order_find_by_id(100)
    if (code == 200):
        print('order_find_by_id(100): ', obj)        
        
    code, obj = order_delete(100)
    if (code == 200):
        print('order_delete(100): ', obj)
        
    code, obj = order_find_by_id(100)
    if (code == 200):
        print('order_find_by_id(100): ', obj)        
        
    code, obj = inventory_status()
    if (code == 200):
        print('inventory_status(): ', obj)
#--------------------------------------------------------------------------------------------
# USER API
#--------------------------------------------------------------------------------------------
def user_createWithArray(user_info):
    post_data = []
    for user in user_info:
        rec =   {
                    "id": user['id'],
                    "username": user['u_name'],
                    "firstName": user['f_name'],
                    "lastName": user['l_name'],
                    "email": user['email'],
                    "password": user['pwd'],
                    "phone": user['phone'],
                    "userStatus": 0
                }
        post_data.append(rec)

    res = requests.post(f"https://petstore.swagger.io/v2/user/createWithArray", data = json.dumps(post_data), 
                        headers={'accept': 'application/json', "Content-Type": "application/json"})
    
    return make_result(res)    
#--------------------------------------------------------------------------------------------
def user_createWithList(user_info):
    post_data = []
    for user in user_info:
        rec =   {
                    "id": user['id'],
                    "username": user['u_name'],
                    "firstName": user['f_name'],
                    "lastName": user['l_name'],
                    "email": user['email'],
                    "password": user['pwd'],
                    "phone": user['phone'],
                    "userStatus": 0
                }
        post_data.append(rec)

    res = requests.post(f"https://petstore.swagger.io/v2/user/createWithList", data = json.dumps(post_data), 
                        headers={'accept': 'application/json', "Content-Type": "application/json"})
    
    return make_result(res)    
#--------------------------------------------------------------------------------------------
def get_user_by_username(username):
    res = requests.get(f"https://petstore.swagger.io/v2/user/{username}", 
                       headers={'accept': 'application/json'})
    
    return make_result(res)
#--------------------------------------------------------------------------------------------
def user_create(user_info):
    post_data = {
                    "id": user_info['id'],
                    "username": user_info['u_name'],
                    "firstName": user_info['f_name'],
                    "lastName": user_info['l_name'],
                    "email": user_info['email'],
                    "password": user_info['pwd'],
                    "phone": user_info['phone'],
                    "userStatus": 0
                }

    res = requests.post(f"https://petstore.swagger.io/v2/user", data = json.dumps(post_data), 
                        headers={'accept': 'application/json', "Content-Type": "application/json"})
    
    return make_result(res)
#--------------------------------------------------------------------------------------------
def user_update(user_name, user_info):
    post_data = {
                    "id": user_info['id'],
                    "username": user_info['u_name'],
                    "firstName": user_info['f_name'],
                    "lastName": user_info['l_name'],
                    "email": user_info['email'],
                    "password": user_info['pwd'],
                    "phone": user_info['phone'],
                    "userStatus": 0
                }

    res = requests.put(f"https://petstore.swagger.io/v2/user/{user_name}", data = json.dumps(post_data), 
                        headers={'accept': 'application/json', "Content-Type": "application/json"})
    
    return make_result(res)   
#--------------------------------------------------------------------------------------------
def user_delete(username):
    res = requests.delete(f"https://petstore.swagger.io/v2/user/{username}", 
                       headers={'accept': 'application/json'})
    
    return make_result(res) 
#--------------------------------------------------------------------------------------------
def login_user(username, password):
    res = requests.get(f"https://petstore.swagger.io/v2/user/login?username={username}&password={password}", 
                       headers={'accept': 'application/json'})
    
    return make_result(res)
#--------------------------------------------------------------------------------------------
def user_logout():
    res = requests.get(f"https://petstore.swagger.io/v2/user/logout", 
                       headers={'accept': 'application/json'})
    
    return make_result(res)
#--------------------------------------------------------------------------------------------
def run_user_api():
    users = [
            {
                'id': 100,
                'u_name': 'user1',
                'f_name': "Вася",
                'l_name': 'Пупкин',
                'email': 'pupkin@vasya.ru',
                'pwd': 'passwd1',
                'phone': 'n/a'
            },
            {
                'id': 101,
                'u_name': 'user2',
                'f_name': "Петя",
                'l_name': 'Сасонко',
                'email': 'petya@super.ru',
                'pwd': 'passwd2',
                'phone': 'n/a'
            }
        ]
    code, obj =  user_createWithArray(users)
    if (code == 200):
        print('user_createWithArray(..): ', obj)

    code, obj =  user_createWithList(users)
    if (code == 200):
        print('user_createWithList(..): ', obj)
        
    code, str = get_user_by_username("user1")
    if (code == 200):
        print('get_user_by_username("user1"): ', str)
        
    upd_user = {
                    'id': 101,
                    'u_name': 'user2',
                    'f_name': "Петр",
                    'l_name': 'Сасонко',
                    'email': 'petya@super.ru',
                    'pwd': 'passwd2',
                    'phone': 'n/a'
                }
    
    code, str = user_update("user2", upd_user)
    if (code == 200):
        print('user_update("user2"): ', str)    

    code, str = user_delete('user1')
    if (code == 200):
        print('user_delete("user1"): ', str)    
        
    new_user = {
                    'id': 103,
                    'u_name': 'user3',
                    'f_name': "Зина",
                    'l_name': 'Сасонко',
                    'email': 'zinaida@mail.ru',
                    'pwd': 'passwd3',
                    'phone': 'n/a'
                }        
    
    code, str = user_create(new_user)
    if (code == 200):
        print('user_create(..): ', str)  
        
    code, str = get_user_by_username("user3")
    if (code == 200):
        print('get_user_by_username("user3"): ', str)
        
    code, str = login_user("user3", 'passwd3')
    if (code == 200):
        print('login_user("user3"): ', str)    
    
    code, str = user_logout()
    if (code == 200):
        print('user_logout(): ', str)            
#--------------------------------------------------------------------------------------------
# MAIN CODE
#--------------------------------------------------------------------------------------------
run_pet_api()
print('--------------------------------')
run_store_api()
print('--------------------------------')
run_user_api()
