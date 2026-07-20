import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# I notice that my regex missed Spacer(modifier = Modifier.statusBarsPadding()).
# And it also missed the fact that "লোগো নাম চার্জ আইকন এবং নোটিফিকেশন আইকন এইগুলা কার্ডের মাঝখানে দিবি বেশি নিচে দিবি না বেশি উপরে দিবি না কার্ডের মাঝখানে সোজাসুজি তাইলে সুন্দর দেখা যাবে".
# They are in a Row with verticalAlignment = Alignment.CenterVertically, so they are vertically centered!
# The user might be complaining about Spacer(modifier = Modifier.statusBarsPadding()) adding too much space at the top.
# "উপরের দিকে একটু ফাঁকা আছে এই ফাকা থাকবে না রে ভাই" (There is a gap at the top, this gap shouldn't be there).
# OK, I'll remove statusBarsPadding from the Sticky Header so it goes all the way to the top of the screen (behind the status bar if edge-to-edge).
# Let's check how the header is rendered.
# Modifier.statusBarsPadding() inside the sticky header Column pushes it down.
# Let's remove it.

content = content.replace("Spacer(modifier = Modifier.statusBarsPadding())", "")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

