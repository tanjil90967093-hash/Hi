import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Make card wider to match design better
content = content.replace("CircleDealCard(shuffled[index], modifier = Modifier.width(160.dp))", "CircleDealCard(shuffled[index], modifier = Modifier.width(180.dp))")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
