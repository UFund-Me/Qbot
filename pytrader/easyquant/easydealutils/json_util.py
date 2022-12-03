import json
import os


class json_util:
    def loadJSONFile():
        jqdata = {"user": os.getenv("USER_ID"), "password": os.getenv("PASSWORD")}
        with open("jqdata.json", "w", encoding="utf-8") as fw:
            json.dump(jqdata, fw, indent=4, ensure_ascii=False)
        print(json)


if __name__ == "__main__":
    json_util.loadJSONFile()
