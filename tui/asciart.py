import random


class asciiArt:

    def LoadArt(index, path):
        Ascii_Art = []
        path = path + "/art.txt"
        try:
            with open(path, "r") as file:
                Ascii_Art = file.read().split("\n\n\n\n")
        except:
            with open("saves/default/art.txt", "r") as file:
                Ascii_Art = file.read().split("\n\n\n\n")
                

        # will return rencomly
        if index < 0:
            return Ascii_Art[random.randint(0, len(Ascii_Art)-2)]

        # will return as indexed
        else:
            if index < len(Ascii_Art):
                return Ascii_Art[index]
            else:
                return "Index is out of range...\n" + Ascii_Art[index % len(Ascii_Art)]
