import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Update icons in sticky header as well
old_sticky_icons = """                   // Icons
                   Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                       Icon(Icons.Outlined.Search, contentDescription = "Search", tint = Color.DarkGray, modifier = Modifier.size(26.dp).clickable { onSearchClick() })
                       Icon(Icons.Outlined.Notifications, contentDescription = "Notifications", tint = Color.DarkGray, modifier = Modifier.size(26.dp))
                   }"""

new_sticky_icons = """                   // Icons
                   Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                       Icon(Icons.Filled.Search, contentDescription = "Search", tint = Color(0xFF4CAF50), modifier = Modifier.size(26.dp).clickable { onSearchClick() })
                       Icon(Icons.Filled.Notifications, contentDescription = "Notifications", tint = Color(0xFF4CAF50), modifier = Modifier.size(26.dp))
                   }"""

content = content.replace(old_sticky_icons, new_sticky_icons)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
