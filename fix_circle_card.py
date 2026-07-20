import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

old_circle_card = r"""fun CircleDealCard\(product: Product, modifier: Modifier = Modifier\) \{[\s\S]*?fun CategoryItem"""

new_circle_card = """fun CircleDealCard(product: Product, modifier: Modifier = Modifier) {
  Card(
    modifier = modifier.clickable { },
    colors = CardDefaults.cardColors(containerColor = Color.White),
    elevation = CardDefaults.cardElevation(defaultElevation = 0.dp),
    shape = RoundedCornerShape(8.dp),
    border = BorderStroke(1.dp, Color(0xFF4CAF50))
  ) {
    Box {
      Column(modifier = Modifier.padding(6.dp)) { // Reduced padding from 8dp to 6dp
        Box(modifier = Modifier.fillMaxWidth().aspectRatio(1f).padding(top = 4.dp)) { // Reduced top padding
          AsyncImage(
            model = product.imageUrl,
            contentDescription = product.title,
            contentScale = ContentScale.Fit,
            modifier = Modifier.fillMaxSize()
          )
        }
        Spacer(modifier = Modifier.height(4.dp))
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
        Spacer(modifier = Modifier.height(6.dp))
        
        // Stock Progress Bar (Green)
        val progress = product.stock.toFloat() / product.maxStock.toFloat()
        
        Column(modifier = Modifier.fillMaxWidth()) {
           Box(modifier = Modifier.fillMaxWidth().height(6.dp).clip(RoundedCornerShape(3.dp)).background(Color(0xFFE0E0E0))) { // Made thicker
              Box(modifier = Modifier.fillMaxWidth(progress).height(6.dp).clip(RoundedCornerShape(3.dp)).background(Color(0xFF4CAF50))) // Made thicker
           }
           Spacer(modifier = Modifier.height(4.dp))
           Text("Only ${product.stock} Left", fontSize = 13.sp, color = Color(0xFF4CAF50), fontWeight = FontWeight.Bold) // Made larger
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

content = re.sub(old_circle_card, new_circle_card, content)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

