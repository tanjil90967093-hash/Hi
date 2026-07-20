import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

start = content.find("      item {\n        Box(modifier = Modifier.fillMaxWidth()) {\n          // Green background for the top to blend with header")
end = content.find("      item {\n        // Circle Deals")

new_top = """      item {
        // 2. Search Bar
        Box(
          modifier = Modifier
            .fillMaxWidth()
            .background(androidx.compose.ui.graphics.Brush.horizontalGradient(listOf(Color(0xFF2E7D32), Color(0xFF388E3C))))
            .padding(horizontal = 16.dp, vertical = 8.dp)
            .padding(bottom = 8.dp)
        ) {
          Box(modifier = Modifier.clickable { onSearchClick() }) {
            TextField(
              value = "",
              onValueChange = {},
              modifier = Modifier.fillMaxWidth().height(52.dp),
              placeholder = { Text("Search products, brands and stores", color = Color.Gray, fontSize = 14.sp) },
              leadingIcon = { Icon(Icons.Outlined.Search, contentDescription = null, tint = Color.Gray) },
              trailingIcon = {
                Row(verticalAlignment = Alignment.CenterVertically) {
                  Icon(Icons.Outlined.Mic, contentDescription = "Voice Search", tint = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(horizontal = 4.dp))
                  Icon(Icons.Outlined.CameraAlt, contentDescription = "Image Search", tint = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(end = 12.dp, start = 4.dp).clickable { onCameraClick() })
                }
              },
              shape = RoundedCornerShape(26.dp),
              colors = TextFieldDefaults.colors(
                unfocusedContainerColor = Color.White,
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

      item {
        // Banners
        AsyncImage(
          model = "https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?w=800&q=80",
          contentDescription = "Banner",
          contentScale = ContentScale.Crop,
          modifier = Modifier
            .fillMaxWidth()
            .height(180.dp)
            .padding(16.dp)
            .clip(RoundedCornerShape(16.dp))
        )
      }

"""

if start != -1 and end != -1:
    content = content[:start] + new_top + content[end:]
    with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
        f.write(content)
    print("Reverted Home")
else:
    print("Could not find start or end")

