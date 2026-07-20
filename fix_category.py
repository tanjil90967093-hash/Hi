import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace(
    'object Category : Screen("category", "Category", Icons.Outlined.Search, Icons.Filled.Search) // Using Search for category exploration',
    'object Category : Screen("category", "Category", Icons.Outlined.GridView, Icons.Filled.GridView)'
)
content = content.replace(
    'object Category : Screen("category", "Category", Icons.Outlined.Search, Icons.Filled.Search)',
    'object Category : Screen("category", "Category", Icons.Outlined.GridView, Icons.Filled.GridView)'
)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
