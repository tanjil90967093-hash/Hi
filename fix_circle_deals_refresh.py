import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# I will add a RefreshTrigger state to shuffle products when user pulls to refresh or something
# Actually, the user says: "মানে আমার অ্যাপ্লিকেশন টা রিজেক্ট করলে ওই প্রোডাক্টগুলো চেঞ্জ হবে"
# "Reject" probably means "Refresh" or restarting the app.
# If they mean restarting the app, mockProducts.shuffled() each time the screen is composed or the app starts is enough.
# Let's add a key to the remember so we can manually trigger it if needed, or just let it randomize on mount.

# It's already randomized on mount because of `remember { mockProducts.shuffled().take(20) }`

# Make sure the grid height is enough
content = content.replace("modifier = Modifier.fillMaxWidth().height(560.dp)", "modifier = Modifier.fillMaxWidth().height(580.dp)")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
