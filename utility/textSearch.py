from rich_pixels import Pixels


class txt:
    # This will search for attribute in given path of .txt file it follows some rules eg it will avoid every white spaces and comments which can be made with //
    def search(text, path):
        with open(path, "r") as txt:
            try:
                testlist = txt.readlines()
                for line in testlist:
                    line = line.replace(" ", "")
                    if line.__contains__("//"):
                        line = line[: line.index("//")]
                    if text == line[: len(text)]:
                        return line.replace("\n", "").replace(text + "=", "")
                raise
            except:
                print(f"Something({text}) is missing from {path}")
                raise ValueError

    # This will give image as path whether they are in custome folder or in default
    def search_image(emotion, custom_path, pngfolder):
        try:
            Pixels(custom_path + f"/exp/{emotion}.png")
            return custom_path + f"/exp/{emotion}.png"
        except:
            return "saves/default" + f"/exp/{pngfolder.lower()}/{emotion}.png"
