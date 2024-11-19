import requests
import json
import time

if __name__ == '__main__':
    with open("config.json", "r") as f:
        config = json.load(f)
    header = config["header"]

    # 爬取第一页
    page = config["now"]

    url = "https://www.zhipin.com/wapi/zpgeek/search/joblist.json?scene=1&query=java&city=100010000&experience=&payType=&partTime=&degree=&industry=&scale=&stage=&position=100101&jobType=&salary=&multiBusinessDistrict=&multiSubway=&page="+str(page)+"&pageSize=30"
    response = requests.get(url, headers=header).text
    resp_json = json.loads(response)
    page += 1
    print(resp_json)
    zpData = resp_json['zpData']
    jobList = zpData['jobList']
    for job in jobList:
        jobName = job['jobName']
        salaryDesc = job['salaryDesc']
        printData = {
            'jobName': jobName,
            'salaryDesc': salaryDesc
        }
        with open('data/wages.json', 'w+', encoding='utf-8') as f:
            f.write(str(printData)+'\n')
    # 开始正式爬取
    while resp_json['zpData']["hasMore"]:
        with open("config.json", "w") as f:
            json.dump({"header": header, "now": page}, f)

        response = requests.get("https://www.zhipin.com/wapi/zpgeek/search/joblist.json?scene=1&query=&city=101200100&experience=&payType=&partTime=&degree=&industry=&scale=&stage=&position=100102&jobType=&salary=&multiBusinessDistrict=&multiSubway=&page="+str(page)+"&pageSize=30", headers=header).text
        resp_json = json.loads(response)
        zpData = resp_json['zpData']
        jobList = zpData['jobList']
        page += 1
        for job in jobList:
            jobName = job['jobName']
            salaryDesc = job['salaryDesc']
            printData = {
                'jobName': jobName,
                'salaryDesc': salaryDesc
            }
            for k, v in printData.items():
                print(k, ":", v)
            with open('data/wages.txt', 'a',encoding="utf-8") as f:
                f.write(str(printData)+'\n')
        time.sleep(1)
