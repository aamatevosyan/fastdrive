import json
import os
import shutil
import uuid

import requests
from bs4 import BeautifulSoup
import glob

start_test_id = 1
end_test_id = 11

def get_test_path(test_id: int):
    return f'tests\\{test_id}\\'

if not os.path.exists('tests'):
    os.mkdir('tests')

for i in range(start_test_id, end_test_id + 1):
    for el in glob.iglob(os.path.join(get_test_path(i) + "\\img", '*.png')):
        filename = os.path.basename(el)
        shutil.copyfile(el, "tests\\img\\" + filename)

    with open(get_test_path(i) + "questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)

    for el in questions:
        el["test_id"] = i

    with open(get_test_path(i) + "questions.json", "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=4)