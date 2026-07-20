import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Make search bar icons cleaner
old_search_bar_icons = """                  Icon(Icons.Outlined.Search, contentDescription = "Search", tint = Color.Gray)
                  Spacer(Modifier.width(8.dp))
                  Text("Search products, brands and stores", color = Color.Gray, fontSize = 14.sp, modifier = Modifier.weight(1f))
                  Icon(
                      Icons.Outlined.CameraAlt, 
                      contentDescription = "Image Search", 
                      tint = MaterialTheme.colorScheme.primary, 
                      modifier = Modifier.padding(horizontal = 8.dp).size(20.dp).clickable(
                         interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() },
                         indication = null
                      ) { 
                         try { context.startActivity(chooserIntent) } catch(e: Exception) {} 
                      }
                  )
                  Icon(
                      Icons.Outlined.Mic, 
                      contentDescription = "Voice Search", 
                      tint = MaterialTheme.colorScheme.primary, 
                      modifier = Modifier.size(20.dp).clickable(
                         interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() },
                         indication = null
                      ) { 
                         try { context.startActivity(voiceIntent) } catch(e: Exception) {} 
                      }
                  )"""

new_search_bar_icons = """                  Icon(Icons.Outlined.Search, contentDescription = "Search", tint = Color(0xFF757575))
                  Spacer(Modifier.width(8.dp))
                  Text("Search Circle Bazar", color = Color(0xFF9E9E9E), fontSize = 14.sp, modifier = Modifier.weight(1f))
                  Icon(
                      Icons.Filled.CameraAlt, 
                      contentDescription = "Image Search", 
                      tint = Color(0xFF2E7D32), 
                      modifier = Modifier.padding(horizontal = 8.dp).size(22.dp).clickable(
                         interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() },
                         indication = null
                      ) { 
                         try { context.startActivity(chooserIntent) } catch(e: Exception) {} 
                      }
                  )
                  Icon(
                      Icons.Filled.Mic, 
                      contentDescription = "Voice Search", 
                      tint = Color(0xFF2E7D32), 
                      modifier = Modifier.size(22.dp).clickable(
                         interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() },
                         indication = null
                      ) { 
                         try { context.startActivity(voiceIntent) } catch(e: Exception) {} 
                      }
                  )"""

content = content.replace(old_search_bar_icons, new_search_bar_icons)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

