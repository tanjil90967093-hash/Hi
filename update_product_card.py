import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Modify ProductCard signature
content = content.replace("fun ProductCard(product: Product, modifier: Modifier = Modifier) {", "fun ProductCard(product: Product, modifier: Modifier = Modifier, isCircleDeal: Boolean = false) {")

# Find the bottom Row in ProductCard
bottom_row_old = """      Spacer(modifier = Modifier.height(8.dp))
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
        Box("""
        
bottom_row_new = """      Spacer(modifier = Modifier.height(8.dp))
      if (isCircleDeal) {
        val sold = product.maxStock - product.stock
        val progress = sold.toFloat() / product.maxStock.toFloat()
        Column(modifier = Modifier.fillMaxWidth()) {
          Box(modifier = Modifier.fillMaxWidth().height(4.dp).clip(RoundedCornerShape(2.dp)).background(Color.LightGray)) {
            Box(modifier = Modifier.fillMaxWidth(progress).height(4.dp).clip(RoundedCornerShape(2.dp)).background(MaterialTheme.colorScheme.primary))
          }
          Spacer(modifier = Modifier.height(4.dp))
          Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
            Text("${sold} Sold • ${product.stock} Left", fontSize = 10.sp, color = Color.Gray)
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
      } else {
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
          Box("""

content = content.replace(bottom_row_old, bottom_row_new)

# Find the end of the Else block (which is the end of the Box for Cart button)
cart_box_end = """          contentAlignment = Alignment.Center
        ) {
          Icon(Icons.Outlined.ShoppingCart, contentDescription = "Add to Cart", tint = Color.White, modifier = Modifier.size(16.dp))
        }
      }
    }
  }
}"""
cart_box_end_new = """          contentAlignment = Alignment.Center
        ) {
          Icon(Icons.Outlined.ShoppingCart, contentDescription = "Add to Cart", tint = Color.White, modifier = Modifier.size(16.dp))
        }
      }
      }
    }
  }
}"""

content = content.replace(cart_box_end, cart_box_end_new)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
