#!/usr/bin/env python3
# Setup:
# This assumes you already have dependancies and compilers installed
# which I do since I program in python a lot.
# wget https://www.python.org/ftp/python/3.8.10/Python-3.8.10.tgz
# cd Python-3.8.10
# ./configure --enable-loadable-sqlite-extensions --prefix=/opt/python-3.8.10 --enable-optimizations
# make
# sudo make install
# mkdir ~/code_test
# cd ~/code_test
# /opt/python-3.8.10/bin/python3 -m venv ./py38
# source ./py38/bin/activate
# pip install --upgrade pip
# pip install -r requirements.txt
import sys
python_version = sys.version_info
if python_version.major != 3 and python_version.minor != 8:
    print("Please install Python 3.8.x")
    sys.exit(1)

try:
    import requests
except BaseException:
    print("Please install the python requests module: pip install requests.")
    sys.exit(1)


class CodeTest:
    def __init__(self):
        self.base_url = "https://jsonplaceholder.typicode.com"
        self.posts_url = "{}/posts".format(self.base_url)

    def test_post_id_range(self, post_id: int) -> None or ValueError:
        if not (0 < post_id < 101):
            raise ValueError

    def get_post_by_id(self, post_id: int) -> requests.models.Response:
        if not isinstance(post_id, int):
            raise TypeError
        self.test_post_id_range(post_id)
        response = requests.get("{}/{}".format(self.posts_url, post_id))
        return response

    def create_post(self, title: str, userid: int,
                    body: str) -> requests.models.Response:
        if not isinstance(
                title,
                str) and not isinstance(
                userid,
                int) and not isinstance(
                body,
                str):
            raise TypeError
        response = requests.post(
            self.posts_url,
            json={
                "title": title,
                "userId": userid,
                "body": body
            }
        )
        return response

    def delete_post(self, post_id: int) -> requests.models.Response:
        if not isinstance(post_id, int):
            raise TypeError
        response = requests.delete("{}/{}".format(self.posts_url, post_id))
        return response


if __name__ == "__main__":
    import json
    import datetime
    test_obj = CodeTest()

    response_one = test_obj.get_post_by_id(99)
    if response_one.ok:
        print(response_one.json().get("title"))

    response_two = test_obj.get_post_by_id(100)
    if response_two.ok:
        response_two_data = response_two.json()
        # why not iso8601?
        utc_date_str = datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%d:%S")
        response_two_data.update({
            "time": utc_date_str
        })
        print(json.dumps(response_two_data, indent=4))

    response_three = test_obj.create_post(
        title="Security Interview Post",
        userid=500,
        body="This is an insertion test with a known API"
    )
    response_three_tuple = None
    if response_three.ok:
        response_three_data = response_three.json()
        response_three_tuple = (
            response_three_data.get("id"),
            response_three.status_code,
            response_three.headers.get("X-Powered-By")
        )
    print(response_three_tuple)
    response_six = test_obj.delete_post(response_three_tuple[0])
    if response_six.ok:
        print(response_six.status_code)
        print(response_six.headers.get("X-Content-Type-Options"))

    del test_obj
