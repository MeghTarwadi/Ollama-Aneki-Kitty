from rich import box
from rich import print as rprint
from rich.table import Table

from utility.textSearch import txt


def box_type():
    if (txt.search("box_borders", "saves/default/config.conf")) == "HEAVY":
        return box.HEAVY
    elif (txt.search("box_borders", "saves/default/config.conf")) == "DOUBLE":
        return box.DOUBLE
    elif (txt.search("box_borders", "saves/default/config.conf")) == "ROUNDED":
        return box.HEAVY
    elif (txt.search("box_borders", "saves/default/config.conf")) == "SQUARE":
        return box.SQUARE
    else:
        return box.SIMPLE


class Tables:
    def __init__(self):
        pass

    def center_table(text):
        width = 0
        if int(txt.search("box_width", "saves/default/config.conf")) == 0:

            table = Table(show_header=False, safe_box=True, box=box_type(), expand=True)
        else:
            width = int(txt.search("box_width", "saves/default/config.conf"))
            table = Table(
                show_header=False,
                safe_box=True,
                box=box_type(),
                width=width,
            )
        table.add_column("", justify="center", no_wrap=True)
        table.add_row(text + "\n")
        rprint(table)

    def normal_table(text):
        width = 0
        if int(txt.search("box_width", "saves/default/config.conf")) == 0:

            table = Table(show_header=False, safe_box=True, box=box_type(), expand=True)
        else:
            width = int(txt.search("box_width", "saves/default/config.conf"))
            table = Table(
                show_header=False,
                safe_box=True,
                box=box_type(),
                width=width,
            )
        table.add_column("", no_wrap=False)
        table.add_row(text)
        rprint(table)

    def multi_table(text):
        width = 0

        if int(txt.search("box_width", "saves/default/config.conf")) == 0:
            tb = Table(show_footer=False, safe_box=True, box=None, expand=True)
        else:
            width = int(txt.search("box_width", "saves/default/config.conf"))
            tb = Table(
                show_footer=False,
                safe_box=True,
                box=None,
                width=width,
            )

        for i in text:
            table = None
            table = Table(show_header=True, safe_box=True, box=box_type(), expand=True)
            table.add_column(i[0], no_wrap=False, ratio=1, justify="center")
            for j in i[1:]:
                table.add_row(j)
            tb.add_column(table, ratio=1, justify="center", no_wrap=False)

        rprint(tb)

    def table_with_emotion(text, emotion):
        width = 0
        if int(txt.search("box_width", "saves/default/config.conf")) == 0:
            table = Table(show_header=False, safe_box=True, box=box_type(), expand=True)
        else:
            width = int(txt.search("box_width", "saves/default/config.conf"))

            table = Table(
                show_header=False,
                safe_box=True,
                box=box_type(),
                width=width,
            )

        table.add_column(
            "emotion",
            width=int(txt.search("width", "saves/default/config.conf")),
            overflow="fold",
            no_wrap=True,
            justify="left",
            vertical="middle",
        )
        table.add_column(
            "text", vertical="middle", no_wrap=False, justify="left", ratio=1
        )
        table.add_row(emotion, txt.search("normal", "saves/default/config.conf") + text)

        return table

    def table_without_emotion(text):
        width = 0
        width = 0
        if int(txt.search("box_width", "saves/default/config.conf")) == 0:

            table = Table(show_header=False, safe_box=True, box=box_type(), expand=True)
        else:
            width = int(txt.search("box_width", "saves/default/config.conf"))
            table = Table(
                show_header=False,
                safe_box=True,
                box=box_type(),
                width=width,
            )
        table.add_column("", no_wrap=False)
        table.add_row(text)

        return table
