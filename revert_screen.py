import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

old_screen = """sealed class Screen(val route: String, val title: String, val icon: androidx.compose.ui.graphics.vector.ImageVector, val selectedIcon: androidx.compose.ui.graphics.vector.ImageVector) {
  object Home : Screen("home", "Home", Icons.Outlined.Home, Icons.Filled.Home)
  object Category : Screen("category", "Category", Icons.Outlined.Search, Icons.Filled.Search) // Using Search for category exploration
  object Cart : Screen("cart", "Cart", Icons.Outlined.ShoppingCart, Icons.Filled.ShoppingCart)
  object Orders : Screen("orders", "Orders", Icons.Outlined.List, Icons.Filled.List)
  object Profile : Screen("profile", "Profile", Icons.Outlined.Person, Icons.Filled.Person)
  object Search : Screen("search", "Search", Icons.Outlined.Search, Icons.Filled.Search)
  object CameraSearch : Screen("camera", "Camera", Icons.Outlined.CameraAlt, Icons.Filled.CameraAlt)
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
