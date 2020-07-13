from os import system, name


tab = "       "
linebreak = "\n{}{}\n".format(tab, 30 * "_")

journal = "doi:                  10.1101/2020.07.03.186387"
git = "repo:                 https://github.com/simonarvin/eyeloop"


def clear() -> None:
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def logo(version: str, label="") -> str:
    logo_msg = fr"""
                                >> {label}

     ___      ___       __   __   __
    |__  \ / |__  |    /  \ /  \ |__)
    |___  |  |___ |___ \__/ \__/ |

                                  v{version}
                                           """
    return logo_msg


def welcome(version, label="") -> None:
    clear()
    msg = fr"""
    {logo(label, version)}
    Developed by Simon Arvin
    Yonehara Laboratory
    Danish Research Institute of
    Translational Neuroscience (DANDRITE)

    {git}
    {journal}{linebreak}"""
    print(msg)
