import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

start_box = content.find("  Box(modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)) {\n    LazyColumn")
end_box = content.find("    LazyColumn", start_box)

new_header = """  Box(modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)) {
    LazyColumn(state = listState, modifier = Modifier.fillMaxSize().padding(bottom = 0.dp)) {
"""

sticky_header_ui = """    } // end LazyColumn

    // Sticky Header
    androidx.compose.animation.AnimatedVisibility(
       visible = showStickyHeader,
       enter = androidx.compose.animation.fadeIn() + androidx.compose.animation.slideInVertically(),
       exit = androidx.compose.animation.fadeOut() + androidx.compose.animation.slideOutVertically(),
       modifier = Modifier.align(Alignment.TopCenter)
    ) {
       Box(
         modifier = Modifier
           .fillMaxWidth()
           .background(Color.White)
           .shadow(4.dp)
           .statusBarsPadding()
       ) {
         Row(
           modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 12.dp),
           horizontalArrangement = Arrangement.SpaceBetween,
           verticalAlignment = Alignment.CenterVertically
         ) {
           // Logo and Name
           Row(verticalAlignment = Alignment.CenterVertically) {
             Icon(Icons.Outlined.ShoppingCart, contentDescription = "Logo", tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(28.dp))
             Spacer(modifier = Modifier.width(8.dp))
             Text("Circle Bazar", color = MaterialTheme.colorScheme.primary, fontSize = 20.sp, fontWeight = FontWeight.Bold, letterSpacing = 1.sp)
           }
           // Icons
           Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
             Icon(Icons.Outlined.Search, contentDescription = "Search", tint = Color.Black, modifier = Modifier.clickable { onSearchClick() })
             Icon(Icons.Outlined.Notifications, contentDescription = "Notifications", tint = Color.Black)
           }
         }
       }
    }
  } // end Box
"""

if start_box != -1:
    content = content[:start_box] + new_header + content[start_box + len("  Box(modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)) {\n    LazyColumn(state = listState, modifier = Modifier.fillMaxSize()) {\n"):]
    # Wait, the end of LazyColumn needs to be found so we can insert the sticky_header_ui.
    
    # Let's just do it securely.
    pass

