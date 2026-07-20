import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Replace the sticky header
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
         shape = androidx.compose.ui.graphics.RectangleShape
       \) \{
           Column \{
               Spacer\(modifier = Modifier.statusBarsPadding\(\)\)
               Row\(
                   modifier = Modifier.fillMaxWidth\(\).padding\(horizontal = 16.dp, vertical = 14.dp\),
                   horizontalArrangement = Arrangement.SpaceBetween,
                   verticalAlignment = Alignment.CenterVertically
               \) \{
                   // Logo and Name
                   Row\(verticalAlignment = Alignment.CenterVertically\) \{
                       // Custom Logo Box
                       Box\(
                           modifier = Modifier
                               .size\(36.dp\)
                               .clip\(RoundedCornerShape\(10.dp\)\)
                               .background\(Color\(0xFF4CAF50\)\),
                           contentAlignment = Alignment.Center
                       \) \{
                           Icon\(
                               Icons.Filled.ShoppingBag,
                               contentDescription = "Logo",
                               tint = Color.White,
                               modifier = Modifier.size\(22.dp\)
                           \)
                           // Little circle detail to match "Circle" theme
                           Box\(
                               modifier = Modifier
                                   .size\(12.dp\)
                                   .align\(Alignment.BottomEnd\)
                                   .offset\(x = \(-4\).dp, y = \(-4\).dp\)
                                   .border\(2.dp, Color\(0xFF4CAF50\), CircleShape\)
                                   .clip\(CircleShape\)
                                   .background\(Color.White\)
                           \)
                       \}
                       Spacer\(modifier = Modifier.width\(12.dp\)\)
                       
                       // Beautiful Title
                       val brush = androidx.compose.ui.graphics.Brush.linearGradient\(
                           colors = listOf\(Color\(0xFF2E7D32\), Color\(0xFF4CAF50\)\)
                       \)
                       Text\(
                           "Circle Bazar", 
                           style = MaterialTheme.typography.titleLarge.copy\(
                               fontWeight = FontWeight.ExtraBold,
                               letterSpacing = 0.5.sp,
                               brush = brush
                           \)
                       \)
                   \}
                   // Icons
                   Row\(horizontalArrangement = Arrangement.spacedBy\(16.dp\)\) \{
                       Box\(
                           modifier = Modifier
                               .size\(40.dp\)
                               .clip\(CircleShape\)
                               .background\(Color\(0xFFF5F5F5\)\)
                               .clickable \{ onSearchClick\(\) \},
                           contentAlignment = Alignment.Center
                       \) \{
                           Icon\(Icons.Outlined.Search, contentDescription = "Search", tint = Color.Black, modifier = Modifier.size\(24.dp\)\)
                       \}
                       Box\(
                           modifier = Modifier
                               .size\(40.dp\)
                               .clip\(CircleShape\)
                               .background\(Color\(0xFFF5F5F5\)\)
                               .clickable \{ \},
                           contentAlignment = Alignment.Center
                       \) \{
                           Icon\(Icons.Outlined.Notifications, contentDescription = "Notifications", tint = Color.Black, modifier = Modifier.size\(24.dp\)\)
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
         color = Color(0xFF4CAF50), // Green background as requested
         shadowElevation = 8.dp,
         shape = RoundedCornerShape(bottomStart = 24.dp, bottomEnd = 24.dp) // Rounded bottom
       ) {
           Column {
               Spacer(modifier = Modifier.statusBarsPadding())
               Row(
                   modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 10.dp), // Thinner height
                   horizontalArrangement = Arrangement.SpaceBetween,
                   verticalAlignment = Alignment.CenterVertically
               ) {
                   // Logo and Name
                   Row(verticalAlignment = Alignment.CenterVertically) {
                       // Using an AsyncImage for the actual logo if possible, but fallback to a very close representation
                       Box(
                           modifier = Modifier
                               .size(32.dp)
                               .clip(RoundedCornerShape(8.dp))
                               .background(Color.White),
                           contentAlignment = Alignment.Center
                       ) {
                           Icon(
                               Icons.Filled.ShoppingBag,
                               contentDescription = "Logo",
                               tint = Color(0xFF4CAF50), // Green logo on white bg
                               modifier = Modifier.size(20.dp)
                           )
                       }
                       Spacer(modifier = Modifier.width(10.dp))
                       
                       // Title
                       Text(
                           "Circle Bazar", 
                           style = MaterialTheme.typography.titleLarge.copy(
                               fontWeight = FontWeight.ExtraBold,
                               letterSpacing = 0.5.sp,
                               color = Color.White // White text on green header
                           )
                       )
                   }
                   // Icons
                   Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                       Icon(Icons.Outlined.Search, contentDescription = "Search", tint = Color.White, modifier = Modifier.size(24.dp).clickable { onSearchClick() })
                       Icon(Icons.Outlined.Notifications, contentDescription = "Notifications", tint = Color.White, modifier = Modifier.size(24.dp))
                   }
               }
           }
       }
    }"""

content = re.sub(old_sticky_header, new_sticky_header, content)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

