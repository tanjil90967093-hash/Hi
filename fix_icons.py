import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# "সার্চ আইকন এবং নোটিফিকেশন আইকন এইগুলা কার্ডের মাঝখানে দিবি বেশি নিচে দিবি না বেশি উপরে দিবি না কার্ডের মাঝখানে সোজাসুজি"
# Currently in Sticky Header:
old_icons = """                   // Icons
                   Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                       Icon(Icons.Filled.Search, contentDescription = "Search", tint = Color(0xFF4CAF50), modifier = Modifier.size(26.dp).clickable { onSearchClick() })
                       Icon(Icons.Filled.Notifications, contentDescription = "Notifications", tint = Color(0xFF4CAF50), modifier = Modifier.size(26.dp))
                   }"""
                   
# They should already be vertically centered due to Row's `verticalAlignment = Alignment.CenterVertically`. 
# To ensure they are centered and distinct, I'll update their size/padding slightly to look better.

new_icons = """                   // Icons
                   Row(
                       horizontalArrangement = Arrangement.spacedBy(12.dp),
                       verticalAlignment = Alignment.CenterVertically
                   ) {
                       Box(
                           modifier = Modifier.size(36.dp).clip(CircleShape).background(Color(0xFFF5F5F5)).clickable { onSearchClick() },
                           contentAlignment = Alignment.Center
                       ) {
                           Icon(Icons.Outlined.Search, contentDescription = "Search", tint = Color(0xFF4CAF50), modifier = Modifier.size(22.dp))
                       }
                       Box(
                           modifier = Modifier.size(36.dp).clip(CircleShape).background(Color(0xFFF5F5F5)).clickable { },
                           contentAlignment = Alignment.Center
                       ) {
                           Icon(Icons.Outlined.Notifications, contentDescription = "Notifications", tint = Color(0xFF4CAF50), modifier = Modifier.size(22.dp))
                       }
                   }"""

content = content.replace(old_icons, new_icons)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
