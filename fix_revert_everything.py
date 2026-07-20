import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Restore ProductCard and CircleDealCard and CategoryItem
product_card = """@Composable
fun ProductCard(product: Product, modifier: Modifier = Modifier) {
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
        Spacer(modifier = Modifier.height(8.dp))
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
          Row(verticalAlignment = Alignment.CenterVertically) {
            Icon(Icons.Filled.Star, contentDescription = "Rating", tint = Color(0xFFFFB300), modifier = Modifier.size(12.dp))
            Spacer(modifier = Modifier.width(2.dp))
            Text("${product.rating}", fontSize = 10.sp, color = Color.Black, fontWeight = FontWeight.Medium)
            Spacer(modifier = Modifier.width(2.dp))
            Text("(${product.soldCount})", fontSize = 10.sp, color = Color.Gray)
            Spacer(modifier = Modifier.width(4.dp))
            Text("|", fontSize = 10.sp, color = Color.LightGray)
            Spacer(modifier = Modifier.width(4.dp))
            Text("Sold ${if(product.soldCount >= 1000) "${product.soldCount/1000.0}k+".replace(".0k+", "k+") else "${product.soldCount}+"}", fontSize = 10.sp, color = Color.Gray)
          }
          Box(
            modifier = Modifier
              .size(28.dp)
              .clip(RoundedCornerShape(6.dp))
              .background(MaterialTheme.colorScheme.primary)
              .clickable { },
            contentAlignment = Alignment.Center
          ) {
            Icon(Icons.Outlined.ShoppingCart, contentDescription = "Add to Cart", tint = Color.White, modifier = Modifier.size(16.dp))
          }
        }
      }
    }
  }
}

@Composable
fun CircleDealCard(product: Product, modifier: Modifier = Modifier) {
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
                    ), label = "fireAlpha"
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

@Composable
fun CategoryItem(name: String, icon: androidx.compose.ui.graphics.vector.ImageVector) {
  Column(horizontalAlignment = Alignment.CenterHorizontally) {
    Box(
      modifier = Modifier
        .size(64.dp)
        .clip(CircleShape)
        .background(MaterialTheme.colorScheme.surface)
        .border(1.dp, MaterialTheme.colorScheme.outline, CircleShape)
        .clickable { },
      contentAlignment = Alignment.Center
    ) {
      Box(modifier = Modifier.size(32.dp).clip(RoundedCornerShape(8.dp)).background(MaterialTheme.colorScheme.secondaryContainer), contentAlignment = Alignment.Center) {
          Icon(icon, contentDescription = name, tint = MaterialTheme.colorScheme.onSecondaryContainer, modifier = Modifier.size(20.dp))
      }
    }
    Spacer(modifier = Modifier.height(8.dp))
    Text(name, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.Medium)
  }
}
"""

content = re.sub(
    r'@Composable\nfun CategoryItem\(name: String, icon: androidx.compose.ui.graphics.vector.ImageVector\) \{[\s\S]*?\n\}\n\n@Composable\nfun ProductCard\(product: Product, modifier: Modifier = Modifier, isCircleDeal: Boolean = false\) \{[\s\S]*?\n\}\n\n@Composable\nfun ProfileScreen',
    product_card + '\n\n@Composable\nfun ProfileScreen',
    content
)


# 2. Fix Circle Deals block in HomeScreen
home_circle_deals = """      item {
        LazyRow(
          contentPadding = PaddingValues(horizontal = 16.dp),
          horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
          items(mockProducts.take(5)) { product ->
            CircleDealCard(product)
          }
        }
      }
"""
content = re.sub(
    r'item \{\n\s*LazyRow\(\n\s*contentPadding = PaddingValues\(horizontal = 16\.dp\),\n\s*horizontalArrangement = Arrangement\.spacedBy\(12\.dp\)\n\s*\) \{\n\s*items\(mockProducts\.take\(5\)\) \{ product ->\n\s*ProductCard\(product, modifier = Modifier\.width\(140\.dp\), isCircleDeal = true\)\n\s*\}\n\s*\}\n\s*\}',
    home_circle_deals,
    content
)


# 3. Fix Categories block in HomeScreen spacing
content = re.sub(
    r'LazyRow\(\n\s*contentPadding = PaddingValues\(horizontal = 16\.dp\),\n\s*horizontalArrangement = Arrangement\.spacedBy\(12\.dp\)\n\s*\)',
    'LazyRow(\n          contentPadding = PaddingValues(horizontal = 16.dp),\n          horizontalArrangement = Arrangement.spacedBy(16.dp)\n        )',
    content
)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

