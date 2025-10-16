from installer import Installer
from packages import CATEGORIES, ENVIRONMENTS, BROWSERS, DEV_TOOLS, EMAIL_CLIENTS, ENCRYPTION_TOOLS, FILE_MANAGERS, GAMING_PACKAGES, MULTIMEDIA_TOOLS, NOTE_TAKING_APPS, TERMINALS
from screen import Screen

screen = Screen()
installer = Installer()

STARTING_INSTRUCTIONS = [
    "Pick what you would like to install!",
    "Press 'Space' or 'Enter' to toggle selection.",
    "Press 'F' to finish selecting packages."
]

browsers = []
environment = []
dev_tools = []
email_clients = []
encryption_tools = []
file_managers = []
gaming_packages = []
multimedia_tools = []
note_taking_apps = []
terminals = []

environment = screen.display_menu(ENVIRONMENTS, STARTING_INSTRUCTIONS)

for env in ENVIRONMENTS:
    if environment[0] == env["Name"]:
        env_pkgs = env["Debian_Packages"]

while True:
    input = screen.display_categories(CATEGORIES)
    if input[0] == "Finish":
        break

    match input[0]:
        case "Browsers":
            browsers = screen.display_menu(BROWSERS, STARTING_INSTRUCTIONS)
        case "Dev Tools":
            dev_tools = screen.display_menu(DEV_TOOLS, STARTING_INSTRUCTIONS)
        case "E-mail Clients":
            email_clients = screen.display_menu(EMAIL_CLIENTS, STARTING_INSTRUCTIONS)
        case "Encryption Tools":
            encryption_tools = screen.display_menu(ENCRYPTION_TOOLS, STARTING_INSTRUCTIONS)
        case "File Managers":
            file_managers = screen.display_menu(FILE_MANAGERS, STARTING_INSTRUCTIONS)
        case "Gaming Packages":
            gaming_packages = screen.display_menu(GAMING_PACKAGES, STARTING_INSTRUCTIONS)
        case "Multimedia Tools":
            multimedia_tools = screen.display_menu(MULTIMEDIA_TOOLS, STARTING_INSTRUCTIONS)
        case "Note Taking Tools":
            note_taking_apps = screen.display_menu(NOTE_TAKING_APPS, STARTING_INSTRUCTIONS)
        case "Terminals":
            terminals = screen.display_menu(TERMINALS, STARTING_INSTRUCTIONS)
        case _:
            pass

ENVIRONMENT_PACKAGES = list(env_pkgs)
PACKAGES =  browsers + dev_tools + email_clients + encryption_tools + file_managers + gaming_packages + multimedia_tools + note_taking_apps + terminals

installer.filter_app_packages(PACKAGES)

installer.install_environment(list(env_pkgs))
installer.install_app_packages()

print(f"Installation complete!\n"
      "Check install logs at {installer.INSTALL_LOG_FILE_LOCATION}\n"
      "Please restart your computer.")