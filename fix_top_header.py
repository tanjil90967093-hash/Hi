import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Make the sticky header top padding less "fat" so it looks better
content = content.replace("modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 10.dp)", "modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 6.dp)")

# Update sticky header rounded corners, the user wanted bottom rounded, which I did:
# shape = RoundedCornerShape(bottomStart = 24.dp, bottomEnd = 24.dp)
# Actually the code currently says: shape = androidx.compose.ui.graphics.RectangleShape
# Oh wait, my second sticky header script replaced the first one and put back RectangleShape! Let's fix that.

old_header_shape = """       Surface(
         modifier = Modifier.fillMaxWidth(),
         color = Color.White,
         shadowElevation = 8.dp,
         shape = androidx.compose.ui.graphics.RectangleShape
       ) {"""

new_header_shape = """       Surface(
         modifier = Modifier.fillMaxWidth(),
         color = Color.White,
         shadowElevation = 8.dp,
         shape = RoundedCornerShape(bottomStart = 16.dp, bottomEnd = 16.dp)
       ) {"""

content = content.replace(old_header_shape, new_header_shape)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
