import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Update CircleDealCard to match the requested design in the image
circle_deal_card = """@Composable
fun CircleDealCard(product: Product, modifier: Modifier = Modifier) {
  Card(
    modifier = modifier.clickable { },
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
    r'@Composable\nfun CircleDealCard\(product: Product, modifier: Modifier = Modifier\) \{[\s\S]*?\n\}\n\n@Composable\nfun CategoryItem',
    circle_deal_card + '\n\n@Composable\nfun CategoryItem',
    content
)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
