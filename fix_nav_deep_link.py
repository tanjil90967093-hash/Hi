import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

navhost_old = """      composable(Screen.CircleDeals.route) { CircleDealsScreen(onBack = { navController.popBackStack() }) }"""
navhost_new = """      composable(
        Screen.CircleDeals.route,
        deepLinks = listOf(androidx.navigation.navDeepLink { uriPattern = "https://circlebazar.com/deals" })
      ) { CircleDealsScreen(onBack = { navController.popBackStack() }) }"""

content = content.replace(navhost_old, navhost_new)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
