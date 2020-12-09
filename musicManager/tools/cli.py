import shutil


def setup_default_playlist(playlists :list) -> str:
    print("Please select the index of your default playlist:")

    for index, playlist in enumerate(playlists):
        print(f"""{index+1}.) {playlist}""")

    try:
        return playlists[int(input()) -1]

    except:
        print("Wrong input, exiting...")
        exit(1)

def format_time(max_seconds, curr_seconds):


    curr_m, curr_s = divmod(curr_seconds, 60)
    max_m, max_s = divmod(max_seconds, 60)

    #return f"{int(max_m)}:{int(max_s)}|{int(curr_m)}:{int(curr_s)}"
    return (f"{int(curr_m):02d}:{int(curr_s):02d}/{int(max_m):02d}:{int(max_s):02d}")

# src: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console,
# slightly modified from: https://gist.github.com/greenstick/b23e475d2bfdc3a82e34eaa1f6781ee4
def printProgressBar (percentage, prefix ='', suffix ='', decimals = 1, length = 100, fill ='█', autosize=True):
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
    if autosize:
        cols, _ = shutil.get_terminal_size(fallback = (length, 1))
        length = cols - len(styling)
    filledLength = int(length * percentage // 100.0)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s' % styling.replace(fill, bar), end = '\r')
    # Print New Line on Complete
    if percentage == 100.0:
        print()