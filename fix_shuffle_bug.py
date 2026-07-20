import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Fix my bug from previous step where I passed `mockProducts[index]` instead of the shuffled one
content = content.replace("items(mockProducts.shuffled().take(20).size) { index ->", "items(mockProducts.size) { index ->")

# We want 20 products. Let's do `items(20)` and use `mockProducts.shuffled()[index % mockProducts.size]` if size < 20, but size is 10.
# The user wants 20 products, so we'll just repeat the 10 products if needed.
# Let's fix this properly.

# Let's define it inside the composable correctly.
# Move to the top of HomeScreen:
top_of_homescreen = """@Composable
fun HomeScreen(onSearchClick: () -> Unit = {}, onCameraClick: () -> Unit = {}, onCircleDealsClick: () -> Unit = {}) {
  val listState = rememberLazyListState()"""

top_with_shuffled = """@Composable
fun HomeScreen(onSearchClick: () -> Unit = {}, onCameraClick: () -> Unit = {}, onCircleDealsClick: () -> Unit = {}) {
  val listState = rememberLazyListState()
  // Generate 20 products by repeating and shuffling
  val circleDealsList = remember { 
      val doubled = mockProducts + mockProducts
      doubled.shuffled().take(20) 
  }"""

content = content.replace(top_of_homescreen, top_with_shuffled)

bad_lazy_content = """            items(mockProducts.size) { index ->
                CircleDealCard(mockProducts[index], modifier = Modifier.width(180.dp))
            }"""

good_lazy_content = """            items(circleDealsList.size) { index ->
                CircleDealCard(circleDealsList[index], modifier = Modifier.width(180.dp))
            }"""

content = content.replace(bad_lazy_content, good_lazy_content)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
