import os
import sys
import shutil

# hides the cursor for a better user experience
# src: https://stackoverflow.com/questions/5174810/how-to-turn-off-blinking-cursor-in-command-window
if os.name == 'nt':
    import ctypes

    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]

def hide_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

def show_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

def clear_screen():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")

def setup_default_playlist(playlists :list) -> str:
    print("Please select the index of your default playlist:")

    for index, playlist in enumerate(playlists):
        print(f"""{index+1}.) {playlist}""")

    try:
        result = int(input()) -1
        clear_screen()
        return playlists[result]

    except:
        print("Wrong input, exiting...")
        exit(1)


def format_time(max_seconds, curr_seconds):
    curr_m, curr_s = divmod(curr_seconds, 60)
    max_m, max_s = divmod(max_seconds, 60)

    return f"{int(curr_m):02d}:{int(curr_s):02d}/{int(max_m):02d}:{int(max_s):02d}"


# src: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console,
# slightly modified from: https://gist.github.com/greenstick/b23e475d2bfdc3a82e34eaa1f6781ee4
def printProgressBar(percentage, prefix='', suffix='', decimals=1, fill ='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        autosize    - Optional  : automatically resize the length of the progress bar to the terminal window (Bool)
    """

    percent = ("{0:." + str(decimals) + "f}").format(100 * (percentage / 100.0))
    styling = '%s |%s| %s%% %s' % (prefix, fill, percent, suffix)
    cols, _ = shutil.get_terminal_size(fallback=(100, 1))
    length = cols - len(styling)
    filledLength = int(length * percentage // 100.0)
    bar = fill * filledLength + ' ' * (length - filledLength)
    print('\r%s' % styling.replace(fill, bar), end = '\r')
    # Print New Line on Complete
    if percentage == 100.0:
        print()


hide_cursor()