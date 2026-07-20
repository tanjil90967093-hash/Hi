import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

old_header_shape = """       Surface(
         modifier = Modifier.fillMaxWidth(),
         color = Color.White,
         shadowElevation = 8.dp,
         shape = RoundedCornerShape(bottomStart = 16.dp, bottomEnd = 16.dp)
       ) {"""

new_header_shape = """       Surface(
         modifier = Modifier.fillMaxWidth(),
         color = Color.White,
         shadowElevation = 8.dp,
         shape = androidx.compose.ui.graphics.RectangleShape // No rounded corners
       ) {"""

content = content.replace(old_header_shape, new_header_shape)

old_header_row = """                   modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 6.dp),
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
                       Icon(Icons.Filled.Search, contentDescription = "Search", tint = Color(0xFF4CAF50), modifier = Modifier.size(26.dp).clickable { onSearchClick() })
                       Icon(Icons.Filled.Notifications, contentDescription = "Notifications", tint = Color(0xFF4CAF50), modifier = Modifier.size(26.dp))
                   }
               }"""

new_header_row = """                   modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 10.dp), // A bit more padding top/bottom to center things
                   horizontalArrangement = Arrangement.SpaceBetween,
                   verticalAlignment = Alignment.CenterVertically
               ) {
                   // Using the provided image for the logo
                   AsyncImage(
                       model = "https://storage.googleapis.com/aistudio-chat-blob-store/b0d62ab3b5cf2e5c1a8bd51509930f9a.jpg",
                       contentDescription = "Logo",
                       modifier = Modifier.size(40.dp).clip(RoundedCornerShape(8.dp))
                   )
                   
                   // Title
                   val brush = androidx.compose.ui.graphics.Brush.linearGradient(
                       colors = listOf(Color(0xFF2E7D32), Color(0xFF4CAF50))
                   )
                   Text(
                       "Circle Bazar", 
                       style = MaterialTheme.typography.titleLarge.copy(
                           fontWeight = FontWeight.ExtraBold,
                           letterSpacing = 0.5.sp,
                           brush = brush
                       ),
                       modifier = Modifier.weight(1f).padding(horizontal = 16.dp), // Give text weight and padding so it sits between logo and icons nicely
                       textAlign = androidx.compose.ui.text.style.TextAlign.Center // Center the text!
                   )
                   
                   // Icons
                   Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                       Icon(Icons.Filled.Search, contentDescription = "Search", tint = Color(0xFF4CAF50), modifier = Modifier.size(26.dp).clickable { onSearchClick() })
                       Icon(Icons.Filled.Notifications, contentDescription = "Notifications", tint = Color(0xFF4CAF50), modifier = Modifier.size(26.dp))
                   }
               }"""

content = content.replace(old_header_row, new_header_row)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

