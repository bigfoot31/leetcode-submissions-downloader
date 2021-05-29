import os
import json
import time

import tqdm
import requests

import config

LEETCODE_COOKIE_ID = ""

LEETCODE_PROBLEMS = "https://leetcode.com/api/problems/all"
LEETCODE_SUBMISSIONS = "https://leetcode.com/api/submissions/"


def api_wrapper(url):
    return requests.get(url, cookies={"LEETCODE_SESSION": LEETCODE_COOKIE_ID})


def get_all_problems():
    resp = api_wrapper(LEETCODE_PROBLEMS)

    if resp.status_code != 200:
        print("ERROR! Error message: {}".format(resp.json()))
        return

    with open(config.FILENAME_PROBLEMS, "w") as f:
        json.dump(resp.json(), f)


def get_submissions_helper(problems):

    failed_attempts = []
    pbar = tqdm.tqdm(problems)
    for slug in pbar:
        resp = api_wrapper(LEETCODE_SUBMISSIONS + slug)

        if resp.status_code != 200:
            failed_attempts.append(slug)
            pbar.set_postfix({"failed": len(failed_attempts)})
            continue

        with open(os.path.join(config.DIR_SUBMISSION, "{}.json".format(slug)), "w") as f:
            json.dump(resp.json(), f)

        time.sleep(2)

    with open(config.FILENAME_ERROR, "w") as f:
        json.dump(failed_attempts, f)


def get_submissions(problems):
    with open(config.FILENAME_PROBLEMS, "r") as f:
        problems = json.load(f)

    problems = [
        p["stat"]["question__title_slug"]
        for p in problems["stat_status_pairs"]
        if p["status"] == "ac"
    ]
    print("No. of problems solved {}".format(len(problems)))

    get_submissions_helper(problems)

    with open(config.FILENAME_ERROR, "r") as f:
        problems = json.load(f)
    while len(problems) > 0:
        get_submissions_helper(problems)
        with open(config.FILENAME_ERROR, "r") as f:
            problems = json.load(f)
        time.sleep(5)


if __name__ == "__main__":
    LEETCODE_COOKIE_ID = os.environ.get('LEETCODE_COOKIE_ID')
    get_all_problems()
    get_submissions()
