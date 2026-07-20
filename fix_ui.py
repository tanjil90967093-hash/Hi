import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Fix banner height
content = content.replace("Modifier.fillMaxWidth().height(480.dp)", "Modifier.fillMaxWidth().height(280.dp)")

# Fix progress bar height which got replaced to 480.dp accidentally
old_progress_bar = """      Column(modifier = Modifier.fillMaxWidth()) {
         Box(modifier = Modifier.fillMaxWidth().height(280.dp).clip(RoundedCornerShape(3.dp)).background(Color(0xFFEEEEEE))) {
            Box(modifier = Modifier.fillMaxWidth(progress).height(6.dp).clip(RoundedCornerShape(3.dp)).background(Color(0xFF4CAF50)))
         }
         Spacer(modifier = Modifier.height(4.dp))
         Text("Only ${product.stock} Left", fontSize = 10.sp, color = Color.Gray, fontWeight = FontWeight.Medium)
      }"""

# Wait, if the previous script replaced 560.dp -> 480.dp, it might have replaced both! 
# Let me just use regex to target the progress bar specifically.

new_progress_bar = """      Column(modifier = Modifier.fillMaxWidth()) {
         Box(modifier = Modifier.fillMaxWidth().height(6.dp).clip(RoundedCornerShape(3.dp)).background(Color(0xFFE0E0E0))) {
            Box(modifier = Modifier.fillMaxWidth(progress).height(6.dp).clip(RoundedCornerShape(3.dp)).background(Color(0xFF4CAF50)))
         }
         Spacer(modifier = Modifier.height(4.dp))
         Text("Only ${product.stock} Left", fontSize = 11.sp, color = Color.DarkGray, fontWeight = FontWeight.Bold)
      }"""

content = re.sub(
    r'Column\(modifier = Modifier\.fillMaxWidth\(\)\) \{\n\s*Box\(modifier = Modifier\.fillMaxWidth\(\)\.height\([0-9]+\.dp\)\.clip\(RoundedCornerShape\(3\.dp\)\)\.background\(Color\(0xFFEEEEEE\)\)\) \{\n\s*Box\(modifier = Modifier\.fillMaxWidth\(progress\)\.height\(6\.dp\)\.clip\(RoundedCornerShape\(3\.dp\)\)\.background\(Color\(0xFF4CAF50\)\)\)\n\s*\}\n\s*Spacer\(modifier = Modifier\.height\(4\.dp\)\)\n\s*Text\("Only \$\{product\.stock\} Left", fontSize = 10\.sp, color = Color\.Gray, fontWeight = FontWeight\.Medium\)\n\s*\}',
    new_progress_bar,
    content
)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

