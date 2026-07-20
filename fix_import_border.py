import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

if "import androidx.compose.foundation.BorderStroke" not in content:
    content = content.replace("import androidx.compose.foundation.layout.*", "import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.BorderStroke")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
