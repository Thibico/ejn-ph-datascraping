import requests
import json

# api_url = "https://apps2.dpwh.gov.ph/server/rest/services/DPWH_Public/RoadNetwork_RoadCondition/MapServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=CONDITION%20ASC&outSR=32651&resultOffset=0&resultRecordCount=1000"

## Function to call api data
def get_data_api(url: str):
    call_api = requests.get(url, verify=False)
    print(call_api.status_code)

    if call_api.status_code == 200:
        resp_json = call_api.json()
        features_lst = resp_json['features']
        print("Len of Features: ", len(features_lst))
        return features_lst
    else:
        print("Can't call api.")


## Function to parse feature list into list of dictionaries
def parse_feat(lst: list, output: list):
    for i in lst:
        # print(i['attributes']['REGION'])
        output.append(i['attributes'])
    return output

## Main code
def main_func():
    output = []
    offset = 0
    for count in range(1, 93):
        resultCount = count * 1000
        api_url = f"https://apps2.dpwh.gov.ph/server/rest/services/DPWH_Public/RoadNetwork_RoadCondition/MapServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=CONDITION%20ASC&outSR=32651&resultOffset={offset}&resultRecordCount={resultCount}"
        try:
            feat_lst = get_data_api(api_url)
            output = parse_feat(feat_lst, output)
            offset = resultCount + 1
            print(f"for {count} times between {offset} & {resultCount}: len of output - {len(output)}")
        except Exception as e:
            print(f"Error {e}")
            break
    
    print("Length of output: ", len(output))
    with open("result.json", "w") as out:
        json.dump(output, out)

## Call to run main func
if __name__ == "__main__":
    main_func()
    print("Main func done!")
