import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Update CircleDealCard to match the requested design exactly
circle_deal_card = """@Composable
fun CircleDealCard(product: Product, modifier: Modifier = Modifier) {
  Card(
    modifier = modifier.clickable { },
    colors = CardDefaults.cardColors(containerColor = Color.White),
    elevation = CardDefaults.cardElevation(defaultElevation = 0.dp),
    shape = RoundedCornerShape(8.dp),
    border = BorderStroke(1.dp, Color(0xFF4CAF50))
  ) {
    Column(modifier = Modifier.padding(8.dp)) {
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
              .padding(horizontal = 6.dp, vertical = 2.dp)
          ) {
            Text("-${product.discount}%", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold)
          }
        }
      }
      Spacer(modifier = Modifier.height(8.dp))
      Text(
        product.title,
        style = MaterialTheme.typography.bodyMedium,
        fontWeight = FontWeight.Medium,
        maxLines = 1,
        overflow = TextOverflow.Ellipsis,
        color = Color.Black
      )
      Spacer(modifier = Modifier.height(4.dp))
      
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
      
      // Stock Progress Bar (Green)
      val progress = product.stock.toFloat() / product.maxStock.toFloat()
      
      Column(modifier = Modifier.fillMaxWidth()) {
         Box(modifier = Modifier.fillMaxWidth().height(6.dp).clip(RoundedCornerShape(3.dp)).background(Color(0xFFEEEEEE))) {
            Box(modifier = Modifier.fillMaxWidth(progress).height(6.dp).clip(RoundedCornerShape(3.dp)).background(Color(0xFF4CAF50)))
         }
         Spacer(modifier = Modifier.height(4.dp))
         Text("Only ${product.stock} Left", fontSize = 10.sp, color = Color.Gray, fontWeight = FontWeight.Medium)
      }
    }
  }
}"""

content = re.sub(
    r'@Composable\nfun CircleDealCard\(product: Product, modifier: Modifier = Modifier\) \{[\s\S]*?\n\}\n\n@Composable\nfun CategoryItem',
    circle_deal_card + '\n\n@Composable\nfun CategoryItem',
    content
)

# Update LazyHorizontalGrid height and item width
content = re.sub(
    r'modifier = Modifier\.fillMaxWidth\(\)\.height\([0-9]+.dp\)',
    'modifier = Modifier.fillMaxWidth().height(480.dp)',
    content
)

content = re.sub(
    r'CircleDealCard\(circleDealsList\[index\], modifier = Modifier\.width\([0-9]+.dp\)\)',
    'CircleDealCard(circleDealsList[index], modifier = Modifier.width(140.dp))',
    content
)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

