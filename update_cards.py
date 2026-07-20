import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Update ProductCard
product_card_old = r"""@Composable
fun ProductCard\(product: Product, modifier: Modifier = Modifier\) \{[\s\S]*?fun CircleDealCard"""

product_card_new = """@Composable
fun ProductCard(product: Product, modifier: Modifier = Modifier) {
  Card(
    modifier = modifier.fillMaxWidth(),
    colors = CardDefaults.cardColors(containerColor = Color.White),
    elevation = CardDefaults.cardElevation(defaultElevation = 0.dp),
    shape = RoundedCornerShape(8.dp),
    border = BorderStroke(1.dp, Color(0xFF4CAF50))
  ) {
    Box {
      Column(modifier = Modifier.padding(10.dp)) {
        Box(modifier = Modifier.fillMaxWidth().aspectRatio(1f).padding(top = 12.dp)) {
          AsyncImage(
            model = product.imageUrl,
            contentDescription = product.title,
            contentScale = ContentScale.Fit,
            modifier = Modifier.fillMaxSize()
          )
        }
        Spacer(modifier = Modifier.height(8.dp))
        Text(
          product.title,
          style = MaterialTheme.typography.bodyMedium,
          maxLines = 1,
          overflow = TextOverflow.Ellipsis,
          color = Color.Black
        )
        Spacer(modifier = Modifier.height(4.dp))
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
        Spacer(modifier = Modifier.height(8.dp))
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
          Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.weight(1f)) {
            Icon(Icons.Filled.Star, contentDescription = "Rating", tint = Color(0xFFFFC107), modifier = Modifier.size(14.dp))
            Spacer(modifier = Modifier.width(2.dp))
            Text("${product.rating}", fontSize = 11.sp, color = Color.Black, fontWeight = FontWeight.Medium)
            Spacer(modifier = Modifier.width(2.dp))
            Text("(${product.soldCount})", fontSize = 10.sp, color = Color.Gray, maxLines = 1, overflow = TextOverflow.Ellipsis)
            Spacer(modifier = Modifier.width(2.dp))
            Text("|", fontSize = 10.sp, color = Color.LightGray)
            Spacer(modifier = Modifier.width(2.dp))
            Text("Sold ${if(product.soldCount >= 1000) "${product.soldCount/1000.0}k+".replace(".0k+", "k+") else "${product.soldCount}+"}", fontSize = 10.sp, color = Color.Gray, maxLines = 1, overflow = TextOverflow.Ellipsis)
          }
          Spacer(modifier = Modifier.width(4.dp))
          Box(
            modifier = Modifier
              .size(28.dp)
              .clip(RoundedCornerShape(8.dp))
              .background(Color(0xFF4CAF50))
              .clickable { },
            contentAlignment = Alignment.Center
          ) {
            Icon(Icons.Outlined.ShoppingCart, contentDescription = "Add to Cart", tint = Color.White, modifier = Modifier.size(16.dp))
          }
        }
      }
      
      // Top Left Corner - Discount Badge
      if (product.discount != null) {
        Box(
          modifier = Modifier
            .align(Alignment.TopStart)
            .clip(RoundedCornerShape(topStart = 8.dp, bottomEnd = 8.dp))
            .background(Color(0xFF4CAF50))
            .padding(horizontal = 6.dp, vertical = 2.dp)
        ) {
          Text("-${product.discount}%", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold)
        }
      }
      
      // Top Right Corner - Favorite Icon
      Icon(
        Icons.Outlined.FavoriteBorder,
        contentDescription = "Favorite",
        tint = Color.Gray,
        modifier = Modifier
            .align(Alignment.TopEnd)
            .padding(8.dp)
            .size(20.dp)
            .clickable { }
      )
    }
  }
}

@Composable
fun CircleDealCard"""

content = re.sub(product_card_old, product_card_new, content)

# 2. Update CircleDealCard
circle_deal_card_old = r"""@Composable
fun CircleDealCard\(product: Product, modifier: Modifier = Modifier\) \{[\s\S]*?fun CategoryItem"""

circle_deal_card_new = """@Composable
fun CircleDealCard(product: Product, modifier: Modifier = Modifier) {
  Card(
    modifier = modifier.clickable { },
    colors = CardDefaults.cardColors(containerColor = Color.White),
    elevation = CardDefaults.cardElevation(defaultElevation = 0.dp),
    shape = RoundedCornerShape(8.dp),
    border = BorderStroke(1.dp, Color(0xFF4CAF50))
  ) {
    Box {
      Column(modifier = Modifier.padding(8.dp)) {
        Box(modifier = Modifier.fillMaxWidth().aspectRatio(1f).padding(top = 10.dp)) {
          AsyncImage(
            model = product.imageUrl,
            contentDescription = product.title,
            contentScale = ContentScale.Fit,
            modifier = Modifier.fillMaxSize()
          )
        }
        Spacer(modifier = Modifier.height(6.dp))
        Text(
          product.title,
          style = MaterialTheme.typography.bodyMedium,
          fontWeight = FontWeight.Medium,
          maxLines = 1,
          overflow = TextOverflow.Ellipsis,
          color = Color.Black
        )
        Spacer(modifier = Modifier.height(2.dp))
        
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
        Spacer(modifier = Modifier.height(4.dp))
        
        // Stock Progress Bar (Green)
        val progress = product.stock.toFloat() / product.maxStock.toFloat()
        
        Column(modifier = Modifier.fillMaxWidth()) {
           Box(modifier = Modifier.fillMaxWidth().height(4.dp).clip(RoundedCornerShape(2.dp)).background(Color(0xFFE0E0E0))) {
              Box(modifier = Modifier.fillMaxWidth(progress).height(4.dp).clip(RoundedCornerShape(2.dp)).background(Color(0xFF4CAF50)))
           }
           Spacer(modifier = Modifier.height(2.dp))
           Text("Only ${product.stock} Left", fontSize = 11.sp, color = Color(0xFF4CAF50), fontWeight = FontWeight.Bold)
        }
      }
      
      // Top Left Corner - Discount Badge
      if (product.discount != null) {
        Box(
          modifier = Modifier
            .align(Alignment.TopStart)
            .clip(RoundedCornerShape(topStart = 8.dp, bottomEnd = 8.dp))
            .background(Color(0xFF4CAF50))
            .padding(horizontal = 6.dp, vertical = 2.dp)
        ) {
          Text("-${product.discount}%", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold)
        }
      }
      
      // Top Right Corner - Favorite Icon
      Icon(
        Icons.Outlined.FavoriteBorder,
        contentDescription = "Favorite",
        tint = Color.Gray,
        modifier = Modifier
            .align(Alignment.TopEnd)
            .padding(8.dp)
            .size(20.dp)
            .clickable { }
      )
    }
  }
}

@Composable
fun CategoryItem"""

content = re.sub(circle_deal_card_old, circle_deal_card_new, content)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
