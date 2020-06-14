from modules.modules import *
import os
import sys


# create medium to know if vlc is stored
PLATFORM = sys.platform
SUPPORTED_VIDEO_FORMATS = ['.mp4', '.mkv', '.avi', '.flv', '.mov', '.webm', '.3gp']

if PLATFORM != 'linux':
    print("Sorry This Program Currently Only Works For Linux Distributions")
    exit()

# Know if vlc is installed on computer
while True:
    ParentPath = input("Where can we find your Video Folder? ")
    # Check If Directory Exists
    it_exist = os.path.exists(ParentPath)
    if it_exist:
        break
    else:
        print("The Folder You Typed In Does Not Exist! Try To Specify The Absolute Path (e.g /home/{"
              "your_username}/Videos")


dirs = getTopFolders(ParentPath)
if dirs:
    print("Here Are The Folders We Found")
    print("\n")
    for _dir in dirs:
        print("==> " + _dir + "")
    print("\n")

    while True:
        selected_dir = input("Type In The Name Of The Directory You Want To Play Videos From: ")
        selected_dir = os.path.join(ParentPath, selected_dir)
        it_exist = os.path.exists(selected_dir)
        if it_exist:
            break
        else:
            print("The Folder You Typed In Does Not Exist! Try To Copy And Paste The Folder Name From The List Above")
    all_files_raw = AllFilesInDir(selected_dir)
else:
    print("There Are No Directories In This Directory So We Are Going To Search For Videos Instead")
    all_files_raw = AllFilesInDir(ParentPath)

all_videos = []
for file in all_files_raw:
    # Get File Extension
    ext = os.path.splitext(file)[-1]
    # Check If Its A Video
    if ext.lower() in SUPPORTED_VIDEO_FORMATS:
        all_videos.append(file)
    else:
        print(f"\nFile {file} Isn't Going To Be Added Because Its An Unsupported Format")

video_count = len(all_videos)
if video_count < 1:
    print("No Video Of Supported Format Was Found :( , Exitting Program")
    exit()
print(f"\nWe Found A Total Of {video_count} Video(s)")

while True:
    try:
        video_num = int(input(f"How Many Videos Do You Want To Add To The VLC Playlist: "))
        if video_num < 1:
            print("You Typed In 0 or A Negative Number! (This Will Close The Program)")
            exit()
        else:
            if video_num > video_count:
                print(f"You Types In A Number Greater Than The Number Of Available Videos, Please Type A Number From "
                      f"1-{video_count}")
            else:
                break
    except ValueError:
        print(f"Hmmmm, Seems Like You Did Not Input A Number, Please Type A Number From 1-{video_count}")

if video_num == 1:
    print("Play One Video")
else:
    while True:
        display_type = input("How Do You Want The Videos To Be Played, At Random or Linearly (R for Random and L for "
                             "Linearly): ")
        if display_type.lower() == 'r' or display_type.lower() == 'l':
            display_type = display_type.lower()
            break
        else:
            print("Wrong Option!, Please Type in Either R or L")

    all_videos.sort()
    videos_to_be_played = all_videos[:video_num]

    # Create Code To Be Executed In The Terminal
    output = ""
    for video in videos_to_be_played:
        output += f' "{video}"'
        print(f"Playing Video {video}")

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
