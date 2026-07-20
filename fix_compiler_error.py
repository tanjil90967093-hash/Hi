import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Fix the compiler error about `@Composable invocations can only happen from the context of a @Composable function`
# I missed removing `val shuffledProducts = remember(mockProducts) { mockProducts.shuffled().take(20) }` from inside the LazyHorizontalGrid scope

lazy_grid = r"""        androidx.compose.foundation.lazy.grid.LazyHorizontalGrid\(
            rows = androidx.compose.foundation.lazy.grid.GridCells.Fixed\(2\),
            contentPadding = PaddingValues\(horizontal = 16.dp\),
            horizontalArrangement = Arrangement.spacedBy\(12.dp\),
            verticalArrangement = Arrangement.spacedBy\(12.dp\),
            modifier = Modifier.fillMaxWidth\(\).height\(580.dp\) // Approximate height for 2 rows of 260dp cards \+ spacing
        \) \{
            // The shuffle state is handled by remember inside HomeScreen to refresh when needed
            // For now, it will generate a list each time it renders
            val shuffledProducts = remember\(mockProducts\) \{ mockProducts.shuffled\(\).take\(20\) \}
            items\(shuffledProducts.size\) \{ index ->
                CircleDealCard\(shuffledProducts\[index\], modifier = Modifier.width\(180.dp\)\)
            \}
        \}"""

fixed_lazy_grid = """        androidx.compose.foundation.lazy.grid.LazyHorizontalGrid(
            rows = androidx.compose.foundation.lazy.grid.GridCells.Fixed(2),
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
            modifier = Modifier.fillMaxWidth().height(580.dp) // Approximate height for 2 rows of 260dp cards + spacing
        ) {
            items(circleDealsList.size) { index ->
                CircleDealCard(circleDealsList[index], modifier = Modifier.width(180.dp))
            }
        }"""

content = re.sub(lazy_grid, fixed_lazy_grid, content)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
