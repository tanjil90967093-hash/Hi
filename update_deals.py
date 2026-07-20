import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Update Screen sealed class
old_screen_block = """sealed class Screen(val route: String, val title: String, val unselectedIcon: androidx.compose.ui.graphics.vector.ImageVector, val selectedIcon: androidx.compose.ui.graphics.vector.ImageVector) {
  object Home : Screen("home", "Home", Icons.Outlined.Home, Icons.Filled.Home)
  object Category : Screen("category", "Category", Icons.Outlined.GridView, Icons.Filled.GridView)
  object Cart : Screen("cart", "Cart", Icons.Outlined.ShoppingCart, Icons.Filled.ShoppingCart)
  object Orders : Screen("orders", "Orders", Icons.Outlined.ListAlt, Icons.Filled.ListAlt)
  object Profile : Screen("profile", "Profile", Icons.Outlined.Person, Icons.Filled.Person)
  object Search : Screen("search", "Search", Icons.Outlined.Search, Icons.Filled.Search)
  object CameraSearch : Screen("camera", "Camera", Icons.Outlined.CameraAlt, Icons.Filled.CameraAlt)
}"""

new_screen_block = """sealed class Screen(val route: String, val title: String, val unselectedIcon: androidx.compose.ui.graphics.vector.ImageVector, val selectedIcon: androidx.compose.ui.graphics.vector.ImageVector) {
  object Home : Screen("home", "Home", Icons.Outlined.Home, Icons.Filled.Home)
  object Category : Screen("category", "Category", Icons.Outlined.GridView, Icons.Filled.GridView)
  object Cart : Screen("cart", "Cart", Icons.Outlined.ShoppingCart, Icons.Filled.ShoppingCart)
  object Orders : Screen("orders", "Orders", Icons.Outlined.ListAlt, Icons.Filled.ListAlt)
  object Profile : Screen("profile", "Profile", Icons.Outlined.Person, Icons.Filled.Person)
  object Search : Screen("search", "Search", Icons.Outlined.Search, Icons.Filled.Search)
  object CameraSearch : Screen("camera", "Camera", Icons.Outlined.CameraAlt, Icons.Filled.CameraAlt)
  object CircleDeals : Screen("circle_deals", "Circle Deals", Icons.Outlined.LocalOffer, Icons.Filled.LocalOffer)
}"""
content = content.replace(old_screen_block, new_screen_block)

# 2. Update NavHost
old_nav_host_block = """      composable(Screen.CameraSearch.route) { CameraSearchScreen(onBack = { navController.popBackStack() }) }
    }"""
new_nav_host_block = """      composable(Screen.CameraSearch.route) { CameraSearchScreen(onBack = { navController.popBackStack() }) }
      composable(Screen.CircleDeals.route) { FullCircleDealsScreen(onBack = { navController.popBackStack() }) }
    }"""
content = content.replace(old_nav_host_block, new_nav_host_block)

# 3. Update HomeScreen signature
old_home_sig = "fun HomeScreen(onSearchClick: () -> Unit = {}, onCameraClick: () -> Unit = {}) {"
new_home_sig = "fun HomeScreen(onSearchClick: () -> Unit = {}, onCameraClick: () -> Unit = {}, onCircleDealsClick: () -> Unit = {}) {"
content = content.replace(old_home_sig, new_home_sig)
content = content.replace("composable(Screen.Home.route) { HomeScreen(", "composable(Screen.Home.route) { HomeScreen(onCircleDealsClick = { navController.navigate(Screen.CircleDeals.route) }, ")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
