import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

main_screen_old = """fun MainScreen() {
  val navController = rememberNavController()
  val items = listOf(
    Screen.Home,
    Screen.Category,
    Screen.Cart,
    Screen.Orders,
    Screen.Profile
  )

  Scaffold("""

main_screen_new = """fun MainScreen() {
  val navController = rememberNavController()
  val items = listOf(
    Screen.Home,
    Screen.Category,
    Screen.Cart,
    Screen.Orders,
    Screen.Profile
  )

  val bottomBarHeight = 80.dp
  val bottomBarHeightPx = with(androidx.compose.ui.platform.LocalDensity.current) { bottomBarHeight.roundToPx().toFloat() }
  val bottomBarOffsetHeightPx = remember { androidx.compose.runtime.mutableFloatStateOf(0f) }

  val nestedScrollConnection = remember {
      object : androidx.compose.ui.input.nestedscroll.NestedScrollConnection {
          override fun onPreScroll(available: androidx.compose.ui.geometry.Offset, source: androidx.compose.ui.input.nestedscroll.NestedScrollSource): androidx.compose.ui.geometry.Offset {
              val delta = available.y
              val newOffset = bottomBarOffsetHeightPx.floatValue - delta
              bottomBarOffsetHeightPx.floatValue = newOffset.coerceIn(0f, bottomBarHeightPx)
              return androidx.compose.ui.geometry.Offset.Zero
          }
      }
  }

  Scaffold(
    modifier = Modifier.nestedScroll(nestedScrollConnection),"""

content = content.replace(main_screen_old, main_screen_new)

nav_bar_old = """    bottomBar = {
      NavigationBar(
        containerColor = MaterialTheme.colorScheme.surface,
        tonalElevation = 8.dp
      ) {"""

nav_bar_new = """    bottomBar = {
      NavigationBar(
        modifier = Modifier.offset { androidx.compose.ui.unit.IntOffset(x = 0, y = bottomBarOffsetHeightPx.floatValue.toInt()) },
        containerColor = MaterialTheme.colorScheme.surface,
        tonalElevation = 8.dp
      ) {"""

content = content.replace(nav_bar_old, nav_bar_new)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

