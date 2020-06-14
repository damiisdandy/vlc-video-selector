from modules.modules import getTopFolders, AllFilesInDir, Colors
import os
import sys

# create medium to know if vlc is stored
try:
    PLATFORM = sys.platform
    SUPPORTED_VIDEO_FORMATS = ['.mp4', '.mkv', '.avi', '.flv', '.mov', '.webm', '.3gp']
    if PLATFORM != 'linux':
        print(Colors.BOLD + Colors.RED + "❌ Sorry This Program Currently Only Works For Linux Distributions" + Colors.ENDC)
        exit()

    # Know if vlc is installed on computer
    # Coming Soon

    while True:
        ParentPath = input(Colors.BOLD + "Where can we find your Video Folder? " + Colors.ENDC)
        # Check If Directory Exists
        it_exist = os.path.exists(ParentPath)
        if it_exist:
            break
        else:
            print(Colors.BOLD + Colors.RED + "❌ The Folder You Typed In Does Not Exist! Try To Specify The Absolute Path ("
                                             "e.g "
                                             "/home/{"
                                             "your_username}/Videos)" + Colors.ENDC)

    dirs = getTopFolders(ParentPath)
    if dirs:
        print(Colors.BOLD + Colors.CYAN + "Here Are The Folder(s) We Found" + Colors.ENDC)
        print("\n")
        for _dir in dirs:
            print("==> " + Colors.BOLD + Colors.BLUE + _dir + Colors.ENDC)
        print("\n")

        while True:
            selected_dir = input(Colors.BOLD + "Type In The Name Of The Directory You Want To Play Videos From: "
                                               "" + Colors.ENDC)
            selected_dir = os.path.join(ParentPath, selected_dir)
            it_exist = os.path.exists(selected_dir)
            if it_exist:
                break
            else:
                print(Colors.BOLD + Colors.RED + " ❌ The Folder You Typed In Does Not Exist! Try To Copy And Paste The "
                                                 "Folder Name From The List Above" + Colors.ENDC)
        all_files_raw = AllFilesInDir(selected_dir)
    else:
        print(
            Colors.BOLD + Colors.YELLOW + "There Are No Directories In This Directory So We Are Going To Search For Videos "
                                          "Instead" + Colors.ENDC)
        all_files_raw = AllFilesInDir(ParentPath)

    all_videos = []
    for file in all_files_raw:
        # Get File Extension
        ext = os.path.splitext(file)[-1]
        # Check If Its A Video
        if ext.lower() in SUPPORTED_VIDEO_FORMATS:
            all_videos.append(file)
        else:
            print(Colors.BOLD + Colors.YELLOW + f"\nFile => "
                                                f"{file.split('/')[-1]} Isn't Going To Be Added Because Its An Unsupported "
                                                f"Format" + Colors.ENDC)

    video_count = len(all_videos)
    if video_count < 1:
        print(Colors.BOLD + Colors.RED + "❌ No Video Of Supported Format Was Found... Exiting Program" + Colors.ENDC)
        exit()
    print(Colors.BOLD + Colors.CYAN + f"\nWe Found A Total Of {video_count} Video(s)" + Colors.ENDC)

    while True:
        try:
            video_num = int(input(Colors.BOLD + f"How Many Videos Do You Want To Add To The VLC Playlist: " + Colors.ENDC))
            if video_num < 1:
                print(Colors.BOLD + Colors.RED + "❌ You Typed In 0 or A Negative Number! (This Will Close The Program) "
                                                 "Program Closing..." + Colors.ENDC)
                exit()
            else:
                if video_num > video_count:
                    print(Colors.BOLD + Colors.RED + f"❌ You Types In A Number Greater Than The Number Of Available "
                                                     f"Videos, "
                                                     f"Please Type A Number From "
                          f"1-{video_count}" + Colors.ENDC)
                else:
                    break
        except ValueError:
            print(Colors.BOLD + Colors.RED + f"❌ Hmmmm, Seems Like You Did Not Input A Number, Please Type A Number From "
                                             f"1-{video_count}" + Colors.ENDC)

    if video_num == 1:
        all_videos.sort()
        video_to_be_played = all_videos[0]
        print(Colors.BOLD + Colors.GREEN + f"Playing Video => {video_to_be_played.split('/')[-1]}" + Colors.ENDC)
        os.system(f'vlc "{video_to_be_played}"')

    else:
        while True:
            display_type = input(Colors.BOLD + "How Do You Want The Videos To Be Played, At Random or Linearly (R for "
                                               "Random and L for "
                                               "Linearly): " + Colors.ENDC)
            if display_type.lower() == 'r' or display_type.lower() == 'l':
                display_type = display_type.lower()
                break
            else:
                print(Colors.BOLD + Colors.GREEN + "Wrong Option!, Please Type in Either R or L" + Colors.ENDC)

        all_videos.sort()
        videos_to_be_played = all_videos[:video_num]

        # Create Code To Be Executed In The Terminal
        output = ""
        for video in videos_to_be_played:
            output += f' "{video}"'
            print(Colors.BOLD + Colors.GREEN + f"Playing Video => {video.split('/')[-1]}" + Colors.ENDC)

        # Get Videos and Arrange Them Accordingly
        if display_type == 'r':
            bash_code = f"vlc -Z {output}"
        else:
            bash_code = f"vlc {output}"

        # Store Code In BashFile
        with open(".playvideo.sh", "w") as f_obj:
            f_obj.write(bash_code)

        # Execute Code in Terminal
        os.system('bash .playvideo.sh')
except KeyboardInterrupt:
    print('\n' + Colors.BOLD + Colors.GREEN + "Program Closed Succesfully" + Colors.ENDC)
