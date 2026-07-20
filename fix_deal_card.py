import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

start = content.find("fun CircleDealCard(product: Product, modifier: Modifier = Modifier) {")
end = content.find("}", content.find("}", content.find("}", content.find("}", content.find("}", content.find("}", start) + 1) + 1) + 1) + 1) + 1) + 1

new_card = """fun CircleDealCard(product: Product, modifier: Modifier = Modifier) {
  Card(
    modifier = modifier.width(160.dp).clickable { },
    colors = CardDefaults.cardColors(containerColor = Color.White),
    elevation = CardDefaults.cardElevation(defaultElevation = 0.dp),
    border = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.primary),
    shape = RoundedCornerShape(12.dp)
  ) {
    Column(modifier = Modifier.padding(12.dp)) {
      Box(modifier = Modifier.fillMaxWidth().height(140.dp)) {
        AsyncImage(
          model = product.imageUrl,
          contentDescription = product.title,
          contentScale = ContentScale.Fit,
          modifier = Modifier.fillMaxSize().padding(12.dp)
        )
        if (product.discount != null) {
          Box(
            modifier = Modifier
              .align(Alignment.TopStart)
              .clip(RoundedCornerShape(4.dp))
              .background(MaterialTheme.colorScheme.primary)
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
        style = MaterialTheme.typography.bodyMedium,
        fontWeight = FontWeight.Medium,
        maxLines = 2,
        overflow = TextOverflow.Ellipsis,
        color = Color.Black
      )
      Spacer(modifier = Modifier.height(4.dp))
      Row(verticalAlignment = Alignment.Bottom) {
        Text(
          "৳ ${product.price.toInt()}",
          style = MaterialTheme.typography.titleMedium,
          fontWeight = FontWeight.Bold,
          color = MaterialTheme.colorScheme.primary
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
      
      // Stock Progress Bar
      val sold = product.maxStock - product.stock
      val progress = sold.toFloat() / product.maxStock.toFloat()
      Column(modifier = Modifier.fillMaxWidth()) {
         Box(modifier = Modifier.fillMaxWidth().height(4.dp).clip(RoundedCornerShape(2.dp)).background(Color.LightGray)) {
            Box(modifier = Modifier.fillMaxWidth(progress).height(4.dp).clip(RoundedCornerShape(2.dp)).background(MaterialTheme.colorScheme.primary))
         }
         Spacer(modifier = Modifier.height(4.dp))
         Text("${sold} Sold • ${product.stock} Left", fontSize = 10.sp, color = Color.Gray)
      }
    }
  }
}"""

if start != -1 and end != -1:
    content = content[:start] + new_card + content[end:]
    with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
        f.write(content)
    print("Updated Deal Card")
else:
    print("Could not find start or end")

