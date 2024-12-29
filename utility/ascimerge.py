# Use this to recreate ascii art if you want to add or remove any of them
from pathlib import Path

from utility.textSearch import txt


class AsciiMerge:
    def merge():
        asciis1_path = txt.search("asciis1_path", "saves/default/config.conf")
        arts = open(asciis1_path, "r").read().split("\n\n\n")

        #
        # CUSTOM TEXTS
        #
        ascii2_path = txt.search("ascii2_path", "saves/default/config.conf")
        Aneki = open(ascii2_path, "r").read()

        def ascii_art(fulllarge, fullshort):
            outcome = ""
            short = fullshort.split("\n")
            large = fulllarge.split("\n")
            min = int(len(large) / 2 - len(short) / 2) - 1
            max = int(len(large) / 2 + len(short) / 2)
            i, j = 0, 0
            for lrg in large:
                if j < len(short) and len(short[j]) < 2:
                    j += 1
                outcome += lrg + "\t\t"
                if min + 1 < i and max + 1 > i and j < len(short):
                    outcome += short[j]
                    j += 1
                else:
                    for _ in range(len(short[1])):
                        outcome += " "
                i += 1
                outcome += "ㅤ"
                outcome += "\n"
            return outcome

        file = ""
        for art in arts:
            if (len(Aneki.split("\n")) - len(art.split("\n"))) < 0:
                file += ascii_art(art, Aneki) + "\n\n\n"
            else:
                file += ascii_art(Aneki, art) + "\n\n\n"

        with open("saves/default/art.txt", "r") as txtfile:
            if file == txtfile.read():
                print("Default Ascii art detected, skipping...")
            else:
                print("Custom Ascii art detected, adding into custom...")
                Path(txt.search("custom_path", "saves/default/config.conf")).mkdir(
                    parents=True, exist_ok=True
                )
                with open(
                    txt.search("custom_path", "saves/default/config.conf") + "/art.txt",
                    "w",
                ) as customtxtfile:
                    customtxtfile.write(file)
