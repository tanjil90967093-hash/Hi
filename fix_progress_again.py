import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Make the stock count text larger and more visible
content = content.replace("Text(\"Only ${product.stock} Left\", fontSize = 11.sp, color = Color.DarkGray, fontWeight = FontWeight.Bold)", "Text(\"Only ${product.stock} Left\", fontSize = 12.sp, color = Color.Black, fontWeight = FontWeight.ExtraBold)")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
