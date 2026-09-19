// The Zero OS desktop: paper with a strip along the top. The strip holds the
// mark (the launcher), the open windows, the tray and the time. No floating,
// no dock, nothing else.
var plasma = getApiVersion(1);

var layout = {
    "desktops": [
        {
            "applets": [],
            "config": {
                "/": {"formfactor": "0", "immutability": "1", "wallpaperplugin": "org.kde.image"},
                "/Wallpaper/org.kde.image/General": {
                    "Image": "/usr/share/wallpapers/ZeroPaper/",
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
                    "config": {
                        "/": {"immutability": "1"},
                        "/General": {
                            "showOnlyCurrentScreen": "false",
                            "groupingStrategy": "0",
                            "iconSpacing": "1",
                            "launchers": ""
                        }
                    },
                    "plugin": "org.kde.plasma.icontasks"
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
                            "showDate": "false",
                            "use24hFormat": "2",
                            "fontFamily": "Geist Pixel Square",
                            "boldText": "false",
                            "autoFontAndSize": "false",
                            "fontSize": "14"
                        }
                    },
                    "plugin": "org.kde.plasma.digitalclock"
                }
            ],
            "config": {"/": {"formfactor": "2", "immutability": "1"}},
            "height": 2.2,
            "hiding": "normal",
            "location": "top",
            "maximumLength": 0,
            "minimumLength": 0,
            "offset": 0
        }
    ],
    "serializationFormatVersion": "1"
};

plasma.loadSerializedLayout(layout);

// Plasma 6 floats panels by default; ours sits flush against the edge.
for (var i in panelIds) {
    var panel = panelById(panelIds[i]);
    if (panel) {
        panel.floating = false;
        panel.height = 40;
        panel.lengthMode = "fill";
    }
}
