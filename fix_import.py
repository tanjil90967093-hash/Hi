import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

if "import androidx.compose.ui.input.nestedscroll.nestedScroll" not in content:
    content = content.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\nimport androidx.compose.ui.input.nestedscroll.nestedScroll")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

