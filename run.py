import array
import datetime
import fcntl
import json
import shutil
import subprocess
import sys
import termios
from pathlib import Path

import ollama
from llmware.models import ModelCatalog
from PIL import Image
from prompt_toolkit import prompt as input
from rich import print as rprint
from rich.live import Live
from rich.prompt import Prompt
from rich.table import Table

from utility.richtables import Tables
from utility.textSearch import txt


def requiredLines(img, width, char, lines):
    buf = array.array("H", [0, 0, 0, 0])
    fcntl.ioctl(1, termios.TIOCGWINSZ, buf)
    displayresH = buf[3]
    displayresW = buf[2]
    return int(
        img.height
        / (((img.width / width) / (displayresW / char)) * (displayresH / lines))
    )


def clear_kitty_image():
    sys.stdout.write("\033c")
    sys.stdout.flush()


def display_image(image_path, rectangle, id):
    subprocess.run(
        [
            "kitten",
            "icat",
            "--place",
            rectangle,
            "--z-index",
            "-1",
            "--image-id",
            str(id),
            image_path,
        ]
    )


class RunModel:
    def __init__(self):
        pass

    def read(self, logs):
        cpath = txt.search("custom_path", "saves/default/config.conf")
        with open(
            cpath + "/history/" + logs + ".json",
            "r",
        ) as history:
            history = json.load(history)[2:]
            user_conversation = txt.search(
                "user_conversation", "saves/default/config.conf"
            )
            try:

                if (
                    int(txt.search("emotion_generation", "saves/default/config.conf"))
                    < 1
                ):
                    raise

                with open(
                    cpath + "/history/" + logs + "-emotions.json",
                    "r",
                ) as emotionlist:
                    emotionlist = json.load(emotionlist)
                    j = 0
                    char, lines = shutil.get_terminal_size()
                    width = int(txt.search("width", "saves/default/config.conf"))
                    for _ in range(lines):
                        print("")
                    for i in range(int(len(history) / 2)):
                        rprint("\n" + user_conversation + " " + history[j]["content"])
                        pngPath = txt.search_image(emotionlist[i], cpath)
                        png = Image.open(pngPath)
                        height = (
                            int(width * png.height / png.width) + 1
                            if (
                                int(width * png.height / png.width)
                                != (width * png.height / png.width)
                            )
                            else int(width * png.height / png.width)
                        )
                        required_lines = requiredLines(png, width, char, lines)
                        rectangle = str(width) + "x" + str(height) + "@" "2x" + str(
                            int(lines - required_lines - 5)
                        )
                        space = ""
                        for _ in range(required_lines):
                            for _ in range(width):
                                space += " "
                            space += "\n"

                        rprint(
                            Tables.table_with_emotion(
                                history[j + 1]["content"],
                                space,
                            )
                        )
                        print("\n")
                        subprocess.run(
                            ["kitten", "icat", "--place", rectangle, pngPath]
                        )
                        for _ in range(required_lines + 1):
                            print("")
                        j += 2
                        print("\n")
            except:
                subprocess.run(["clear"])
                clear_kitty_image()
                rprint(
                    txt.search("highlight", "saves/default/config.conf")
                    + '"Ollama-Aneki Kitty"'
                    + txt.search("alert", "saves/default/config.conf")
                    + "was made to be used in linux KITTY terminal "
                    + txt.search("highlight", "saves/default/config.conf")
                    + "b'cos of the icat command"
                )
                for i in range(len(history)):
                    if i % 2 == 0:
                        rprint("\n" + user_conversation + " " + history[i]["content"])
                    else:
                        rprint(Tables.table_without_emotion(history[i]["content"]))

    def ConinueFromWhereItLeft(self, logs):
        now = str(datetime.datetime.now())
        cpath = txt.search("custom_path", "saves/default/config.conf")
        models = (
            open(
                cpath + "/model-list.txt",
                "r",
            )
            .read()
            .split("\n")[:-1]
        )

        model_name = Prompt.ask(
            "Select Model: ",
            default=models[0],
            choices=models,
        )
        memory_list = []
        emotionlist = []
        with open(cpath + f"/models/{model_name}.json", "r") as file:
            memory_list = json.load(file)
            memory_list[0]["content"] += ". The current time is " + now

        with open(
            cpath + "/history/" + logs + ".json",
            "r",
        ) as history:
            history = json.load(history)[2:]
            choices = []
            print("\n")
            for i in range(int(len(history) / 2)):
                choices.append(str(i + 1))
                rprint(
                    txt.search("highlight", "saves/default/config.conf")
                    + str(i + 1)
                    + " "
                    + txt.search("normal", "saves/default/config.conf")
                    + history[i * 2]["content"]
                )
            print("\n")
            indexs = int(
                Prompt.ask(
                    "From where do you want to continue",
                    default=str(int(len(history) / 2)),
                    choices=choices,
                )
            )
            history = history[: (indexs) * 2]
            with open(cpath + "/history/" + logs + ".json", "w") as chats:
                for h in history:
                    memory_list.append(h)
                json.dump(memory_list, chats, indent=2)
            try:
                with open(
                    cpath + "/history/" + logs + "-emotions.json",
                    "r",
                ) as emotionlist:
                    emotionlist = json.load(emotionlist)
                    emotionlist = emotionlist[:indexs]
                    with open(
                        cpath + "/history/" + logs + "-emotions.json",
                        "w",
                    ) as emotion:

                        json.dump(emotionlist, emotion, indent=2)
            except:
                pass
        print("I am heree\n")
        max_respose_size = int(
            txt.search("max_respose_size", "saves/default/config.conf")
        )
        length = 2 * int(txt.search("memory_length", "saves/default/config.conf"))
        user_conversation = txt.search("user_conversation", "saves/default/config.conf")
        with open(cpath + f"/models/{model_name}.json", "r") as file:
            memory = json.load(file)
            memory[0]["content"] += ". The current time is " + now

            def length_ret(leng, hist):
                if leng < len(hist):
                    hist = hist[(len(hist) - leng) + 1 :]
                    new_hist = memory
                    for h in hist:
                        new_hist.append(h)
                    print(new_hist)
                    return new_hist
                else:
                    return hist

            history = memory_list
            self.read(logs)
            if int(txt.search("emotion_generation", "saves/default/config.conf")) >= 1:
                emotions = emotionlist
                model = ModelCatalog().load_model("slim-emotions-tool")

                width = int(txt.search("width", "saves/default/config.conf"))
                char, lines = shutil.get_terminal_size()
                pngPath = txt.search_image("joyful", cpath)
                png = Image.open(pngPath)
                height = (
                    int(width * png.height / png.width) + 1
                    if (
                        int(width * png.height / png.width)
                        != (width * png.height / png.width)
                    )
                    else int(width * png.height / png.width)
                )
                required_lines = requiredLines(png, width, char, lines)
                rectangle = str(width) + "x" + str(height) + "@" "2x" + str(
                    lines - required_lines - 3
                )
                space = ""
                for _ in range(required_lines):
                    for _ in range(width):
                        space += " "
                    space += "\n"


                if int(txt.search("auto_clear", "saves/default/config.conf")) >= 1:
                    subprocess.run(["clear"])
                    clear_kitty_image()
                    self.read(logs)
                user_input = input("\n" + user_conversation + " ")
                id = 0
                while (
                    user_input.lower()
                    != txt.search("exit_code", "saves/default/config.conf").lower()
                ):
                    id += 1
                    history.append({"role": "user", "content": user_input})
                    stream = ollama.chat(
                        model=model_name,
                        messages=length_ret(length, history),
                        stream=True,
                    )
                    msg = ""
                    flag = True
                    with Live(Table(), auto_refresh=True) as live:
                        response = "joyful"
                        for chunk in stream:
                            msg += chunk["message"]["content"]
                            live.update(Tables.table_with_emotion(msg, space))
                            if len(msg) > max_respose_size and flag:
                                response = model.function_call(msg)["llm_response"][
                                    "emotions"
                                ][0]
                                pngPath = txt.search_image(response, cpath)
                                flag = False
                    live.update(Tables.table_with_emotion(msg, space))
                    if flag or not flag:
                        if len(msg) > max_respose_size:
                            response = model.function_call(msg[: max_respose_size - 1])[
                                "llm_response"
                            ]["emotions"][0]
                        else:
                            response = model.function_call(msg)["llm_response"][
                                "emotions"
                            ][0]
                        pngPath = txt.search_image(response, cpath)
                        display_image(pngPath, rectangle, id=id)
                    for _ in range(required_lines + 2):
                        print("")
                    emotions.append(response)
                    with open(cpath + f"/history/{logs}-emotions.json", "w") as emotion:
                        json.dump(emotions, emotion, indent=2)

                    history.append(
                        {
                            "role": "assistant",
                            "content": msg,
                        }
                    )
                    with open(cpath + f"/history/{logs}.json", "w") as chats:
                        json.dump(history, chats, indent=2)

                    if (
                        int(
                            txt.search("reprint_everytime", "saves/default/config.conf")
                        )
                        >= 1
                    ):
                        subprocess.run(["clear"])
                        clear_kitty_image()
                        self.read(logs)
                    user_input = input("\n" + user_conversation + " ")
            else:
                self.read(logs)
                user_input = input("\n" + user_conversation + " ")
                while (
                    user_input.lower()
                    != txt.search("exit_code", "saves/default/config.conf").lower()
                ):
                    history.append({"role": "user", "content": user_input})
                    stream = ollama.chat(
                        model=model_name,
                        messages=length_ret(length, history),
                        stream=True,
                    )
                    msg = ""
                    with Live(Table(), auto_refresh=True) as live:
                        for chunk in stream:
                            msg += chunk["message"]["content"]
                            live.update(Tables.table_without_emotion(msg))
                    history.append(
                        {
                            "role": "assistant",
                            "content": msg,
                        }
                    )
                    with open(cpath + f"/history/{logs}.json", "w") as chats:
                        json.dump(history, chats, indent=2)
                    if (
                        int(
                            txt.search("reprint_everytime", "saves/default/config.conf")
                        )
                        >= 1
                    ):
                        subprocess.run(["clear"])
                        clear_kitty_image()
                        self.read(logs)
                    user_input = input("\n" + user_conversation + " ")

    def new_run(self, model_name):
        now = str(datetime.datetime.now())
        custom = txt.search("custom_path", "saves/default/config.conf")
        user_conversation = txt.search("user_conversation", "saves/default/config.conf")
        ask_for_Topic = (
            int(txt.search("ask_for_Topic", "saves/default/config.conf")) == 1
        )
        Topic = ""
        if ask_for_Topic:
            Topic = Prompt.ask("Save history with name: ", default=now)
            with open(custom + "/historylog.txt", "a") as historylog:
                historylog.write(f"{model_name}-{Topic}\n")
        else:
            with open(custom + "/historylog.txt", "a") as historylog:
                historylog.write(f"{model_name}-{now}\n")

        length = 2 * int(txt.search("memory_length", "saves/default/config.conf"))
        max_respose_size = int(
            txt.search("max_respose_size", "saves/default/config.conf")
        )
        Path(custom + "/history/").mkdir(parents=True, exist_ok=True)
        # subprocess.run(["clear"])
        with open(custom + f"/models/{model_name}.json", "r") as file:
            memory = json.load(file)
            memory[0]["content"] += ". The current time is " + now

            def length_ret(leng, hist):
                if leng < len(hist):
                    hist = hist[(len(hist) - leng) + 1 :]
                    new_hist = memory
                    for h in hist:
                        new_hist.append(h)
                    return new_hist
                else:
                    return hist

            history = []
            history.append(memory[0])
            history.append(memory[1])

            if int(txt.search("emotion_generation", "saves/default/config.conf")) >= 1:

                def requiredLines(img, width, char, lines):
                    buf = array.array("H", [0, 0, 0, 0])
                    fcntl.ioctl(1, termios.TIOCGWINSZ, buf)
                    displayresH = buf[3]
                    displayresW = buf[2]
                    try:
                        return int(
                            img.height
                            / (
                                ((img.width / width) / (displayresW / char))
                                * (displayresH / lines)
                            )
                        )
                    except:
                        rprint(
                            f"{txt.search('alert', 'saves/default/config.conf')} Are you sure you are using right terminal because we arn't getting precise height and width of terminal"
                        )

                emotions = []
                model = ModelCatalog().load_model("slim-emotions-tool")
                if int(txt.search("auto_clear", "saves/default/config.conf")) >= 1:
                    subprocess.run(["clear"])
                    clear_kitty_image()

                width = int(txt.search("width", "saves/default/config.conf"))
                char, lines = shutil.get_terminal_size()
                pngPath = txt.search_image("joyful", custom)
                png = Image.open(pngPath)
                height = (
                    int(width * png.height / png.width) + 1
                    if (
                        int(width * png.height / png.width)
                        != (width * png.height / png.width)
                    )
                    else int(width * png.height / png.width)
                )
                required_lines = requiredLines(png, width, char, lines)
                rectangle = str(width) + "x" + str(height) + "@" "2x" + str(
                    lines - required_lines - 3
                )
                space = ""
                for _ in range(required_lines):
                    for _ in range(width):
                        space += " "
                    space += "\n"
                for _ in range(lines):
                    print(" ")
                user_input = input("\n" + user_conversation + " ")
                id = 0
                while (
                    user_input.lower()
                    != txt.search("exit_code", "saves/default/config.conf").lower()
                ):
                    id += 1
                    history.append({"role": "user", "content": user_input})
                    stream = ollama.chat(
                        model=model_name,
                        messages=length_ret(length, history),
                        stream=True,
                    )
                    msg = ""
                    flag = True
                    with Live(Table(), auto_refresh=True) as live:
                        response = "joyful"
                        for chunk in stream:
                            msg += chunk["message"]["content"]
                            live.update(Tables.table_with_emotion(msg, space))
                            if len(msg) > max_respose_size and flag:
                                response = model.function_call(msg)["llm_response"][
                                    "emotions"
                                ][0]
                                pngPath = txt.search_image(response, custom)
                                flag = False
                    live.update(Tables.table_with_emotion(msg, space))
                    if flag or not flag:
                        if len(msg) > max_respose_size:
                            response = model.function_call(msg[: max_respose_size - 1])[
                                "llm_response"
                            ]["emotions"][0]
                        else:
                            response = model.function_call(msg)["llm_response"][
                                "emotions"
                            ][0]
                        pngPath = txt.search_image(response, custom)
                        display_image(pngPath, rectangle, id=id)
                    for _ in range(required_lines + 2):
                        print("")
                    emotions.append(response)
                    if ask_for_Topic:
                        with open(
                            custom + f"/history/{model_name}-{Topic}-emotions.json", "w"
                        ) as emotion:
                            json.dump(emotions, emotion, indent=2)

                    else:
                        with open(
                            custom + f"/history/{model_name}-{now}-emotions.json", "w"
                        ) as emotion:
                            json.dump(emotions, emotion, indent=2)

                    history.append(
                        {
                            "role": "assistant",
                            "content": msg,
                        }
                    )
                    if ask_for_Topic:
                        with open(
                            custom + f"/history/{model_name}-{Topic}.json", "w"
                        ) as chats:
                            json.dump(history, chats, indent=2)
                        if (
                            int(
                                txt.search(
                                    "reprint_everytime", "saves/default/config.conf"
                                )
                            )
                            >= 1
                        ):
                            subprocess.run(["clear"])
                            clear_kitty_image()
                            self.read(f"{model_name}-{Topic}")
                    else:
                        with open(
                            custom + f"/history/{model_name}-{now}.json", "w"
                        ) as chats:
                            json.dump(history, chats, indent=2)
                        if (
                            int(
                                txt.search(
                                    "reprint_everytime", "saves/default/config.conf"
                                )
                            )
                            >= 1
                        ):
                            subprocess.run(["clear"])
                            clear_kitty_image()
                            self.read(f"{model_name}-{now}")

                    user_input = input("\n" + user_conversation + " ")
            else:
                user_input = input("\n" + user_conversation + " ")
                while (
                    user_input.lower()
                    != txt.search("exit_code", "saves/default/config.conf").lower()
                ):
                    history.append({"role": "user", "content": user_input})
                    stream = ollama.chat(
                        model=model_name,
                        messages=length_ret(length, history),
                        stream=True,
                    )
                    msg = ""
                    with Live(Table(), auto_refresh=True) as live:
                        for chunk in stream:
                            msg += chunk["message"]["content"]
                            live.update(Tables.table_without_emotion(msg))
                    history.append(
                        {
                            "role": "assistant",
                            "content": msg,
                        }
                    )
                    if ask_for_Topic:
                        with open(
                            custom + f"/history/{model_name}-{Topic}.json", "w"
                        ) as chats:
                            json.dump(history, chats, indent=2)
                    else:
                        with open(
                            custom + f"/history/{model_name}-{now}.json", "w"
                        ) as chats:
                            json.dump(history, chats, indent=2)

                    user_input = input("\n" + user_conversation + " ")
