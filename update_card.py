with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Replace CircleDealCard
start = content.find("fun CircleDealCard(product: Product")
end = content.find("}", content.find("}", content.find("}", content.find("}", content.find("}", content.find("}", start) + 1) + 1) + 1) + 1) + 1) + 1
# Just replace everything from fun CircleDealCard to the end of file
new_card = """fun CircleDealCard(product: Product, modifier: Modifier = Modifier) {
  Card(
    modifier = modifier.width(180.dp).clickable { },
    colors = CardDefaults.cardColors(containerColor = Color.White),
    elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
    shape = RoundedCornerShape(12.dp)
  ) {
    Column(modifier = Modifier.padding(12.dp)) {
      Box(modifier = Modifier.fillMaxWidth().height(140.dp)) {
        AsyncImage(
          model = product.imageUrl,
          contentDescription = product.title,
          contentScale = ContentScale.Fit,
          modifier = Modifier.fillMaxSize().padding(8.dp)
        )
        if (product.discount != null) {
          Box(
            modifier = Modifier
              .align(Alignment.TopStart)
              .clip(RoundedCornerShape(4.dp))
              .background(Color(0xFFE53935))
              .padding(horizontal = 6.dp, vertical = 2.dp)
          ) {
            Text("-${product.discount}%", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold)
          }
        }
        Icon(
          Icons.Outlined.FavoriteBorder,
          contentDescription = "Favorite",
          tint = Color.DarkGray,
          modifier = Modifier.align(Alignment.TopEnd).size(20.dp).clickable { }
        )
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
      Spacer(modifier = Modifier.height(4.dp))
      
      Row(verticalAlignment = Alignment.CenterVertically) {
        Icon(Icons.Filled.Star, contentDescription = "Rating", tint = Color(0xFFFFB300), modifier = Modifier.size(12.dp))
        Spacer(modifier = Modifier.width(2.dp))
        Text("${product.rating}", fontSize = 10.sp, color = Color.Black, fontWeight = FontWeight.Medium)
        Spacer(modifier = Modifier.width(4.dp))
        Text("|", fontSize = 10.sp, color = Color.LightGray)
        Spacer(modifier = Modifier.width(4.dp))
        Text("Sold ${if(product.soldCount >= 1000) "${product.soldCount/1000.0}k+".replace(".0k+", "k+") else "${product.soldCount}+"}", fontSize = 10.sp, color = Color.Gray)
      }
      Spacer(modifier = Modifier.height(6.dp))
      
      Row(verticalAlignment = Alignment.Bottom, horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
        Column {
            Text(
              "৳ ${product.price.toInt()}",
              style = MaterialTheme.typography.titleMedium,
              fontWeight = FontWeight.Bold,
              color = Color(0xFFE53935)
            )
            if (product.oldPrice != null) {
              Text(
                "৳ ${product.oldPrice.toInt()}",
                style = MaterialTheme.typography.bodySmall,
                color = Color.Gray,
                textDecoration = TextDecoration.LineThrough,
                fontSize = 10.sp
              )
            }
        }
        Box(
          modifier = Modifier
            .size(28.dp)
            .clip(RoundedCornerShape(6.dp))
            .background(Color(0xFFE53935))
            .clickable { },
          contentAlignment = Alignment.Center
        ) {
          Icon(Icons.Outlined.ShoppingCart, contentDescription = "Add to Cart", tint = Color.White, modifier = Modifier.size(16.dp))
        }
      }
      Spacer(modifier = Modifier.height(8.dp))
      
      // Stock Progress Bar
      val progress = product.stock.toFloat() / product.maxStock.toFloat()
      Column(modifier = Modifier.fillMaxWidth()) {
         Box(modifier = Modifier.fillMaxWidth().height(6.dp).clip(RoundedCornerShape(3.dp)).background(Color.LightGray)) {
            Box(modifier = Modifier.fillMaxWidth(progress).height(6.dp).clip(RoundedCornerShape(3.dp)).background(Color(0xFFE53935)))
         }
         Spacer(modifier = Modifier.height(4.dp))
         Text("${product.stock} available", fontSize = 10.sp, color = Color.Gray)
      }
    }
  }
}
"""

content = content[:start] + new_card
with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
