# -*- coding: utf-8 -*-
# Created by apple on 2017/2/7.


class IPAPlist:
    __plist_template = '''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>items</key>
    <array>
        <dict>
            <key>assets</key>
            <array>
                <dict>
                    <key>kind</key>
                    <string>software-package</string>
                    <key>url</key>
                    <string>{}</string>
                </dict>
            </array>
            <key>metadata</key>
            <dict>
                <key>bundle-identifier</key>
                <string>{}</string>
                <key>bundle-version</key>
                <string>{}</string>
                <key>kind</key>
                <string>software</string>
                <key>title</key>
                <string>{}</string>
            </dict>
        </dict>
    </array>
</dict>
</plist>
    '''

    @classmethod
    def parse(cls, url: str, bundle: str, version: str, title: str) -> str:
        return cls.__plist_template.format(url, bundle, version, title)
