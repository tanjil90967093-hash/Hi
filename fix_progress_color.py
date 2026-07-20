import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Make the stock count text color primary
content = content.replace("Text(\"Only ${product.stock} Left\", fontSize = 12.sp, color = Color.Black, fontWeight = FontWeight.ExtraBold)", "Text(\"Only ${product.stock} Left\", fontSize = 12.sp, color = Color(0xFF4CAF50), fontWeight = FontWeight.ExtraBold)")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
