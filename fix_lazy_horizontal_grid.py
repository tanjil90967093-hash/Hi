import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Replace the Grid (which is making the page too long) with a LazyHorizontalGrid
grid_code = r"""      // Circle Deals Grid \(10 rows, 2 columns, exactly 20 products\)
      val circleDealsProducts = mockProducts.take\(20\).chunked\(2\)
      items\(circleDealsProducts\) \{ rowProducts ->
        Row\(
          modifier = Modifier
            .fillMaxWidth\(\)
            .padding\(horizontal = 16.dp, vertical = 6.dp\),
          horizontalArrangement = Arrangement.spacedBy\(12.dp\)
        \) \{
          for \(product in rowProducts\) \{
            ProductCard\(product, modifier = Modifier.weight\(1f\)\)
          \}
          if \(rowProducts.size == 1\) \{
            Spacer\(modifier = Modifier.weight\(1f\)\)
          \}
        \}
      \}"""

lazy_horizontal_grid_code = """      item {
        androidx.compose.foundation.lazy.grid.LazyHorizontalGrid(
            rows = androidx.compose.foundation.lazy.grid.GridCells.Fixed(2),
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
            modifier = Modifier.fillMaxWidth().height(560.dp) // Approximate height for 2 rows of 260dp cards + spacing
        ) {
            val shuffled = mockProducts.shuffled().take(20)
            items(shuffled.size) { index ->
                CircleDealCard(shuffled[index], modifier = Modifier.width(160.dp))
            }
        }
      }"""

content = re.sub(grid_code, lazy_horizontal_grid_code, content)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
