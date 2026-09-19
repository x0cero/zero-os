// The Zero desktop: a slim bar along the top (mark, the focused app's
// menus, tray, clock) and a floating dock along the bottom.
var plasma = getApiVersion(1);

var layout = {
    "desktops": [
        {
            "applets": [],
            "config": {
                "/": {"formfactor": "0", "immutability": "1", "wallpaperplugin": "org.kde.image"},
                "/Wallpaper/org.kde.image/General": {
                    "Image": "/usr/share/wallpapers/Zero/",
                    "FillMode": "2"
                }
            },
            "wallpaperPlugin": "org.kde.image"
        }
    ],
    "panels": [
        {
            "alignment": "left",
            "applets": [
                {
                    "config": {
                        "/": {"immutability": "1"},
                        "/General": {"icon": "zero-os", "showIconOnly": "true"}
                    },
                    "plugin": "org.kde.plasma.kickoff"
                },
                {
                    "config": {"/": {"immutability": "1"}, "/General": {"compactView": "false"}},
                    "plugin": "org.kde.plasma.appmenu"
                },
                {"plugin": "org.kde.plasma.panelspacer"},
                {
                    "config": {"/": {"immutability": "1"}},
                    "plugin": "org.kde.plasma.systemtray"
                },
                {
                    "config": {
                        "/": {"immutability": "1"},
                        "/Appearance": {
                            "showDate": "true",
                            "dateFormat": "custom",
                            "customDateFormat": "ddd d MMM",
                            "dateDisplayFormat": "BesideTime",
                            "use24hFormat": "0",
                            "boldText": "false"
                        }
                    },
                    "plugin": "org.kde.plasma.digitalclock"
                }
            ],
            "config": {"/": {"formfactor": "2", "immutability": "1"}},
            "height": 1.8,
            "hiding": "normal",
            "location": "top",
            "maximumLength": 0,
            "minimumLength": 0,
            "offset": 0
        },
        {
            "alignment": "center",
            "applets": [
                {
                    "config": {
                        "/": {"immutability": "1"},
                        "/General": {
                            "showOnlyCurrentScreen": "false",
                            "groupingStrategy": "0",
                            "iconSpacing": "1",
                            "launchers": "applications:org.kde.dolphin.desktop,applications:chromium-browser.desktop,applications:org.kde.konsole.desktop,applications:systemsettings.desktop"
                        }
                    },
                    "plugin": "org.kde.plasma.icontasks"
                }
            ],
            "config": {"/": {"formfactor": "2", "immutability": "1"}},
            "height": 4,
            "hiding": "normal",
            "location": "bottom",
            "maximumLength": 0,
            "minimumLength": 0,
            "offset": 0
        }
    ],
    "serializationFormatVersion": "1"
};

plasma.loadSerializedLayout(layout);

for (var i in panelIds) {
    var panel = panelById(panelIds[i]);
    if (!panel) continue;
    if (panel.location == "top") {
        panel.floating = false;
        panel.height = 28;
        panel.lengthMode = "fill";
    } else {
        panel.floating = true;
        panel.height = 64;
        panel.lengthMode = "fit";
        panel.alignment = "center";
    }
}
