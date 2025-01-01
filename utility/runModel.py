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


# This fuction returns the number of lines required to display the image since
# the terminal calculates pixels diffrenetly and icat uses diffrent methods to
# do so but since its in terminal its needed to find precise lines needed for this
# bcos if we scaled down image with icat than its minimum side will be assigned to
# main line eg. vericle lines of rows or horizontal lines of columns number of
# columns of characters in ollama aneki its made that way so that every time the
# horizontal lines of columns number of columns of characters gets the minimum size.
def requiredLines(img, width, char, lines):
    buf = array.array("H", [0, 0, 0, 0])
    fcntl.ioctl(1, termios.TIOCGWINSZ, buf)
    displayresH = buf[3]
    displayresW = buf[2]
    return int(
        img.height
        / (((img.width / width) / (displayresW / char)) * (displayresH / lines))
    )


# This fuction clears the kitty terminal since images cant be cleared with simple clear
def clear_kitty_image():
    subprocess.run(["clear"])
    sys.stdout.write("\033c")
    sys.stdout.flush()


# This fuction displays image in kitty terminal at required location with required parameters
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

    # Its used to read the past conversation
    def read(self, logs):
        # Loading previous conversations titles
        pngfolder = txt.search("pngfolder", "saves/default/config.conf")
        cpath = txt.search("custom_path", "saves/default/config.conf")
        with open(
            cpath + "/history/" + logs + ".json",
            "r",
        ) as history:
            history = json.load(history)[2:]
            user_conversation = txt.search(
                "user_conversation", "saves/default/config.conf"
            )
            current = 0

            # There is a big reason to use try and except here it is because if user has previously enebled the emotion
            # generation than desabled it and currently its active so its like first 5 conversation has emotions now again
            # 5 doesnt has emotions but remaining 5 which were added lastly by aneki run cont hence it will throw an error
            # so to manage that because there are total 15 and emotions are 10 only to show conversation without emotions
            try:
                if (
                    int(txt.search("emotion_generation", "saves/default/config.conf"))
                    < 1
                ):
                    raise
                # getting emotions from where its been stored
                with open(
                    cpath + "/history/" + logs + "-emotions.json",
                    "r",
                ) as emotionlist:
                    emotionlist = json.load(emotionlist)
                    j = 0
                    # Get measures of terminal in a way that shows how many charactes can be entered and
                    # how many enters do be needed to be hitten in order to get to new line or screen
                    char, lines = shutil.get_terminal_size()
                    width = int(txt.search("width", "saves/default/config.conf"))
                    # To make curser touch the bottom
                    for _ in range(lines):
                        print("")
                    for i in range(current, int(len(history) / 2)):
                        rprint("\n" + user_conversation + " " + history[j]["content"])
                        pngPath = txt.search_image(emotionlist[i], cpath, pngfolder)
                        png = Image.open(pngPath)
                        # Required lines kitty terminal in terms of number of lines
                        required_lines = requiredLines(png, width, char, lines)
                        # Rectangle for icat to get position in x,y and sizes of png
                        rectangle = str(width) + "x" + str(
                            required_lines
                        ) + "@" "2x" + str(int(lines - required_lines - 5))
                        # Since we need to tell table to place some spaces for image we are passing that as empty spaces in
                        # such a way that it will be equal to required lines and of width so that it take up whole space as png
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
                        # This will display pngs
                        display_image(pngPath, rectangle, i)
                        for _ in range(required_lines + 1):
                            print("")
                        current = j
                        j += 2
                        print("\n")
            # If emotion generation is disabled or some error happens in finding emotions in file eg. missing 1 outof 5 emotion
            except:
                rprint(
                    txt.search("highlight", "saves/default/config.conf")
                    + '"Ollama-Aneki Kitty"'
                    + txt.search("alert", "saves/default/config.conf")
                    + "was made to be used in linux KITTY terminal "
                    + txt.search("highlight", "saves/default/config.conf")
                    + "b'cos of the icat command"
                )
                for i in range(current, len(history)):
                    if i % 2 == 0:
                        rprint("\n" + user_conversation + " " + history[i]["content"])
                    else:
                        rprint(Tables.table_without_emotion(history[i]["content"]))

    # It will allow to continue from where we left the conversation and with or without the same model as previous
    def ConinueFromWhereItLeft(self, logs):
        pngfolder = txt.search("pngfolder", "saves/default/config.conf")

        # Since ollama aneki makes model aware about time
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
        # It will ask user to select model from models which is the list of all models so that
        # user can continue from where he left and which which ever model he wants
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
        # What if user wants to continue from the previous promt instead of current promt
        # Aneki gatchu sicne aneki asks from which pormt user wants to continue
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
            # since user is using llm user might be lazzy hence user doesnt want to write whole
            # promt aneki simplifies by asking them based on index
            indexs = int(
                Prompt.ask(
                    "From where do you want to continue",
                    default=str(int(len(history) / 2)),
                    choices=choices,
                )
            )
            # new history has been created based on from where user wants to continue
            history = history[: (indexs) * 2]
            with open(cpath + "/history/" + logs + ".json", "w") as chats:
                for h in history:
                    memory_list.append(h)
                json.dump(memory_list, chats, indent=2)
            try:
                # checks whether emotions have been stored or not
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
        max_respose_size = int(
            txt.search("max_respose_size", "saves/default/config.conf")
        )
        length = 2 * int(txt.search("memory_length", "saves/default/config.conf"))
        user_conversation = txt.search("user_conversation", "saves/default/config.conf")
        with open(cpath + f"/models/{model_name}.json", "r") as file:
            memory = json.load(file)
            memory[0]["content"] += ". The current time is " + now

            # It will return history based on memory_length
            def length_ret(leng, hist):
                if leng < len(hist):
                    hist = hist[(len(hist) - leng) + 1 :]
                    new_hist = memory
                    for h in hist:
                        new_hist.append(h)
                    return new_hist
                else:
                    return hist

            history = memory_list
            self.read(logs)
            if int(txt.search("emotion_generation", "saves/default/config.conf")) >= 1:
                # Calling emotion generation model
                emotions = emotionlist
                model = ModelCatalog().load_model("slim-emotions-tool")
                width = int(txt.search("width", "saves/default/config.conf"))
                char, lines = shutil.get_terminal_size()
                pngPath = txt.search_image("joyful", cpath, pngfolder)
                png = Image.open(pngPath)
                required_lines = requiredLines(png, width, char, lines)
                rectangle = str(width) + "x" + str(required_lines) + "@" "2x" + str(
                    lines - required_lines - 3
                )
                # Since we need to tell table to place some spaces for image we are passing that as empty spaces in
                # such a way that it will be equal to required lines and of width so that it take up whole space as png
                space = ""
                for _ in range(required_lines):
                    for _ in range(width):
                        space += " "
                    space += "\n"

                if int(txt.search("auto_clear", "saves/default/config.conf")) >= 1:
                    clear_kitty_image()
                    self.read(logs)
                user_input = input("\n" + user_conversation + " ")
                id = 0
                while (
                    user_input.lower()
                    != txt.search("exit_code", "saves/default/config.conf").lower()
                ):
                    id += 1
                    # to make prompt and history understandable by llm of ollama aneki uses this formate ({"role": "user", "content": user_input})
                    history.append({"role": "user", "content": user_input})
                    stream = ollama.chat(
                        model=model_name,
                        messages=length_ret(length, history),
                        stream=True,
                    )
                    msg = ""
                    with Live(Table(), auto_refresh=True) as live:

                        response = "joyful"
                        for chunk in stream:
                            msg += chunk["message"]["content"]
                            live.update(Tables.table_with_emotion(msg, space))

                    if len(msg) > max_respose_size:
                        response = model.function_call(msg[: max_respose_size - 1])[
                            "llm_response"
                        ]["emotions"][0]
                    else:
                        response = model.function_call(msg)["llm_response"]["emotions"][
                            0
                        ]
                    pngPath = txt.search_image(response, cpath, pngfolder)
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
                        clear_kitty_image()
                        self.read(logs)
                    user_input = input("\n" + user_conversation + " ")

    def new_run(self, model_name):
        pngfolder = txt.search("pngfolder", "saves/default/config.conf")
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
                    clear_kitty_image()

                width = int(txt.search("width", "saves/default/config.conf"))
                char, lines = shutil.get_terminal_size()
                pngPath = txt.search_image("joyful", custom, pngfolder)
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
                    print("")
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
                                pngPath = txt.search_image(response, custom, pngfolder)
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
                        pngPath = txt.search_image(response, custom, pngfolder)
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
