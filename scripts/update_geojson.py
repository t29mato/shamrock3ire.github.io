# -*- coding: utf-8 -*-

import json

import pandas as pd
import tabula


def to_int(vacancy):
    try:
        return int(vacancy)
    except ValueError:
        return 0


def ages_vacancies_to_string(vacancies):
    result = ""
    for i, vacancy in enumerate(vacancies):
        if vacancy > 0:
            result += str(i) + " "
    result += "歳児"
    return result


json_file_path = '../data/nurseryFacilities.geojson'

pdf_dfs = tabula.read_pdf("./pdfs/2023-1aki2.pdf", lattice=False, pages='1-2')

geo_json = json.load(open(json_file_path))
geo_df = pd.DataFrame(geo_json['features'])

for page_number, df in enumerate(pdf_dfs):
    for row_number, data in df.iterrows():
        if page_number == 0:
            if row_number == 0:
                continue
            if row_number == 1:
                nursery = geo_json["features"][0]["properties"]
                class_0 = to_int(data[4])
                class_1 = to_int(data[6])
                class_2 = to_int(data[8])
                class_3 = to_int(data[10])
                class_4 = to_int(data[12])
                class_5 = to_int(data[14])
            else:
                nurseries = [feature for feature in geo_json["features"] if feature["properties"]["nursery"] == data[1]]
                if len(nurseries) == 0:
                    continue
                nursery = nurseries[0]["properties"]
                class_0 = to_int(data[3])
                class_1 = to_int(data[5])
                class_2 = to_int(data[7])
                class_3 = to_int(data[9])
                class_4 = to_int(data[11])
                class_5 = to_int(data[13])

        elif page_number == 1:  # 2ページ目
            if row_number == 0 or row_number == 1:  # 表頭なので除外
                continue
            if row_number == 18 or row_number == 35:  # 認定こども園の「こ」という文字だけ取得されてる行なので除外
                continue
            if row_number == 47:  # 合計なので除外
                continue
            else:
                nurseries = [feature for feature in geo_json["features"] if feature["properties"]["nursery"] == data[2]]
                if len(nurseries) == 0:
                    continue
                nursery = nurseries[0]["properties"]
                class_0 = to_int(data[3].split()[1])
                class_1 = to_int(data[3].split()[3])
                class_2 = to_int(data[4].split()[1])
                class_3 = to_int(data[5].split()[1])
                class_4 = to_int(data[6].split()[1])
                class_5 = to_int(data[7].split()[1])
        print(nursery["nursery"])
        nursery["Vacancy0"] = class_0
        nursery["Vacancy1"] = class_1
        nursery["Vacancy2"] = class_2
        nursery["Vacancy3"] = class_3
        nursery["Vacancy4"] = class_4
        nursery["Vacancy5"] = class_5
        nursery["Vacancy"] = class_0 + class_1 + class_2 + class_3 + class_4 + class_5
        if nursery["Vacancy"] == 0:
            nursery["v_age"] = "null"
        else:
            nursery["v_age"] = ages_vacancies_to_string([class_0, class_1, class_2, class_3, class_4, class_5])

with open(json_file_path, 'w', encoding="utf-8") as j:
    json.dump(geo_json, j, ensure_ascii=False, indent=2)
