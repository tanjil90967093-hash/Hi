with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

old_nav = """      composable(Screen.Profile.route) { ProfileScreen() }
    }"""
new_nav = """      composable(Screen.Profile.route) { ProfileScreen() }
      composable(Screen.Search.route) { SearchScreen(onBack = { navController.popBackStack() }) }
      composable(Screen.CameraSearch.route) { CameraSearchScreen(onBack = { navController.popBackStack() }) }
      composable(Screen.CircleDeals.route) { FullCircleDealsScreen(onBack = { navController.popBackStack() }) }
    }"""

content = content.replace(old_nav, new_nav)
with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
