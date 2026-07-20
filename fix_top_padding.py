import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Since it goes behind the status bar, we need to add standard top padding instead of statusBarsPadding so it doesn't overlap completely with the time and battery icons, OR if the user literally wants it glued to the top of the device screen ("একদম মোবাইলের উপরে লাগানো থাকবে", glued to the top of the mobile). If it's glued to the top, it will go under the status bar text.
# Let's add a small fixed padding so it doesn't look broken, but stays glued.
old_row = "modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 10.dp),"
new_row = "modifier = Modifier.fillMaxWidth().padding(start = 16.dp, end = 16.dp, top = 24.dp, bottom = 10.dp),"

content = content.replace(old_row, new_row)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
