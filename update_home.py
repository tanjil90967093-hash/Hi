import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Replace Search Bar and Banner item
start = content.find("      item {\n        // 2. Search Bar")
end = content.find("      item {\n        // Circle Deals")

new_top_section = """      item {
        Box(modifier = Modifier.fillMaxWidth()) {
          // Green background for the top to blend with header
          Box(modifier = Modifier.fillMaxWidth().height(80.dp).background(androidx.compose.ui.graphics.Brush.horizontalGradient(listOf(Color(0xFF2E7D32), Color(0xFF388E3C)))))
          
          Column {
             // Banner (behind the search bar slightly)
             Box(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp)) {
                AsyncImage(
                  model = "https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?w=800&q=80",
                  contentDescription = "Banner",
                  contentScale = ContentScale.Crop,
                  modifier = Modifier.fillMaxWidth().height(160.dp).clip(RoundedCornerShape(16.dp))
                )
                
                // Search bar on top of the banner
                Box(modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp).padding(top = 12.dp)) {
                  Box(modifier = Modifier.clickable { onSearchClick() }) {
                    TextField(
                      value = "",
                      onValueChange = {},
                      modifier = Modifier.fillMaxWidth().height(44.dp),
                      placeholder = { Text("Search products, brands and stores", color = Color.Gray, fontSize = 12.sp) },
                      leadingIcon = { Icon(Icons.Outlined.Search, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(20.dp)) },
                      trailingIcon = {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                          Icon(Icons.Outlined.Mic, contentDescription = "Voice Search", tint = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(horizontal = 4.dp).size(20.dp))
                          Icon(Icons.Outlined.CameraAlt, contentDescription = "Image Search", tint = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(end = 12.dp, start = 4.dp).size(20.dp).clickable { onCameraClick() })
                        }
                      },
                      shape = RoundedCornerShape(22.dp),
                      colors = TextFieldDefaults.colors(
                        unfocusedContainerColor = Color.White.copy(alpha = 0.95f),
                        focusedContainerColor = Color.White,
                        unfocusedIndicatorColor = Color.Transparent,
                        focusedIndicatorColor = Color.Transparent
                      ),
                      singleLine = true,
                      readOnly = true,
                      enabled = false
                    )
                    // Overlay to handle clicks
                    Box(modifier = Modifier.matchParentSize().clickable { onSearchClick() })
                  }
                }
             }
          }
        }
      }

"""

content = content[:start] + new_top_section + content[end:]
with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

