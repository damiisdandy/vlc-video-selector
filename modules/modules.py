import os


# Get all Top Most Directories In A Directory
def getTopFolders(_path):
    all_root_dirs = set()
    for root, _, __ in os.walk(_path):
        # Get Relative Path To All Directories in Specified Directory
        # Then Create A List Of Inner Directories
        folder = root.replace(_path, '').split('/')
        if len(folder) > 1:
            # Add Root Directories Into A Set To Avoid Repetition
            all_root_dirs.add(folder[1])
    return list(all_root_dirs)


def AllFilesInDir(path):
    index = -1
    rootlist = []
    filelist = []
    allfiles = []
    for root, _, files in os.walk(path):
        # FULL PATH OF ALL DIRECTORIES
        rootlist.append(root)
        # ALL FILES IN EVERY DIRECTORY
        filelist.append(files)

    #  TO FIND FULLPATH FOR ALL FILES IN DIRECTORY
    for root in rootlist:
        index += 1
        for filex in filelist[index]:
            filename = root + '/' + filex
            allfiles.append(filename)
    return allfiles


class Colors:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    UNDERLINE = "\033[4m"
    BOLD = "\033[1m"
    ENDC = "\033[0m"
