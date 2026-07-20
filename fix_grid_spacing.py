import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Update Just For You Products Grid padding
old_products_grid = """      // Products Grid
      val chunkedProducts = mockProducts.chunked(2)
      items(chunkedProducts) { rowProducts ->
        Row(
          modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp),
          horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {"""

new_products_grid = """      // Products Grid
      val chunkedProducts = mockProducts.chunked(2)
      items(chunkedProducts) { rowProducts ->
        Row(
          modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 8.dp, vertical = 6.dp),
          horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {"""

content = content.replace(old_products_grid, new_products_grid)

# Update Circle Deals Screen (the dedicated page) padding
old_circle_deals_screen_grid = """              Row(
                  modifier = Modifier
                      .fillMaxWidth()
                      .padding(horizontal = 16.dp, vertical = 8.dp),
                  horizontalArrangement = Arrangement.spacedBy(16.dp)
              ) {"""

new_circle_deals_screen_grid = """              Row(
                  modifier = Modifier
                      .fillMaxWidth()
                      .padding(horizontal = 8.dp, vertical = 6.dp),
                  horizontalArrangement = Arrangement.spacedBy(8.dp)
              ) {"""

content = content.replace(old_circle_deals_screen_grid, new_circle_deals_screen_grid)


with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
