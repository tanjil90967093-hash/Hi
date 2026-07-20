import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Fix the remember being called inside LazyHorizontalGrid scope where it shouldn't be
# Move it up inside HomeScreen composable

# Find the block and replace
bad_code = r"""        \} \{
            // The shuffle state is handled by remember inside HomeScreen to refresh when needed
            // For now, it will generate a list each time it renders
            val shuffledProducts = remember\(mockProducts\) \{ mockProducts\.shuffled\(\)\.take\(20\) \}
            items\(shuffledProducts\.size\) \{ index ->
                CircleDealCard\(shuffledProducts\[index\], modifier = Modifier\.width\(180\.dp\)\)
            \}
        \}"""

good_code = """        } {
            items(mockProducts.shuffled().take(20).size) { index ->
                CircleDealCard(mockProducts[index], modifier = Modifier.width(180.dp))
            }
        }"""

content = re.sub(bad_code, good_code, content)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
