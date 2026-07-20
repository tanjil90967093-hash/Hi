import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Replace Screen sealed class
old_screen = """sealed class Screen(val route: String, val title: String, val unselectedIcon: androidx.compose.ui.graphics.vector.ImageVector, val selectedIcon: androidx.compose.ui.graphics.vector.ImageVector) {
  object Home : Screen("home", "Home", Icons.Outlined.Home, Icons.Filled.Home)
  object Category : Screen("category", "Category", Icons.Outlined.GridView, Icons.Filled.GridView)
  object Cart : Screen("cart", "Cart", Icons.Outlined.ShoppingCart, Icons.Filled.ShoppingCart)
  object Orders : Screen("orders", "Orders", Icons.Outlined.ListAlt, Icons.Filled.ListAlt)
  object Profile : Screen("profile", "Profile", Icons.Outlined.Person, Icons.Filled.Person)
}"""

new_screen = """sealed class Screen(val route: String, val title: String, val unselectedIcon: androidx.compose.ui.graphics.vector.ImageVector, val selectedIcon: androidx.compose.ui.graphics.vector.ImageVector) {
  object Home : Screen("home", "Home", Icons.Outlined.Home, Icons.Filled.Home)
  object Category : Screen("category", "Category", Icons.Outlined.GridView, Icons.Filled.GridView)
  object Cart : Screen("cart", "Cart", Icons.Outlined.ShoppingCart, Icons.Filled.ShoppingCart)
  object Orders : Screen("orders", "Orders", Icons.Outlined.ListAlt, Icons.Filled.ListAlt)
  object Profile : Screen("profile", "Profile", Icons.Outlined.Person, Icons.Filled.Person)
  object Search : Screen("search", "Search", Icons.Outlined.Search, Icons.Filled.Search)
  object CameraSearch : Screen("camera", "Camera", Icons.Outlined.CameraAlt, Icons.Filled.CameraAlt)
}"""

content = content.replace(old_screen, new_screen)

# Replace NavHost to add new screens
old_nav_host = """    NavHost(
      navController = navController,
      startDestination = Screen.Home.route,
      modifier = Modifier.padding(bottom = innerPadding.calculateBottomPadding())
    ) {
      composable(Screen.Home.route) { HomeScreen() }
      composable(Screen.Category.route) { CategoryScreen() }
      composable(Screen.Cart.route) { CartScreen() }
      composable(Screen.Orders.route) { OrdersScreen() }
      composable(Screen.Profile.route) { ProfileScreen() }
    }"""

new_nav_host = """    NavHost(
      navController = navController,
      startDestination = Screen.Home.route,
      modifier = Modifier.padding(bottom = innerPadding.calculateBottomPadding())
    ) {
      composable(Screen.Home.route) { HomeScreen(
        onSearchClick = { navController.navigate(Screen.Search.route) },
        onCameraClick = { navController.navigate(Screen.CameraSearch.route) }
      ) }
      composable(Screen.Category.route) { CategoryScreen() }
      composable(Screen.Cart.route) { CartScreen() }
      composable(Screen.Orders.route) { OrdersScreen() }
      composable(Screen.Profile.route) { ProfileScreen() }
      composable(Screen.Search.route) { SearchScreen(onBack = { navController.popBackStack() }) }
      composable(Screen.CameraSearch.route) { CameraSearchScreen(onBack = { navController.popBackStack() }) }
    }"""
content = content.replace(old_nav_host, new_nav_host)

# Update HomeScreen signature
old_home_sig = "fun HomeScreen() {"
new_home_sig = "fun HomeScreen(onSearchClick: () -> Unit = {}, onCameraClick: () -> Unit = {}) {"
content = content.replace(old_home_sig, new_home_sig)

# Update clicks
content = content.replace('Icon(Icons.Outlined.Search, contentDescription = "Search", tint = Color.White, modifier = Modifier.clickable { /* TODO */ })', 'Icon(Icons.Outlined.Search, contentDescription = "Search", tint = Color.White, modifier = Modifier.clickable { onSearchClick() })')
content = content.replace('Box(modifier = Modifier.clickable { /* TODO: Open Search Screen */ })', 'Box(modifier = Modifier.clickable { onSearchClick() })')
content = content.replace('Icon(Icons.Outlined.CameraAlt, contentDescription = "Image Search", tint = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(end = 12.dp, start = 4.dp).clickable { /* TODO */ })', 'Icon(Icons.Outlined.CameraAlt, contentDescription = "Image Search", tint = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(end = 12.dp, start = 4.dp).clickable { onCameraClick() })')
content = content.replace('Box(modifier = Modifier.matchParentSize().clickable { /* TODO */ })', 'Box(modifier = Modifier.matchParentSize().clickable { onSearchClick() })')


# Now append the new composables and CircleDealCard at the end
new_components = """

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SearchScreen(onBack: () -> Unit) {
  var query by remember { mutableStateOf("") }
  Column(modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)) {
    TopAppBar(
      title = { 
        TextField(
          value = query,
          onValueChange = { query = it },
          placeholder = { Text("Search products...") },
          colors = TextFieldDefaults.colors(
             unfocusedContainerColor = Color.Transparent,
             focusedContainerColor = Color.Transparent,
             unfocusedIndicatorColor = Color.Transparent,
             focusedIndicatorColor = Color.Transparent
          ),
          modifier = Modifier.fillMaxWidth()
        )
      },
      navigationIcon = {
        IconButton(onClick = onBack) { Icon(Icons.Outlined.ArrowBack, contentDescription = "Back") }
      },
      actions = {
        IconButton(onClick = { /* Voice Search */ }) { Icon(Icons.Outlined.Mic, contentDescription = "Voice") }
      },
      colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.surface)
    )
    
    // Voice Search Hint
    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
       Column(horizontalAlignment = Alignment.CenterHorizontally) {
           Icon(Icons.Outlined.Mic, contentDescription = null, modifier = Modifier.size(64.dp), tint = Color.LightGray)
           Spacer(modifier = Modifier.height(16.dp))
           Text("Try saying \"Smart Watches\"", color = Color.Gray)
       }
    }
  }
}

@Composable
fun CameraSearchScreen(onBack: () -> Unit) {
  Box(modifier = Modifier.fillMaxSize().background(Color.Black)) {
    // Fake Camera Viewfinder
    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
       Box(modifier = Modifier.size(250.dp).border(2.dp, Color.White.copy(alpha=0.5f), RoundedCornerShape(16.dp)))
    }
    
    // Top Bar
    Row(modifier = Modifier.fillMaxWidth().statusBarsPadding().padding(16.dp), horizontalArrangement = Arrangement.SpaceBetween) {
      IconButton(onClick = onBack) { Icon(Icons.Outlined.Close, contentDescription = "Close", tint = Color.White) }
      IconButton(onClick = { }) { Icon(Icons.Outlined.MoreVert, contentDescription = "More", tint = Color.White) }
    }
    
    // Bottom Gallery Strip
    Column(modifier = Modifier.align(Alignment.BottomCenter).fillMaxWidth().padding(bottom = 32.dp)) {
      Text("Search with an image", color = Color.White, modifier = Modifier.align(Alignment.CenterHorizontally).padding(bottom = 16.dp))
      LazyRow(contentPadding = PaddingValues(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        items(5) {
          Box(modifier = Modifier.size(64.dp).clip(RoundedCornerShape(8.dp)).background(Color.DarkGray))
        }
      }
      Spacer(modifier = Modifier.height(32.dp))
      // Capture Button
      Box(modifier = Modifier.size(72.dp).clip(CircleShape).border(4.dp, Color.White, CircleShape).align(Alignment.CenterHorizontally).clickable{ /* Capture */ }) {
         Box(modifier = Modifier.size(56.dp).clip(CircleShape).background(Color.White).align(Alignment.Center))
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
      Box(modifier = Modifier.fillMaxWidth().height(120.dp)) {
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
      Row(verticalAlignment = Alignment.Bottom) {
        Text(
          "৳ ${product.price.toInt()}",
          style = MaterialTheme.typography.titleSmall,
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

with open("app/src/main/java/com/example/MainActivity.kt", "a") as f:
    f.write(new_components)

