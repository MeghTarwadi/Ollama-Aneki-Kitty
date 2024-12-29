import subprocess
import sys

from rich import print as rprint
from rich.prompt import Prompt

from run import RunModel
from tui.asciart import asciiArt
from utility.ascimerge import AsciiMerge
from utility.model import createModel
from utility.richtables import Tables
from utility.textSearch import txt

auto_clear = bool((int(txt.search("auto_clear", "saves/default/config.conf"))))

asciiart = txt.search("asciiart", "saves/default/config.conf")
normal = txt.search("normal", "saves/default/config.conf")
highlight = txt.search("highlight", "saves/default/config.conf")
alert = txt.search("alert", "saves/default/config.conf")
user = ""
if auto_clear:
    subprocess.run(["clear"])
Tables.center_table(
    asciiart
    + asciiArt.LoadArt(
        int(txt.search("asciiart_index", "saves/default/config.conf")),
        txt.search("custom_path", "saves/default/config.conf"),
    )
)
print("\n")
flag = True
while user != "exit":
    try:
        if flag and sys.argv[1] in [
            "run",
            "help",
            "exit",
            "new",
            "history",
            "asciiart",
            "pixelize",
        ]:
            user = sys.argv[1]
            flag = False
        else:
            raise
    except:
        flag = False
        user = Prompt.ask(
            "",
            default="new",
            choices=["new", "history", "run", "asciiart", "help", "exit"],
        )

    if auto_clear:
        subprocess.run(["clear"])
    if user == "run":
        history = True
        try:
            open(
                txt.search("custom_path", "saves/default/config.conf")
                + "/historylog.txt",
                "r",
            ).read().split("\n")[:-1]

        except:
            history = False

        def call_fun(mode):
            runmodel = RunModel()
            if mode == "read" or mode == "cont":
                logs = (
                    open(
                        txt.search("custom_path", "saves/default/config.conf")
                        + "/historylog.txt",
                        "r",
                    )
                    .read()
                    .split("\n")[:-1]
                )
                choices = []
                print("\n")
                for c in range(len(logs)):
                    rprint(f"{highlight} {c + 1}. {normal} {logs[c]}")
                    choices.append(str(c + 1))
                print("\n")
                index = Prompt.ask(
                    "Title of past coversation : ",
                    default=choices[0],
                    choices=choices,
                )
                if mode == "read":
                    runmodel.read(logs[int(index) - 1])
                else:
                    runmodel.ConinueFromWhereItLeft(logs[int(index) - 1])
            else:
                runmodel.new_run(mode)

        try:
            available_option = (
                open(
                    txt.search("custom_path", "saves/default/config.conf")
                    + "/model-list.txt",
                    "r",
                )
                .read()
                .split("\n")[:-1]
            )
            if history:
                available_option.append("read")
                available_option.append("cont")
            if sys.argv[2] in available_option:
                mode = sys.argv[2]
                call_fun(mode)
                sys.argv[2] = ""
            else:
                raise
        except:
            try:
                available_option = (
                    open(
                        txt.search("custom_path", "saves/default/config.conf")
                        + "/model-list.txt",
                        "r",
                    )
                    .read()
                    .split("\n")[:-1]
                )
                if history:
                    available_option.append("read")
                    available_option.append("cont")
                mode = Prompt.ask(
                    "Model Name: ",
                    default=(
                        open(
                            txt.search("custom_path", "saves/default/config.conf")
                            + "/model-list.txt",
                            "r",
                        )
                        .read()
                        .split("\n")[:-1]
                    )[0],
                    choices=available_option,
                )
                call_fun(mode)
            except Exception as e:
                print(e)
                rprint(
                    f"{alert}No custome model found! Please create custome model using{alert.replace('[', '[/')} {highlight}'new'{highlight.replace('[', '[/')} {alert} command first!{alert.replace('[', '[/')}"
                )

    elif user == "help":
        text = []
        rprint(
            f"{normal}Welcome to the help section! Here’s a brief overview of the commands available:{normal.replace('[', '[/')} "
        )
        text = [
            [
                f"{highlight}run{highlight.replace('[', '[/')}",
                "Launch a model by name.",
                "If it exists, it will run.",
                f"{alert}Make sure the model is available!{alert.replace('[', '[/')}",
            ],
            [
                f"{highlight}exit{highlight.replace('[', '[/')}",
                "Exit the setup program.",
                "All progress is saved automatically.",
                f"{alert}You can return later to continue!{alert.replace('[', '[/')}",
            ],
            [
                f"{highlight}new{highlight.replace('[', '[/')}",
                "Create a new custom model.",
                "Base it on an existing model.",
                f"{alert}Choose a unique name for it!{alert.replace('[', '[/')}",
            ],
            [
                f"{highlight}history{highlight.replace('[', '[/')}",
                "View past model configurations.",
                "Even deleted ones can be restored.",
                f"{alert}Recreate them if needed!{alert.replace('[', '[/')}",
            ],
            [
                f"{highlight}asciiart{highlight.replace('[', '[/')}",
                "Merge two ASCII arts.",
                "To saperate two ascii use enters three times.",
                f"{alert}Only ascii1.txt allows multiple art!{alert.replace('[', '[/')}",
            ],
        ]
        Tables.multi_table(text)
        rprint(f"{normal}Feel free to ask for help anytime!{normal.replace('[', '[/')}")
    elif user == "asciiart":
        AsciiMerge.merge()
    elif user == "exit":
        print("Exiting...")
    elif user == "new":
        createModel.NewModel()
    elif user == "history":
        createModel.History()
    else:
        pass
    print("\n")
