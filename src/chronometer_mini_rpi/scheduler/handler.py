from datetime import datetime
from chronometer_mini_rpi.scheduler.queue import Queue
import json
from pathlib import Path
import subprocess
import os
import re
from traceback import format_exc

schedules_json = json.load(open(Path(__file__).parent / "shedules.json"))

def clone_git_repo(repo_url:str, folder_name:str = None):
    print(os.getcwd())
    if folder_name is None:
        folder_name = repo_url.rsplit("/", maxsplit=1)[-1].replace(".git", "")
    if Path(folder_name).exists():
        print(f"{folder_name} exists")
        return folder_name
    print(f"cloning {repo_url}")
    subprocess.check_output(['git', 'clone',repo_url, folder_name])
    return folder_name

def get_poetry_venv(path:str):
    # current_wd = os.getcwd()
    # os.chdir(path)
    # try:
    #     poetry_show_output = subprocess.check_output(["poetry", "show", "-v"])
    #     os.chdir(current_wd)
    #     venv_path_match = re.match(r"^Using virtualenv: ([\:\w\.\\\s\/\-]+)", poetry_show_output.decode("utf8"))
    #     print(poetry_show_output.decode("utf8"))
    #     venv_path = venv_path_match.group(1)
    #     if not venv_path:
    #         venv_path = f"{path}/.venv/Scripts/python.exe"
    #     return venv_path
    # except Exception as error:
    #     print(error)
    #     os.chdir(current_wd)
    return f".venv/bin/python"

def init_bot(item):
    current_wd = os.getcwd()
    repo_url = item.get("repo")
    bot_name = clone_git_repo(repo_url)
    try:
        # cobweb_pypi = os.environ.get('COBWEB_PYPI')
        os.chdir(bot_name)
        if not Path("./pyproject.toml").exists():
            raise Exception("Not a poetry project")
        # clone_venv('./.venv', default_env_path)
        # subprocess.check_output(["poetry","source","add", "--secondary","cobweb", cobweb_pypi])
        subprocess.check_output(["poetry", "lock"])
        subprocess.check_output(["poetry", "install"])
        os.chdir(current_wd)
        return bot_name
    except Exception as error:
        print(error)
        os.chdir(current_wd)
        return bot_name

def run_scraper(item):
    current_wd = os.getcwd()
    bot_path = init_bot(item)
    env_path = get_poetry_venv(bot_path)
    print(">>>>>>>>>>>>>>", env_path)
    try:
        os.chdir(bot_path)
        print(subprocess.check_output([env_path, "-m","pycobweb","run"]))
    except Exception as error:
        print(error)
        print(format_exc())
    finally:
        os.chdir(current_wd)
        


queue = Queue()
queue.listener(run_scraper)

def schedule_handler():
    now = datetime.now()
    day = now.day
    month = now.month
    year = now.year
    weekday = now.weekday()
    hour = now.hour
    minute = now.minute

    now_dict = {
        "day": day,
        "month": month,
        "year": year,
        "weekday": weekday,
        "hour": hour,
        "minute": minute,
    }
    for schedule in schedules_json:
        schedule_object = schedule.get("scheduleObject",{})
        time_object = schedule.get("timeObject", {})
        is_schedule_time = compare_dict(now_dict,time_object)
        if is_schedule_time:
            queue.enqueue(schedule_object)

def compare_dict(source:dict, dest:dict)->bool:
    compasion_list = []
    for key, value in source.items():
        compasion_list.append( dest.get(key) == value)
    return any(compasion_list)