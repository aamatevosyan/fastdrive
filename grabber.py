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

questions = []

for i in range(start_test_id, end_test_id + 1):
    if not os.path.exists(get_test_path(i)):
        os.mkdir(get_test_path(i))

    if os.path.exists(get_test_path(i) + "img"):
        shutil.rmtree(get_test_path(i) + "img")

    if not os.path.exists(get_test_path(i) + "img"):
        os.mkdir(get_test_path(i) + "img")

    for zippath in glob.iglob(os.path.join(get_test_path(i), '*.png')):
        os.remove(zippath)

    if os.path.exists(get_test_path(i) + "index.html"):
        with open(get_test_path(i) + "index.html", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

            soup = soup.findAll("div", class_="col-lg-5 col-md-offset-3 m-t-30")

            ind = 0
            for el in soup:
                ind += 1
                question = {}
                question["id"] = f"test_{i}_{ind}"
                question["test_id"] = i
                if el.find("div", class_="cover-wrapper") is None:
                    question["img"] = "undefined"
                else:
                    question["img"] = f"test_{i}_{ind}.png"

                    if not os.path.exists("tests\\img\\" + question["id"] + ".png"):
                        downloaded_obj = requests.get(el.a.img["src"])

                        with open("tests\\img\\" + question["id"] + ".png", "wb") as file:
                            file.write(downloaded_obj.content)

                answer = []

                for button in el.find("div", class_="post-info").findAll("button"):
                    if button["type"] == "1":
                        correct = True
                    else:
                        correct = False
                    answer.append({
                        "text": button.text,
                        "correct": correct
                    })
                question["choices"] = answer
                question["question"] = el.find("div", class_="post-info").h4.text
                questions.append(question)



with open("tests/questions.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=4)

    print(questions)
