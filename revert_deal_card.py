import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Let's completely revert ProductCard to a simple version that matches original.
# Wait, I don't have the original code saved. But I can reconstruct it from memory of typical templates or from the git history if it existed.
# Since it's not a git repo, I'll just write a standard ProductCard that looks like the original.
# The original had: Title, price, oldPrice, and a progress bar for "Sold".
original_product_card = """@Composable
fun ProductCard(product: Product, modifier: Modifier = Modifier, isCircleDeal: Boolean = false) {
  Card(
    modifier = modifier.fillMaxWidth(),
    colors = CardDefaults.cardColors(containerColor = Color.White),
    elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
    shape = RoundedCornerShape(8.dp)
  ) {
    Column {
      Box(modifier = Modifier.fillMaxWidth().aspectRatio(1f).background(Color(0xFFF5F5F5))) {
        AsyncImage(
          model = product.imageUrl,
          contentDescription = product.title,
          contentScale = ContentScale.Crop,
          modifier = Modifier.fillMaxSize()
        )
        if (product.discount != null) {
          Box(
            modifier = Modifier
              .align(Alignment.TopEnd)
              .background(MaterialTheme.colorScheme.primary, RoundedCornerShape(bottomStart = 8.dp))
              .padding(horizontal = 8.dp, vertical = 4.dp)
          ) {
            Text("${product.discount}% OFF", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold)
          }
        }
      }
      Column(modifier = Modifier.padding(8.dp)) {
        Text(
          product.title,
          style = MaterialTheme.typography.bodyMedium,
          maxLines = 2,
          overflow = TextOverflow.Ellipsis
        )
        Spacer(modifier = Modifier.height(4.dp))
        Row(verticalAlignment = Alignment.CenterVertically) {
          Text(
            "৳ ${product.price.toInt()}",
            style = MaterialTheme.typography.titleMedium,
            color = MaterialTheme.colorScheme.primary,
            fontWeight = FontWeight.Bold
          )
          if (product.oldPrice != null) {
            Spacer(modifier = Modifier.width(4.dp))
            Text(
              "৳ ${product.oldPrice.toInt()}",
              style = MaterialTheme.typography.bodySmall,
              color = Color.Gray,
              textDecoration = TextDecoration.LineThrough
            )
          }
        }
        if (isCircleDeal) {
          Spacer(modifier = Modifier.height(8.dp))
          LinearProgressIndicator(
            progress = { product.soldCount.toFloat() / product.maxStock.toFloat() },
            modifier = Modifier.fillMaxWidth().height(4.dp).clip(RoundedCornerShape(2.dp)),
            color = MaterialTheme.colorScheme.primary,
            trackColor = Color(0xFFEEEEEE),
          )
          Spacer(modifier = Modifier.height(4.dp))
          Text("${product.soldCount} Sold", fontSize = 10.sp, color = Color.Gray)
        }
      }
    }
  }
}"""

content = re.sub(
    r'@Composable\nfun ProductCard\(product: Product, modifier: Modifier = Modifier, isCircleDeal: Boolean = false\) \{[\s\S]*?\n\}\n\n@Composable\nfun ProfileScreen',
    original_product_card + '\n\n@Composable\nfun ProfileScreen',
    content
)

# And fix Circle Deals section spacing.
# The user said "Circle Deals title is inside the banner". 
# The banner box currently has:
# Box(modifier = Modifier.fillMaxWidth().height(260.dp))
# Let's check how the Banner and Circle Deals are arranged. They are in the same LazyColumn.
# item { Box(Banner...) }
# item { Row(CIRCLE DEALS...) }
# They should not overlap unless there is negative padding or the banner Box doesn't take enough height.
# Wait, maybe the Search bar inside the Banner Box has some weird alignment that pushes things?
# Actually, the user says "ব্যানার ভিতরে ঢুকে গেছে এটা একটু নিচে করে দিতে" (It entered the banner, move it down).
# Maybe we just need a Spacer between the Banner and the Circle Deals section.
content = content.replace(
    '// Circle Deals Section\n        Row(',
    '// Spacer to separate banner and deals\n        Spacer(modifier = Modifier.height(24.dp))\n        // Circle Deals Section\n        Row('
)

# Also revert Home Page Circle Deals from 10 rows grid back to LazyRow.
# User was angry about "categories spread out" - I didn't change categories but I changed Circle Deals to a Grid of 10 rows in Home Page!
# Let's revert that to a LazyRow!

circle_deals_lazyrow = """        // Spacer to separate banner and deals
        Spacer(modifier = Modifier.height(24.dp))
        // Circle Deals Section
        Row(
           modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),
           horizontalArrangement = Arrangement.SpaceBetween,
           verticalAlignment = Alignment.CenterVertically
        ) {
           Row(verticalAlignment = Alignment.CenterVertically) {
             val infiniteTransition = androidx.compose.animation.core.rememberInfiniteTransition(label = "shimmer")
             val translateAnim = infiniteTransition.animateFloat(
                initialValue = 0f,
                targetValue = 1000f,
                animationSpec = androidx.compose.animation.core.infiniteRepeatable(
                    animation = androidx.compose.animation.core.tween(durationMillis = 3000, easing = androidx.compose.animation.core.LinearEasing),
                    repeatMode = androidx.compose.animation.core.RepeatMode.Restart
                ), label = "shimmerTranslate"
             )
             val brush = androidx.compose.ui.graphics.Brush.linearGradient(
                colors = listOf(Color(0xFF4CAF50), Color(0xFFFFC107), Color(0xFFFF9800), Color(0xFFFFD700), Color(0xFF4CAF50)),
                start = androidx.compose.ui.geometry.Offset(translateAnim.value, translateAnim.value),
                end = androidx.compose.ui.geometry.Offset(translateAnim.value + 200f, translateAnim.value + 200f)
             )
             Text(
                text = "CIRCLE DEALS", 
                style = MaterialTheme.typography.titleLarge.copy(
                    fontWeight = FontWeight.ExtraBold,
                    letterSpacing = 1.sp,
                    brush = brush,
                    shadow = androidx.compose.ui.graphics.Shadow(
                        color = Color(0xFFFFC107).copy(alpha = 0.5f), 
                        offset = androidx.compose.ui.geometry.Offset(0f, 4f), 
                        blurRadius = 8f
                    )
                )
             )
             Spacer(modifier = Modifier.width(12.dp))
             val timerBg = Color(0xFFFFB300)
             val timerText = Color.Black
             Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                 Box(modifier = Modifier.clip(RoundedCornerShape(6.dp)).background(timerBg).padding(horizontal = 6.dp, vertical = 3.dp)) {
                     Text("02", color = timerText, fontSize = 12.sp, fontWeight = FontWeight.ExtraBold)
                 }
                 Text(":", color = timerBg, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                 Box(modifier = Modifier.clip(RoundedCornerShape(6.dp)).background(timerBg).padding(horizontal = 6.dp, vertical = 3.dp)) {
                     Text("45", color = timerText, fontSize = 12.sp, fontWeight = FontWeight.ExtraBold)
                 }
                 Text(":", color = timerBg, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                 Box(modifier = Modifier.clip(RoundedCornerShape(6.dp)).background(timerBg).padding(horizontal = 6.dp, vertical = 3.dp)) {
                     Text("12", color = timerText, fontSize = 12.sp, fontWeight = FontWeight.ExtraBold)
                 }
             }
           }
           Text("See All", color = MaterialTheme.colorScheme.primary, fontSize = 12.sp, fontWeight = FontWeight.Medium, modifier = Modifier.clickable { onCircleDealsClick() })
        }
        Spacer(modifier = Modifier.height(12.dp))
      }
      
      item {
        LazyRow(
          contentPadding = PaddingValues(horizontal = 16.dp),
          horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
          items(mockProducts.take(5)) { product ->
            ProductCard(product, modifier = Modifier.width(140.dp), isCircleDeal = true)
          }
        }
      }
"""

# Replace the Circle Deals Grid (from `// Spacer to separate banner and deals\n        // Circle Deals Section\n` up to `SectionTitle("Categories"`)
content = re.sub(
    r'// Spacer to separate banner and deals\n\s*// Circle Deals Section\n\s*Row\([\s\S]*?item \{\n\s*Spacer\(modifier = Modifier\.height\(24\.dp\)\)\n\s*SectionTitle\("Categories"',
    circle_deals_lazyrow + '\n      item {\n        Spacer(modifier = Modifier.height(24.dp))\n        SectionTitle("Categories"',
    content
)


with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
