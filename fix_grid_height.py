import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace("modifier = Modifier.fillMaxWidth().height(460.dp)", "modifier = Modifier.fillMaxWidth().height(410.dp)")
content = content.replace("CircleDealCard(circleDealsList[index], modifier = Modifier.width(140.dp))", "CircleDealCard(circleDealsList[index], modifier = Modifier.width(130.dp))")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
