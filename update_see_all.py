import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Replace the Circle Deals Header Row
start = content.find("        // Circle Deals")
end = content.find("        Spacer(modifier = Modifier.height(12.dp))", start)

new_header = """        // Circle Deals
        Row(
           modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),
           horizontalArrangement = Arrangement.SpaceBetween,
           verticalAlignment = Alignment.CenterVertically
        ) {
           Row(verticalAlignment = Alignment.CenterVertically) {
             Text("Circle Deals", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = Color.Black)
             Spacer(modifier = Modifier.width(8.dp))
             // Countdown Timer
             Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                 Box(modifier = Modifier.clip(RoundedCornerShape(4.dp)).background(Color(0xFFE53935)).padding(horizontal = 4.dp, vertical = 2.dp)) {
                     Text("02", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                 }
                 Text(":", color = Color(0xFFE53935), fontSize = 12.sp, fontWeight = FontWeight.Bold)
                 Box(modifier = Modifier.clip(RoundedCornerShape(4.dp)).background(Color(0xFFE53935)).padding(horizontal = 4.dp, vertical = 2.dp)) {
                     Text("45", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                 }
                 Text(":", color = Color(0xFFE53935), fontSize = 12.sp, fontWeight = FontWeight.Bold)
                 Box(modifier = Modifier.clip(RoundedCornerShape(4.dp)).background(Color(0xFFE53935)).padding(horizontal = 4.dp, vertical = 2.dp)) {
                     Text("12", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                 }
             }
           }
           Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.clickable { onCircleDealsClick() }) {
               Text("See All", color = MaterialTheme.colorScheme.primary, fontSize = 12.sp, fontWeight = FontWeight.Medium)
               Icon(Icons.Outlined.ChevronRight, contentDescription = "See All Deals", tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(16.dp))
           }
        }
"""

content = content[:start] + new_header + content[end:]
with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

