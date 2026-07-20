with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    lines = f.readlines()

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

for i, line in enumerate(lines):
    if line.strip() == "item { Spacer(modifier = Modifier.height(32.dp)) }":
        # Check if the next lines are closing the LazyColumn and Box
        if lines[i+1].strip() == "}" and lines[i+2].strip() == "}":
            lines.insert(i+2, sticky_header_ui)
            print("Inserted sticky header")
            break

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.writelines(lines)
