import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Find the end of HomeScreen
end_home = content.find("fun CategoryScreen() {")

if end_home != -1:
    # Look back to find the closing brace of HomeScreen
    closing_brace = content.rfind("}", 0, end_home)
    # The structure should be:
    #     } // end LazyColumn
    #   } // end Box
    # } // end HomeScreen

    # Let's find the closing of Box and insert our sticky header.
    # Actually, it's safer to just replace the last part of HomeScreen.
    last_item_end = content.find("      item {\n        // Footer", 0, closing_brace)
    if last_item_end != -1:
        # Find the end of the item block
        item_end = content.find("      }", last_item_end)
        lazy_col_end = content.find("    }", item_end)
        
        insert_idx = lazy_col_end + 5
        
        sticky_header_ui = """
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
"""
        content = content[:insert_idx] + sticky_header_ui + content[insert_idx:]
        with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
            f.write(content)
        print("Injected sticky header at the end of HomeScreen box")

