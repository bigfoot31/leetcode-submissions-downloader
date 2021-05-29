import os
import json
from pathlib import Path

import config

MAP_DIFFICULTY_TO_DIR = ["1-easy", "2-medium", "3-hard"]

def map_lang_to_extension(lang):

    if lang.lower().startswith("python"):
        return "py"
    elif lang.lower().startswith("java"):
        return "java"
    elif lang.lower().startswith("cpp"):
        return "cpp"
    else:
        raise Exception("Language extension for lang: {} not supported".format(lang))


def parse_code():

    with open(config.FILENAME_PROBLEMS, "r") as f:
        problems_data = json.load(f)

    map_slug_to_difficulty = {} 
    for p in problems_data["stat_status_pairs"]:
        if p["status"] == "ac":
            map_slug_to_difficulty[ p["stat"]["question__title_slug"] ] = MAP_DIFFICULTY_TO_DIR[p["difficulty"]["level"]-1]

    for folder in MAP_DIFFICULTY_TO_DIR:
        rel_path = os.path.join(config.DIR_CODE, folder)
        if not os.path.exists( rel_path ):
            os.mkdir(rel_path)

    for root, _, fileNames in os.walk(config.DIR_SUBMISSION):

        for fileName in fileNames:

            filePath = os.path.join(root, fileName)
            fileName = Path(fileName)
            
            with open(filePath, "r") as f:
                metadata = json.load(f)
                submissions_dump = metadata["submissions_dump"]

            min_runtime = 100_000_000
            counter = 0
            correct_idx = 0
            for idx, submission in enumerate(submissions_dump):
                if submission["status_display"] == "Accepted":
                    runtime = int(submission["runtime"].split(" ")[0])
                    if runtime == min_runtime:
                        counter += 1 
                    elif runtime < min_runtime:
                        min_runtime = runtime
                        correct_idx = idx
            if counter > 1:
                print("This file: {} has multiple submissions with minimum runtime".format(fileName))

            submission_to_parse = submissions_dump[correct_idx]

            try:
                file_extension = map_lang_to_extension(submission_to_parse["lang"])
                subdir = map_slug_to_difficulty[fileName.stem]
                with open(os.path.join(config.DIR_CODE, subdir, "{}.{}".format(fileName.stem, file_extension)), "w") as f:
                    f.write(submission_to_parse["code"])
            except Exception as ex:
                print("Submission for file: {}. Exception: {}".format(fileName, ex))

if __name__ == "__main__":
    parse_code()    
