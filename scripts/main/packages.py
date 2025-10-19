CATEGORIES = [
    "0. Exit",
    "1. Applications",
    "2. Containers",
    "3. DNS Servers",
    "4. System Utilities",
    "5. VPN Clients",
]

COMMON = {
    "FONTS": [
        {
            "Distro": "debian",
            "Packages": [
                "fonts-font-awesome",
                "fonts-recommended",
                "fonts-roboto",
                "fonts-terminus",
            ],
        }
    ],
    "UTILITY_PACKAGES": [
        {
            "Distro": "debian",
            "Packages": [
                "curl",
                "fastfetch",
                "flatpak",
                "git",
                "gnupg2",
                "gpg",
                "libavcodec-extra",
                "libspa-0.2-bluetooth",
                "pipewire",
                "pipewire-alsa",
                "pipewire-pulse",
                "vim",
                "zram-tools",
            ],
        }
    ],
}

APP_CATEGORIES = [
    "0. Exit",
    "1. Browsers",
    "2. Dev Tools",
    "3. E-mail Clients",
    "4. Encryption Tools",
    "5. File Managers",
    "6. Gaming Packages",
    "7. Multimedia Tools",
    "8. Note Taking Tools",
    "9. Terminals",
]

DNS_SERVERS = ["0. Exit", "1. Cloudflare", "2. Quad9", "3. Google"]

VPN_CLIENTS = ["0. Exit", "1. Mullvad", "2. Proton"]

ENVIRONMENTS = [
    {
        "Name": "0. Skip",
        "Debian_Packages": [""],
    },
    {
        "Name": "1. KDE",
        "Debian_Packages": [
            "kde-plasma-desktop",
            "plasma-discover-backend-flatpak",
            "plasma-nm",
            "sddm-theme-breeze ",
        ],
    },
    #! If Wayland session is missing when using the proprietary nvidia drivers, use:
    #! ln -s /dev/null /etc/udev/rules.d/61-gdm.rules
    {
        "Name": "2. Gnome",
        "Debian_Packages": [
            "gnome-session",
            "gnome-software-plugin-flatpak",
            "gnome-terminal",
            "gnome-text-editor",
            "nautilus",
        ],
    },
    {
        "Name": "3. XFCE",
        "Debian_Packages": [
            "xfce4",
        ],
    }
]

SYSTEM_UTILITIES = ["0. Exit", "1. Nvidia Drivers"]

CONTAINER_BACKENDS = ["0. Exit", "1. Distrobox (Docker)", "2. Distrobox (Podman)"]

CONTAINERS = [
    {
        "Type": "Distrobox",
        "Name": "1. Development"
    }
]

BROWSERS = [
    {
        "Name": "Brave",
        "APT_Package": "",
        "Custom_Script": "",
        "Flatpak_Package": "com.brave.Browser",
    },
    {
        "Name": "Firefox",
        "APT_Package": "",
        "Custom_Script": "",
        "Flatpak_Package": "org.mozilla.firefox",
    },
    {
        "Name": "Libre Wolf",
        "APT_Package": "",
        "Custom_Script": "",
        "Flatpak_Package": "io.gitlab.librewolf-community",
    },
    {
        "Name": "Zen Browser",
        "APT_Package": "",
        "Custom_Script": "",
        "Flatpak_Package": "app.zen_browser.zen",
    },
]

DEV_TOOLS = [
    {
        "Name": "Bruno",
        "APT_Package": "",
        "Custom_Script": "",
        "Flatpak_Package": "com.usebruno.Bruno",
    },
    {
        "Name": "Filezilla",
        "APT_Package": "filezilla",
        "Custom_Script": "",
        "Flatpak_Package": "org.filezillaproject.Filezilla",
    },
]

EMAIL_CLIENTS = [
    {
        "Name": "Betterbird",
        "APT_Package": "",
        "Custom_Script": "",
        "Flatpak_Package": "eu.betterbird.Betterbird",
    },
    {
        "Name": "Thunderbird",
        "APT_Package": "",
        "Custom_Script": "",
        "Flatpak_Package": "org.mozilla.Thunderbird",
    },
]

ENCRYPTION_TOOLS = [
    {
        "Name": "Cryptomator",
        "APT_Package": "",
        "Custom_Script": "",
        "Flatpak_Package": "org.cryptomator.Cryptomator",
    },
    {
        "Name": "Veracrypt",
        "APT_Package": "",
        "Custom_Script": "$SCRIPT_DIR/scripts/custom/Apps/veracrypt.sh",
        "Flatpak_Package": "",
    },
]

FILE_MANAGERS = [
    {
        "Name": "Dolphin",
        "APT_Package": "dolphin",
        "Custom_Script": "",
        "Flatpak_Package": "",
    },
    {
        "Name": "Nautilus",
        "APT_Package": "nautilus",
        "Custom_Script": "",
        "Flatpak_Package": "",
    },
    {
        "Name": "PCManFM",
        "APT_Package": "pcmanfm",
        "Custom_Script": "",
        "Flatpak_Package": "",
    },
    {
        "Name": "Thunar",
        "APT_Package": "thunar",
        "Custom_Script": "",
        "Flatpak_Package": "",
    },
]

GAMING_PACKAGES = [
    {
        "Name": "Heroic Games Launcher",
        "APT_Package": "",
        "Custom_Script": "",
        "Flatpak_Package": "com.heroicgameslauncher.hgl",
    },
    {
        "Name": "Lutris",
        "APT_Package": "",
        "Custom_Script": "",
        "Flatpak_Package": "net.lutris.Lutris",
    },
    {
        "Name": "Prism Launcher",
        "APT_Package": "",
        "Custom_Script": "",
        "Flatpak_Package": "org.prismlauncher.PrismLauncher",
    },
    {
        "Name": "Steam",
        "APT_Package": "",
        "Custom_Script": "",
        "Flatpak_Package": "com.valvesoftware.Steam",
    },
]

MULTIMEDIA_TOOLS = [
    {
        "Name": "Freetube",
        "APT_Package": "",
        "Custom_Script": "",
        "Flatpak_Package": "io.freetubeapp.FreeTube",
    },
    {
        "Name": "Gimp",
        "APT_Package": "gimp",
        "Custom_Script": "",
        "Flatpak_Package": "org.gimp.GIMP",
    },
    {
        "Name": "Jellyfin Media Player",
        "APT_Package": "",
        "Custom_Script": "",
        "Flatpak_Package": "com.github.iwalton3.jellyfin-media-player",
    },
    {
        "Name": "Libre Office",
        "APT_Package": "libreoffice",
        "Custom_Script": "",
        "Flatpak_Package": "org.libreoffice.LibreOffice",
    },
    {
        "Name": "MkvToolNix",
        "APT_Package": "",
        "Custom_Script": "",
        "Flatpak_Package": "org.bunkus.mkvtoolnix-gui",
    },
    {
        "Name": "VLC",
        "APT_Package": "vlc",
        "Custom_Script": "",
        "Flatpak_Package": "org.videolan.VLC",
    },
]

NOTE_TAKING_APPS = [
    {
        "Name": "Obsidian",
        "APT_Package": "",
        "Custom_Script": "",
        "Flatpak_Package": "md.obsidian.Obsidian",
    },
    {
        "Name": "Trillium Notes",
        "APT_Package": "",
        "Custom_Script": "",
        "Flatpak_Package": "com.github.zadam.trilium",
    },
    {
        "Name": "Zettlr",
        "APT_Package": "",
        "Custom_Script": "",
        "Flatpak_Package": "com.zettlr.Zettlr",
    },
]

TERMINALS = [
    {
        "Name": "Allacrity",
        "APT_Package": "alacritty",
        "Custom_Script": "",
        "Flatpak_Package": "",
    },
    {
        "Name": "Kitty",
        "APT_Package": "kitty",
        "Custom_Script": "",
        "Flatpak_Package": "",
    },
]
