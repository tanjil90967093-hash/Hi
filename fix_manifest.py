import re

with open("app/src/main/AndroidManifest.xml", "r") as f:
    content = f.read()

intent_filter_old = """            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>"""

intent_filter_new = """            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
            <intent-filter android:autoVerify="true">
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data android:scheme="https" android:host="circlebazar.com" android:pathPrefix="/deals" />
            </intent-filter>"""

content = content.replace(intent_filter_old, intent_filter_new)

with open("app/src/main/AndroidManifest.xml", "w") as f:
    f.write(content)
