import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Add CircleDeals route
content = content.replace(
    '  object CameraSearch : Screen("camera", "Camera", Icons.Outlined.CameraAlt, Icons.Filled.CameraAlt)\n}',
    '  object CameraSearch : Screen("camera", "Camera", Icons.Outlined.CameraAlt, Icons.Filled.CameraAlt)\n  object CircleDeals : Screen("circle_deals", "Circle Deals", Icons.Outlined.LocalOffer, Icons.Filled.LocalOffer)\n}'
)

# Update NavHost
navhost_old = """      composable(Screen.Search.route) { SearchScreen(onBack = { navController.popBackStack() }) }
      composable(Screen.CameraSearch.route) { CameraSearchScreen(onBack = { navController.popBackStack() }) }
    }
  }"""
navhost_new = """      composable(Screen.Search.route) { SearchScreen(onBack = { navController.popBackStack() }) }
      composable(Screen.CameraSearch.route) { CameraSearchScreen(onBack = { navController.popBackStack() }) }
      composable(Screen.CircleDeals.route) { CircleDealsScreen(onBack = { navController.popBackStack() }) }
    }
  }"""
content = content.replace(navhost_old, navhost_new)

# Update HomeScreen signature
content = content.replace(
    "fun HomeScreen(onSearchClick: () -> Unit = {}, onCameraClick: () -> Unit = {}) {",
    "fun HomeScreen(onSearchClick: () -> Unit = {}, onCameraClick: () -> Unit = {}, onCircleDealsClick: () -> Unit = {}) {"
)
# Update composable(Screen.Home.route)
content = content.replace(
    "composable(Screen.Home.route) { HomeScreen(onSearchClick = { navController.navigate(Screen.Search.route) }, onCameraClick = { navController.navigate(Screen.CameraSearch.route) }) }",
    "composable(Screen.Home.route) { HomeScreen(onSearchClick = { navController.navigate(Screen.Search.route) }, onCameraClick = { navController.navigate(Screen.CameraSearch.route) }, onCircleDealsClick = { navController.navigate(Screen.CircleDeals.route) }) }"
)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
