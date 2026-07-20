import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# I accidentally replaced the LazyHorizontalGrid height when replacing 480.dp -> 280.dp!
content = content.replace("modifier = Modifier.fillMaxWidth().height(280.dp) // Approximate height for 2 rows of 260dp cards + spacing", "modifier = Modifier.fillMaxWidth().height(480.dp) // Approximate height for 2 rows of 260dp cards + spacing")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
