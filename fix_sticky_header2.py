import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Make the sticky header bottom square, and background white, with prominent green logo.
# The user wants "লোগো এই ফটোতে যেটা দিছি সেম টু সেম এই লোগো হবে"
# Image is a green background with a white bag. 
# So the sticky header could be white, with a green logo box containing a white bag.

old_header = r"""       Surface\(
         modifier = Modifier.fillMaxWidth\(\),
         color = Color\(0xFF4CAF50\), // Green background as requested
         shadowElevation = 8.dp,
         shape = RoundedCornerShape\(bottomStart = 24.dp, bottomEnd = 24.dp\) // Rounded bottom
       \) \{
           Column \{
               Spacer\(modifier = Modifier.statusBarsPadding\(\)\)
               Row\(
                   modifier = Modifier.fillMaxWidth\(\).padding\(horizontal = 16.dp, vertical = 10.dp\), // Thinner height
                   horizontalArrangement = Arrangement.SpaceBetween,
                   verticalAlignment = Alignment.CenterVertically
               \) \{
                   // Logo and Name
                   Row\(verticalAlignment = Alignment.CenterVertically\) \{
                       // Using an AsyncImage for the actual logo if possible, but fallback to a very close representation
                       Box\(
                           modifier = Modifier
                               .size\(32.dp\)
                               .clip\(RoundedCornerShape\(8.dp\)\)
                               .background\(Color.White\),
                           contentAlignment = Alignment.Center
                       \) \{
                           Icon\(
                               Icons.Filled.ShoppingBag,
                               contentDescription = "Logo",
                               tint = Color\(0xFF4CAF50\), // Green logo on white bg
                               modifier = Modifier.size\(20.dp\)
                           \)
                       \}
                       Spacer\(modifier = Modifier.width\(10.dp\)\)
                       
                       // Title
                       Text\(
                           "Circle Bazar", 
                           style = MaterialTheme.typography.titleLarge.copy\(
                               fontWeight = FontWeight.ExtraBold,
                               letterSpacing = 0.5.sp,
                               color = Color.White // White text on green header
                           \)
                       \)
                   \}
                   // Icons
                   Row\(horizontalArrangement = Arrangement.spacedBy\(16.dp\)\) \{
                       Icon\(Icons.Outlined.Search, contentDescription = "Search", tint = Color.White, modifier = Modifier.size\(24.dp\).clickable \{ onSearchClick\(\) \}\)
                       Icon\(Icons.Outlined.Notifications, contentDescription = "Notifications", tint = Color.White, modifier = Modifier.size\(24.dp\)\)
                   \}
               \}
           \}
       \}"""

new_header = """       Surface(
         modifier = Modifier.fillMaxWidth(),
         color = Color.White,
         shadowElevation = 8.dp,
         shape = androidx.compose.ui.graphics.RectangleShape
       ) {
           Column {
               Spacer(modifier = Modifier.statusBarsPadding())
               Row(
                   modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 10.dp),
                   horizontalArrangement = Arrangement.SpaceBetween,
                   verticalAlignment = Alignment.CenterVertically
               ) {
                   // Logo and Name
                   Row(verticalAlignment = Alignment.CenterVertically) {
                       // Logo exactly like the image (Green square, white bag)
                       Box(
                           modifier = Modifier
                               .size(36.dp)
                               .clip(RoundedCornerShape(8.dp))
                               .background(Color(0xFF2E7D32)), // Darker green
                           contentAlignment = Alignment.Center
                       ) {
                           Icon(
                               Icons.Filled.ShoppingBag,
                               contentDescription = "Logo",
                               tint = Color.White,
                               modifier = Modifier.size(24.dp)
                           )
                       }
                       Spacer(modifier = Modifier.width(12.dp))
                       
                       // Beautiful Title
                       val brush = androidx.compose.ui.graphics.Brush.linearGradient(
                           colors = listOf(Color(0xFF2E7D32), Color(0xFF4CAF50))
                       )
                       Text(
                           "Circle Bazar", 
                           style = MaterialTheme.typography.titleLarge.copy(
                               fontWeight = FontWeight.ExtraBold,
                               letterSpacing = 0.5.sp,
                               brush = brush
                           )
                       )
                   }
                   // Icons
                   Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                       Icon(Icons.Outlined.Search, contentDescription = "Search", tint = Color.DarkGray, modifier = Modifier.size(26.dp).clickable { onSearchClick() })
                       Icon(Icons.Outlined.Notifications, contentDescription = "Notifications", tint = Color.DarkGray, modifier = Modifier.size(26.dp))
                   }
               }
           }
       }"""

content = re.sub(old_header, new_header, content)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
