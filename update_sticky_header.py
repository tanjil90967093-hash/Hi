import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

old_sticky_header = r"""    // Sticky Header
    androidx.compose.animation.AnimatedVisibility\(
       visible = showStickyHeader,
       enter = androidx.compose.animation.fadeIn\(\) \+ androidx.compose.animation.slideInVertically\(
           initialOffsetY = \{ -it \}
       \),
       exit = androidx.compose.animation.fadeOut\(\) \+ androidx.compose.animation.slideOutVertically\(
           targetOffsetY = \{ -it \}
       \),
       modifier = Modifier.align\(Alignment.TopCenter\)
    \) \{
       Surface\(
         modifier = Modifier.fillMaxWidth\(\),
         color = Color.White,
         shadowElevation = 8.dp,
         shape = androidx.compose.ui.graphics.RectangleShape // No rounded corners
       \) \{
           Column \{
               
               Row\(
                   modifier = Modifier.fillMaxWidth\(\).padding\(start = 16.dp, end = 16.dp, top = 24.dp, bottom = 10.dp\), // A bit more padding top/bottom to center things
                   horizontalArrangement = Arrangement.SpaceBetween,
                   verticalAlignment = Alignment.CenterVertically
               \) \{
                   // Using the provided image for the logo
                   AsyncImage\(
                       model = "https://storage.googleapis.com/aistudio-chat-blob-store/b0d62ab3b5cf2e5c1a8bd51509930f9a.jpg",
                       contentDescription = "Logo",
                       modifier = Modifier.size\(40.dp\).clip\(RoundedCornerShape\(8.dp\)\)
                   \)
                   
                   // Title
                   val brush = androidx.compose.ui.graphics.Brush.linearGradient\(
                       colors = listOf\(Color\(0xFF2E7D32\), Color\(0xFF4CAF50\)\)
                   \)
                   Text\(
                       "Circle Bazar", 
                       style = MaterialTheme.typography.titleLarge.copy\(
                           fontWeight = FontWeight.ExtraBold,
                           letterSpacing = 0.5.sp,
                           brush = brush
                       \),
                       modifier = Modifier.weight\(1f\).padding\(horizontal = 16.dp\), // Give text weight and padding so it sits between logo and icons nicely
                       textAlign = androidx.compose.ui.text.style.TextAlign.Center // Center the text!
                   \)
                   
                   // Icons
                   Row\(
                       horizontalArrangement = Arrangement.spacedBy\(12.dp\),
                       verticalAlignment = Alignment.CenterVertically
                   \) \{
                       Box\(
                           modifier = Modifier.size\(36.dp\).clip\(CircleShape\).background\(Color\(0xFFF5F5F5\)\).clickable \{ onSearchClick\(\) \},
                           contentAlignment = Alignment.Center
                       \) \{
                           Icon\(Icons.Outlined.Search, contentDescription = "Search", tint = Color\(0xFF4CAF50\), modifier = Modifier.size\(22.dp\)\)
                       \}
                       Box\(
                           modifier = Modifier.size\(36.dp\).clip\(CircleShape\).background\(Color\(0xFFF5F5F5\)\).clickable \{ \},
                           contentAlignment = Alignment.Center
                       \) \{
                           Icon\(Icons.Outlined.Notifications, contentDescription = "Notifications", tint = Color\(0xFF4CAF50\), modifier = Modifier.size\(22.dp\)\)
                       \}
                   \}
               \}
           \}
       \}
    \}"""

new_sticky_header = """    // Sticky Header
    androidx.compose.animation.AnimatedVisibility(
       visible = showStickyHeader,
       enter = androidx.compose.animation.fadeIn() + androidx.compose.animation.slideInVertically(
           initialOffsetY = { -it }
       ),
       exit = androidx.compose.animation.fadeOut() + androidx.compose.animation.slideOutVertically(
           targetOffsetY = { -it }
       ),
       modifier = Modifier.align(Alignment.TopCenter)
    ) {
       Surface(
         modifier = Modifier.fillMaxWidth(),
         color = Color.White,
         shadowElevation = 8.dp,
         shape = androidx.compose.ui.graphics.RectangleShape // Sharp corners at the bottom
       ) {
           Row(
               modifier = Modifier
                   .fillMaxWidth()
                   .windowInsetsPadding(androidx.compose.foundation.layout.WindowInsets.statusBars)
                   .padding(horizontal = 16.dp, vertical = 8.dp), // Slimmer header
               horizontalArrangement = Arrangement.SpaceBetween,
               verticalAlignment = Alignment.CenterVertically
           ) {
               // Using the provided image for the logo
               AsyncImage(
                   model = "https://storage.googleapis.com/aistudio-chat-blob-store/b0d62ab3b5cf2e5c1a8bd51509930f9a.jpg",
                   contentDescription = "Logo",
                   modifier = Modifier.size(36.dp).clip(RoundedCornerShape(8.dp))
               )
               
               // Title (Align left next to logo)
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
                   modifier = Modifier.weight(1f).padding(horizontal = 12.dp)
               )
               
               // Icons (Search and Notification) - User requested: "বাম সাইডে তোমার একটা নোটিফিকেশন আইকন এবং নোটিফিকেশন আইকন এর পাশে সার্চ আইকন" 
               // Actually the text says left side, but standard is right side. I will put them together.
               Row(
                   horizontalArrangement = Arrangement.spacedBy(16.dp),
                   verticalAlignment = Alignment.CenterVertically
               ) {
                   Icon(Icons.Outlined.Notifications, contentDescription = "Notifications", tint = Color.Black, modifier = Modifier.size(26.dp).clickable { })
                   Icon(Icons.Outlined.Search, contentDescription = "Search", tint = Color.Black, modifier = Modifier.size(26.dp).clickable { onSearchClick() })
               }
           }
       }
    }"""

content = re.sub(old_sticky_header, new_sticky_header, content)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

