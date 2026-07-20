import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# We need to replace HomeScreen entirely from `fun HomeScreen` to the `item { // Circle Deals }`
start = content.find("@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun HomeScreen(")
end_circle_deals = content.find("        // Circle Deals")

new_home_start = """@OptIn(ExperimentalMaterial3Api::class, androidx.compose.foundation.ExperimentalFoundationApi::class)
@Composable
fun HomeScreen(onSearchClick: () -> Unit = {}, onCameraClick: () -> Unit = {}) {
  val listState = rememberLazyListState()
  val showStickyHeader by remember {
     derivedStateOf { listState.firstVisibleItemIndex > 0 || listState.firstVisibleItemScrollOffset > 300 }
  }

  val banners = listOf(
      "https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?w=800&q=80",
      "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=800&q=80",
      "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=800&q=80"
  )
  val pagerState = androidx.compose.foundation.pager.rememberPagerState(pageCount = { banners.size })
  
  LaunchedEffect(Unit) {
      while (true) {
          kotlinx.coroutines.delay(3000)
          val nextPage = (pagerState.currentPage + 1) % banners.size
          pagerState.animateScrollToPage(nextPage)
      }
  }

  Box(modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)) {
    LazyColumn(state = listState, modifier = Modifier.fillMaxSize()) {
      item {
        // Banner that goes behind status bar
        Box(modifier = Modifier.fillMaxWidth().height(280.dp)) {
           // Auto-sliding Banner
           androidx.compose.foundation.pager.HorizontalPager(
               state = pagerState,
               modifier = Modifier.fillMaxSize()
           ) { page ->
               AsyncImage(
                  model = banners[page],
                  contentDescription = "Banner",
                  contentScale = ContentScale.Crop,
                  modifier = Modifier.fillMaxSize().clip(RoundedCornerShape(bottomStart = 24.dp, bottomEnd = 24.dp))
               )
           }
           
           // Gradient overlay for better status bar visibility
           Box(modifier = Modifier.fillMaxWidth().height(100.dp).background(androidx.compose.ui.graphics.Brush.verticalGradient(listOf(Color.Black.copy(alpha = 0.5f), Color.Transparent))))
           
           // Search Bar overlaying the banner at the bottom
           Box(
             modifier = Modifier
               .align(Alignment.BottomCenter)
               .fillMaxWidth()
               .padding(horizontal = 16.dp)
               .padding(bottom = 24.dp)
           ) {
              Box(modifier = Modifier.clickable { onSearchClick() }.shadow(8.dp, RoundedCornerShape(26.dp))) {
                TextField(
                  value = "",
                  onValueChange = {},
                  modifier = Modifier.fillMaxWidth().height(52.dp),
                  placeholder = { Text("Search products, brands and stores", color = Color.Gray, fontSize = 14.sp) },
                  leadingIcon = { Icon(Icons.Outlined.Search, contentDescription = null, tint = Color.Gray) },
                  trailingIcon = {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                      Icon(Icons.Outlined.Mic, contentDescription = "Voice Search", tint = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(horizontal = 4.dp))
                      Icon(Icons.Outlined.CameraAlt, contentDescription = "Image Search", tint = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(end = 12.dp, start = 4.dp).clickable { onCameraClick() })
                    }
                  },
                  shape = RoundedCornerShape(26.dp),
                  colors = TextFieldDefaults.colors(
                    unfocusedContainerColor = Color.White,
                    focusedContainerColor = Color.White,
                    unfocusedIndicatorColor = Color.Transparent,
                    focusedIndicatorColor = Color.Transparent
                  ),
                  singleLine = true,
                  readOnly = true,
                  enabled = false
                )
                // Overlay to handle clicks
                Box(modifier = Modifier.matchParentSize().clickable { onSearchClick() })
              }
           }
           
           // Pager Indicators
           Row(
             modifier = Modifier.align(Alignment.BottomCenter).padding(bottom = 8.dp),
             horizontalArrangement = Arrangement.spacedBy(6.dp)
           ) {
             repeat(banners.size) { iteration ->
               val color = if (pagerState.currentPage == iteration) MaterialTheme.colorScheme.primary else Color.White.copy(alpha = 0.6f)
               Box(
                 modifier = Modifier
                   .size(if (pagerState.currentPage == iteration) 10.dp else 8.dp)
                   .clip(CircleShape)
                   .background(color)
               )
             }
           }
        }
      }

      item {
"""

if start != -1 and end_circle_deals != -1:
    content = content[:start] + new_home_start + "        // Circle Deals" + content[end_circle_deals + len("        // Circle Deals"):]
    with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
        f.write(content)
    print("Replaced HomeScreen start with Pager banner")
else:
    print("Could not find start or end")

