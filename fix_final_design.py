import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Update ProductCard
product_card = """@Composable
fun ProductCard(product: Product, modifier: Modifier = Modifier) {
  Card(
    modifier = modifier.fillMaxWidth(),
    colors = CardDefaults.cardColors(containerColor = Color.White),
    elevation = CardDefaults.cardElevation(defaultElevation = 0.dp),
    shape = RoundedCornerShape(8.dp),
    border = BorderStroke(1.dp, Color(0xFF4CAF50))
  ) {
    Column(modifier = Modifier.padding(12.dp)) {
      Box(modifier = Modifier.fillMaxWidth().aspectRatio(1f)) {
        AsyncImage(
          model = product.imageUrl,
          contentDescription = product.title,
          contentScale = ContentScale.Fit,
          modifier = Modifier.fillMaxSize()
        )
        if (product.discount != null) {
          Box(
            modifier = Modifier
              .align(Alignment.TopStart)
              .clip(RoundedCornerShape(4.dp))
              .background(Color(0xFF4CAF50))
              .padding(horizontal = 6.dp, vertical = 4.dp)
          ) {
            Text("-${product.discount}%", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold)
          }
        }
        Icon(
          Icons.Outlined.FavoriteBorder,
          contentDescription = "Favorite",
          tint = Color.Black,
          modifier = Modifier.align(Alignment.TopEnd).size(20.dp).clickable { }
        )
      }
      Spacer(modifier = Modifier.height(12.dp))
      Text(
        product.title,
        style = MaterialTheme.typography.bodyMedium,
        maxLines = 1,
        overflow = TextOverflow.Ellipsis,
        color = Color.Black
      )
      Spacer(modifier = Modifier.height(6.dp))
      Row(verticalAlignment = Alignment.CenterVertically) {
        Text(
          "৳ ${product.price.toInt()}",
          style = MaterialTheme.typography.titleMedium,
          color = Color(0xFF4CAF50),
          fontWeight = FontWeight.Bold
        )
        if (product.oldPrice != null) {
          Spacer(modifier = Modifier.width(6.dp))
          Text(
            "৳ ${product.oldPrice.toInt()}",
            style = MaterialTheme.typography.bodySmall,
            color = Color.Gray,
            textDecoration = TextDecoration.LineThrough
          )
        }
      }
      Spacer(modifier = Modifier.height(6.dp))
      Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
        Row(verticalAlignment = Alignment.CenterVertically) {
          Icon(Icons.Filled.Star, contentDescription = "Rating", tint = Color(0xFFFFC107), modifier = Modifier.size(14.dp))
          Spacer(modifier = Modifier.width(4.dp))
          Text("${product.rating}", fontSize = 11.sp, color = Color.Black, fontWeight = FontWeight.Medium)
          Spacer(modifier = Modifier.width(2.dp))
          Text("(${product.soldCount})", fontSize = 11.sp, color = Color.Gray)
          Spacer(modifier = Modifier.width(4.dp))
          Text("|", fontSize = 11.sp, color = Color.LightGray)
          Spacer(modifier = Modifier.width(4.dp))
          Text("Sold ${if(product.soldCount >= 1000) "${product.soldCount/1000.0}k+".replace(".0k+", "k+") else "${product.soldCount}+"}", fontSize = 11.sp, color = Color.Gray)
        }
        Box(
          modifier = Modifier
            .size(32.dp)
            .clip(RoundedCornerShape(8.dp))
            .background(Color(0xFF4CAF50))
            .clickable { },
          contentAlignment = Alignment.Center
        ) {
          Icon(Icons.Outlined.ShoppingCart, contentDescription = "Add to Cart", tint = Color.White, modifier = Modifier.size(18.dp))
        }
      }
    }
  }
}"""

content = re.sub(
    r'@Composable\nfun ProductCard\(product: Product, modifier: Modifier = Modifier\) \{[\s\S]*?\n\}\n\n@Composable\nfun CircleDealCard',
    product_card + '\n\n@Composable\nfun CircleDealCard',
    content
)

# Update CircleDealCard
circle_deal_card = """@Composable
fun CircleDealCard(product: Product, modifier: Modifier = Modifier) {
  Card(
    modifier = modifier.width(160.dp).clickable { },
    colors = CardDefaults.cardColors(containerColor = Color.White),
    elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
    shape = RoundedCornerShape(8.dp)
  ) {
    Column(modifier = Modifier.padding(12.dp)) {
      Box(modifier = Modifier.fillMaxWidth().height(120.dp)) {
        AsyncImage(
          model = product.imageUrl,
          contentDescription = product.title,
          contentScale = ContentScale.Fit,
          modifier = Modifier.fillMaxSize()
        )
        if (product.discount != null) {
          Box(
            modifier = Modifier
              .align(Alignment.TopStart)
              .clip(RoundedCornerShape(4.dp))
              .background(Color(0xFF4CAF50))
              .padding(horizontal = 6.dp, vertical = 4.dp)
          ) {
            Text("-${product.discount}%", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold)
          }
        }
      }
      Spacer(modifier = Modifier.height(8.dp))
      Text(
        product.title,
        style = MaterialTheme.typography.labelMedium,
        fontWeight = FontWeight.Medium,
        maxLines = 1,
        overflow = TextOverflow.Ellipsis,
        color = Color.Black
      )
      Spacer(modifier = Modifier.height(6.dp))
      
      Row(verticalAlignment = Alignment.Bottom, modifier = Modifier.fillMaxWidth()) {
        Text(
          "৳ ${product.price.toInt()}",
          style = MaterialTheme.typography.titleMedium,
          fontWeight = FontWeight.Bold,
          color = Color(0xFF4CAF50)
        )
        if (product.oldPrice != null) {
          Spacer(modifier = Modifier.width(4.dp))
          Text(
            "৳ ${product.oldPrice.toInt()}",
            style = MaterialTheme.typography.bodySmall,
            color = Color.Gray,
            textDecoration = TextDecoration.LineThrough,
            fontSize = 10.sp
          )
        }
      }
      Spacer(modifier = Modifier.height(8.dp))
      
      // Stock Progress Bar
      val progress = product.stock.toFloat() / product.maxStock.toFloat()
      
      Column(modifier = Modifier.fillMaxWidth()) {
         Box(modifier = Modifier.fillMaxWidth().height(6.dp).clip(RoundedCornerShape(3.dp)).background(Color(0xFFEEEEEE))) {
            Box(modifier = Modifier.fillMaxWidth(progress).height(6.dp).clip(RoundedCornerShape(3.dp)).background(Color(0xFF4CAF50)))
         }
         Spacer(modifier = Modifier.height(4.dp))
         Text("Only ${product.stock} Left", fontSize = 10.sp, color = Color.Gray)
      }
    }
  }
}"""

content = re.sub(
    r'@Composable\nfun CircleDealCard\(product: Product, modifier: Modifier = Modifier\) \{[\s\S]*?\n\}\n\n@Composable\nfun CategoryItem',
    circle_deal_card + '\n\n@Composable\nfun CategoryItem',
    content
)

# Fix Circle Deals list to show 20 products
content = re.sub(
    r'items\(mockProducts\.take\(5\)\) \{ product ->\n\s*CircleDealCard\(product\)\n\s*\}',
    'items(mockProducts.take(20)) { product ->\n            CircleDealCard(product)\n          }',
    content
)

# Rename See All to Show More
content = content.replace(
    'Text("See All", color = MaterialTheme.colorScheme.primary, fontSize = 12.sp, fontWeight = FontWeight.Medium, modifier = Modifier.clickable { onCircleDealsClick() })',
    'Text("Show More", color = MaterialTheme.colorScheme.primary, fontSize = 12.sp, fontWeight = FontWeight.Medium, modifier = Modifier.clickable { onCircleDealsClick() })'
)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
