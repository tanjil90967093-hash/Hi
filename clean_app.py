with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Remove FullCircleDealsScreen
start = content.find("@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun FullCircleDealsScreen")
if start != -1:
    content = content[:start]

# 2. Fix NavHost
old_nav = """      composable(Screen.Profile.route) { ProfileScreen() }
      composable(Screen.Search.route) { SearchScreen(onBack = { navController.popBackStack() }) }
      composable(Screen.CameraSearch.route) { CameraSearchScreen(onBack = { navController.popBackStack() }) }
      composable(Screen.CircleDeals.route) { FullCircleDealsScreen(onBack = { navController.popBackStack() }) }
    }"""
new_nav = """      composable(Screen.Profile.route) { ProfileScreen() }
      composable(Screen.Search.route) { SearchScreen(onBack = { navController.popBackStack() }) }
      composable(Screen.CameraSearch.route) { CameraSearchScreen(onBack = { navController.popBackStack() }) }
    }"""
content = content.replace(old_nav, new_nav)

# 3. Fix HomeScreen signature
old_sig = "fun HomeScreen(onSearchClick: () -> Unit = {}, onCameraClick: () -> Unit = {}, onCircleDealsClick: () -> Unit = {}) {"
new_sig = "fun HomeScreen(onSearchClick: () -> Unit = {}, onCameraClick: () -> Unit = {}) {"
content = content.replace(old_sig, new_sig)

# 4. Fix NavHost composable
old_comp = "composable(Screen.Home.route) { HomeScreen(onSearchClick = { navController.navigate(Screen.Search.route) }, onCameraClick = { navController.navigate(Screen.CameraSearch.route) }, onCircleDealsClick = { navController.navigate(Screen.CircleDeals.route) }) }"
new_comp = "composable(Screen.Home.route) { HomeScreen(onSearchClick = { navController.navigate(Screen.Search.route) }, onCameraClick = { navController.navigate(Screen.CameraSearch.route) }) }"
content = content.replace(old_comp, new_comp)

# 5. Fix Screen sealed class
old_screen = """sealed class Screen(val route: String, val title: String, val icon: androidx.compose.ui.graphics.vector.ImageVector, val selectedIcon: androidx.compose.ui.graphics.vector.ImageVector) {
  object Home : Screen("home", "Home", Icons.Outlined.Home, Icons.Filled.Home)
  object Category : Screen("category", "Category", Icons.Outlined.Search, Icons.Filled.Search)
  object Cart : Screen("cart", "Cart", Icons.Outlined.ShoppingCart, Icons.Filled.ShoppingCart)
  object Orders : Screen("orders", "Orders", Icons.Outlined.List, Icons.Filled.List)
  object Profile : Screen("profile", "Profile", Icons.Outlined.Person, Icons.Filled.Person)
  object Search : Screen("search", "Search", Icons.Outlined.Search, Icons.Filled.Search)
  object CameraSearch : Screen("camera", "Camera", Icons.Outlined.CameraAlt, Icons.Filled.CameraAlt)
  object CircleDeals : Screen("circle_deals", "Circle Deals", Icons.Outlined.LocalOffer, Icons.Filled.LocalOffer)
}"""

new_screen = """sealed class Screen(val route: String, val title: String, val icon: androidx.compose.ui.graphics.vector.ImageVector, val selectedIcon: androidx.compose.ui.graphics.vector.ImageVector) {
  object Home : Screen("home", "Home", Icons.Outlined.Home, Icons.Filled.Home)
  object Category : Screen("category", "Category", Icons.Outlined.Search, Icons.Filled.Search) // Using Search for category exploration
  object Cart : Screen("cart", "Cart", Icons.Outlined.ShoppingCart, Icons.Filled.ShoppingCart)
  object Orders : Screen("orders", "Orders", Icons.Outlined.List, Icons.Filled.List)
  object Profile : Screen("profile", "Profile", Icons.Outlined.Person, Icons.Filled.Person)
  object Search : Screen("search", "Search", Icons.Outlined.Search, Icons.Filled.Search)
  object CameraSearch : Screen("camera", "Camera", Icons.Outlined.CameraAlt, Icons.Filled.CameraAlt)
}"""
content = content.replace(old_screen, new_screen)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
