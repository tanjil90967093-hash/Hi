import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Replace CircleDealCard
start = content.find("fun CircleDealCard(product: Product")
end = content.find("}", content.find("}", content.find("}", content.find("}", content.find("}", content.find("}", start) + 1) + 1) + 1) + 1) + 1) + 1

new_card = """fun CircleDealCard(product: Product, modifier: Modifier = Modifier) {
  Card(
    modifier = modifier.width(160.dp).clickable { },
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
      
      Row(verticalAlignment = Alignment.Bottom, modifier = Modifier.fillMaxWidth()) {
        Text(
          "৳ ${product.price.toInt()}",
          style = MaterialTheme.typography.titleMedium,
          fontWeight = FontWeight.Bold,
          color = Color(0xFFE53935)
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
      val sold = product.maxStock - product.stock
      val progress = sold.toFloat() / product.maxStock.toFloat()
      val isLastItem = product.stock == 1
      
      Column(modifier = Modifier.fillMaxWidth()) {
         Box(modifier = Modifier.fillMaxWidth().height(6.dp).clip(RoundedCornerShape(3.dp)).background(Color.LightGray)) {
            // Normal green, but red/orange at the end if it's the last item
            val barBrush = if (isLastItem) {
                androidx.compose.ui.graphics.Brush.horizontalGradient(
                    0.0f to Color(0xFF388E3C),
                    0.7f to Color(0xFF388E3C),
                    1.0f to Color(0xFFFF5722)
                )
            } else {
                androidx.compose.ui.graphics.Brush.horizontalGradient(listOf(Color(0xFF388E3C), Color(0xFF388E3C)))
            }
            
            Box(modifier = Modifier.fillMaxWidth(progress).height(6.dp).clip(RoundedCornerShape(3.dp)).background(barBrush))
            
            if (isLastItem && progress > 0f) {
                // Fire animation
                val infiniteTransition = androidx.compose.animation.core.rememberInfiniteTransition()
                val alpha by infiniteTransition.animateFloat(
                    initialValue = 0.5f,
                    targetValue = 1f,
                    animationSpec = androidx.compose.animation.core.infiniteRepeatable(
                        animation = androidx.compose.animation.core.tween(500),
                        repeatMode = androidx.compose.animation.core.RepeatMode.Reverse
                    )
                )
                Icon(
                    Icons.Filled.LocalFireDepartment,
                    contentDescription = "Hot",
                    tint = Color(0xFFFF5722).copy(alpha = alpha),
                    modifier = Modifier.align(Alignment.CenterStart).offset(x = 136.dp * progress - 8.dp).size(12.dp) // Approximate offset based on card width (160 - 24 padding = 136 width)
                )
            }
         }
         Spacer(modifier = Modifier.height(4.dp))
         Text(if (isLastItem) "Only 1 Left" else "Only ${product.stock} Left", fontSize = 10.sp, color = if (isLastItem) Color(0xFFFF5722) else Color.Gray, fontWeight = if (isLastItem) FontWeight.Bold else FontWeight.Normal)
      }
    }
  }
}
"""

content = content[:start] + new_card + content[end:]
with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
