import re

with open("app/src/main/java/com/example/MainActivity.kt", "a") as f:
    f.write("""

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun FullCircleDealsScreen(onBack: () -> Unit) {
  val listState = androidx.compose.foundation.lazy.rememberLazyListState()
  
  Column(modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)) {
    TopAppBar(
      title = { Text("Circle Deals", fontWeight = FontWeight.Bold) },
      navigationIcon = {
        IconButton(onClick = onBack) { Icon(Icons.Outlined.ArrowBack, contentDescription = "Back") }
      },
      actions = {
        IconButton(onClick = { /* Search */ }) { Icon(Icons.Outlined.Search, contentDescription = "Search") }
      },
      colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.surface)
    )
    
    LazyColumn(state = listState, modifier = Modifier.fillMaxSize()) {
       item {
         // Premium Banner
         AsyncImage(
            model = "https://images.unsplash.com/photo-1607082349566-187342175e2f?w=800&q=80",
            contentDescription = "Flash Sale Banner",
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxWidth().height(140.dp)
         )
       }
       
       item {
         // Countdown and Filters
         Column(modifier = Modifier.fillMaxWidth().background(Color.White).padding(16.dp)) {
           Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
               Text("Ending in", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
               Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                   Box(modifier = Modifier.clip(RoundedCornerShape(4.dp)).background(Color(0xFFE53935)).padding(horizontal = 6.dp, vertical = 4.dp)) {
                       Text("02", color = Color.White, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                   }
                   Text(":", color = Color(0xFFE53935), fontSize = 16.sp, fontWeight = FontWeight.Bold)
                   Box(modifier = Modifier.clip(RoundedCornerShape(4.dp)).background(Color(0xFFE53935)).padding(horizontal = 6.dp, vertical = 4.dp)) {
                       Text("45", color = Color.White, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                   }
                   Text(":", color = Color(0xFFE53935), fontSize = 16.sp, fontWeight = FontWeight.Bold)
                   Box(modifier = Modifier.clip(RoundedCornerShape(4.dp)).background(Color(0xFFE53935)).padding(horizontal = 6.dp, vertical = 4.dp)) {
                       Text("12", color = Color.White, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                   }
               }
           }
           Spacer(modifier = Modifier.height(16.dp))
           LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
               val filters = listOf("All", "Electronics", "Fashion", "Home", "Beauty")
               items(filters.size) { index ->
                   val isSelected = index == 0
                   Box(
                       modifier = Modifier
                         .clip(RoundedCornerShape(16.dp))
                         .background(if (isSelected) MaterialTheme.colorScheme.primary else Color.LightGray.copy(alpha = 0.3f))
                         .padding(horizontal = 16.dp, vertical = 8.dp)
                         .clickable { }
                   ) {
                       Text(filters[index], color = if (isSelected) Color.White else Color.Black, fontSize = 12.sp, fontWeight = if (isSelected) FontWeight.Medium else FontWeight.Normal)
                   }
               }
           }
         }
       }
       
       item { Spacer(modifier = Modifier.height(8.dp)) }
       
       // Product Grid
       val chunkedProducts = (mockProducts + mockProducts + mockProducts).chunked(2)
       items(chunkedProducts.size) { index ->
          val rowProducts = chunkedProducts[index]
          Row(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
          ) {
            for (product in rowProducts) {
               CircleDealCard(product, modifier = Modifier.weight(1f))
            }
            if (rowProducts.size == 1) {
               Spacer(modifier = Modifier.weight(1f))
            }
          }
       }
       
       item { Spacer(modifier = Modifier.height(32.dp)) }
    }
  }
}
""")
