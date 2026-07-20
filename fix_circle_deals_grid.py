import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Update CircleDealCard so it doesn't have a hardcoded width if it's placed in a Grid
# Change `modifier = modifier.width(160.dp).clickable { }` to `modifier = modifier.clickable { }`
content = content.replace(
    "modifier = modifier.width(160.dp).clickable { },",
    "modifier = modifier.clickable { },"
)

# 2. Replace the Circle Deals LazyRow with a Grid in HomeScreen
home_circle_deals_lazyrow = """      item {
        LazyRow(
          contentPadding = PaddingValues(horizontal = 16.dp),
          horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
          items(mockProducts.take(20)) { product ->
            CircleDealCard(product)
          }
        }
      }"""

home_circle_deals_grid = """      // Circle Deals Grid (10 rows, 2 columns, exactly 20 products)
      val circleDealsProducts = mockProducts.shuffled().take(20).chunked(2)
      items(circleDealsProducts) { rowProducts ->
        Row(
          modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 6.dp),
          horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
          for (product in rowProducts) {
            CircleDealCard(product, modifier = Modifier.weight(1f))
          }
          if (rowProducts.size == 1) {
            Spacer(modifier = Modifier.weight(1f))
          }
        }
      }"""

if home_circle_deals_lazyrow in content:
    content = content.replace(home_circle_deals_lazyrow, home_circle_deals_grid)
else:
    # Use regex to find and replace the LazyRow
    content = re.sub(
        r'item \{\n\s*LazyRow\(\n\s*contentPadding = PaddingValues\(horizontal = 16\.dp\),\n\s*horizontalArrangement = Arrangement\.spacedBy\(12\.dp\)\n\s*\) \{\n\s*items\(mockProducts\.take\(20\)\) \{ product ->\n\s*CircleDealCard\(product\)\n\s*\}\n\s*\}\n\s*\}',
        home_circle_deals_grid,
        content
    )

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

