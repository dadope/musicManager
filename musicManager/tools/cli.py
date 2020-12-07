def setup_default_playlist(playlists :list) -> str:
    print("Please select the index of your default playlist:")

    for index, playlist in enumerate(playlists):
        print(f"""{index+1}.) {playlist}""")

    try:
        return playlists[int(input()) -1]

    except:
        print("Wrong input, exiting...")
        exit(1)