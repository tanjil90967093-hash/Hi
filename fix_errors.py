with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Fix SectionTitle
content = content.replace("fun SectionTitle(title: String, action: String) {", "@Composable\nfun SectionTitle(title: String, action: String) {")

# Fix Text quotes
content = content.replace('Text("Try saying "Smart Watches"", color = Color.Gray)', 'Text("Try saying \\"Smart Watches\\"", color = Color.Gray)')

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
