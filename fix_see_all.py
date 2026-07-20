import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Remove the stray "See All" from inside the banner
content = re.sub(r'Text\("See All"[^\n]+\n\s*\}\n\s*\}\n\s*item \{\n\s*// Circle Deals Section', r'}\n      }\n\n      item {\n        // Circle Deals Section', content)

# Insert it back in the Circle Deals section
circle_deals_header_end = """             }
           }
           Text("See All", color = MaterialTheme.colorScheme.primary, fontSize = 12.sp, fontWeight = FontWeight.Medium, modifier = Modifier.clickable { onCircleDealsClick() })
        }
        Spacer(modifier = Modifier.height(12.dp))"""

content = re.sub(r'\s*\}\n\s*\}\n\s*\}\n\s*Spacer\(modifier = Modifier\.height\(12\.dp\)\)', circle_deals_header_end, content)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
