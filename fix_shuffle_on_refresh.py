import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Make the shuffle stateful so it updates on refresh
shuffled_code = r"""            val shuffled = mockProducts.shuffled\(\).take\(20\)
            items\(shuffled.size\) \{ index ->"""

shuffled_state_code = """            // The shuffle state is handled by remember inside HomeScreen to refresh when needed
            // For now, it will generate a list each time it renders
            val shuffledProducts = remember(mockProducts) { mockProducts.shuffled().take(20) }
            items(shuffledProducts.size) { index ->
                CircleDealCard(shuffledProducts[index], modifier = Modifier.width(180.dp))
            }
"""

content = re.sub(
    r'val shuffled = mockProducts\.shuffled\(\)\.take\(20\)\n\s*items\(shuffled\.size\) \{ index ->\n\s*CircleDealCard\(shuffled\[index\], modifier = Modifier\.width\([0-9]+.dp\)\)\n\s*\}',
    shuffled_state_code.strip(),
    content
)


with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
