import json
import requests
####### 도로명주소 위도 경도 값으로 바꿔주기 ########
#### 해서 db에 넣어주기!!!!! ######
import dbconnect as db
api_key = "key를 입력하시오"

def addr_to_lat_lon(addr):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query={address}'.format(address=addr)
    headers = {"Authorization": "KakaoAK " + api_key}
    result = json.loads(requests.get(url, headers=headers).text)

    if 'documents' in result and result['documents']:
        match_first = result['documents'][0]
    else:
        match_first = {'x': 0, 'y': 0}

    return [round(float(match_first['x']),6), round(float(match_first['y']),6)]

# n = 0
# r = db.select_all_pm()
# print(r[0][0])
# for i in r:
#     a = addr_to_lat_lon(i[2])
#     db.update_ll(i[0], round(a[1], 6), round(a[0], 6))
#     print(n, '번째임', a[0], ' ', a[1])
#     n += 1

# r = db.select_all_pm()
# print(r)
