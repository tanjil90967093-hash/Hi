import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# 1. Update mockProducts to have 20 items
mock_products_replacement = """val images = listOf(
  "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=500&q=80",
  "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500&q=80",
  "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&q=80",
  "https://images.unsplash.com/photo-1618365908648-713d016335a0?w=500&q=80",
  "https://images.unsplash.com/photo-1572569533349-f520ce4ce2f5?w=500&q=80"
)
val mockProducts = List(20) { index ->
  Product(
    id = index + 1,
    title = "Premium Product ${index + 1} with a very long title that spans multiple lines",
    imageUrl = images[index % images.size],
    price = 800.0 + (index * 150),
    oldPrice = 1200.0 + (index * 200),
    rating = 4.0 + (index % 10) * 0.1,
    soldCount = 500 + (index * 15),
    discount = 15 + (index % 5) * 5,
    stock = 20,
    maxStock = 100
  )
}"""

content = re.sub(r'val mockProducts = listOf\([\s\S]*?\n\)', mock_products_replacement, content)


# 2. HomeScreen modifications
# We need to replace the Banner clip, remove See All from inside the banner Box, and update the Search Bar.
# First, let's target the Banner Box inside HomeScreen.

def replace_search_bar(match):
    return """// Search Bar overlaying the banner at the top
           val context = androidx.compose.ui.platform.LocalContext.current
           val voiceIntent = remember { android.content.Intent(android.speech.RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply { putExtra(android.speech.RecognizerIntent.EXTRA_LANGUAGE_MODEL, android.speech.RecognizerIntent.LANGUAGE_MODEL_FREE_FORM) } }
           val pickIntent = remember { android.content.Intent(android.content.Intent.ACTION_PICK, android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI) }
           val takePhotoIntent = remember { android.content.Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE) }
           val chooserIntent = remember { android.content.Intent.createChooser(pickIntent, "Select Image").apply { putExtra(android.content.Intent.EXTRA_INITIAL_INTENTS, arrayOf(takePhotoIntent)) } }
           
           Box(
             modifier = Modifier
               .align(Alignment.TopCenter)
               .fillMaxWidth()
               .statusBarsPadding()
               .padding(start = 16.dp, end = 16.dp, top = 8.dp)
           ) {
              Row(
                  modifier = Modifier
                      .fillMaxWidth()
                      .height(46.dp)
                      .shadow(8.dp, RoundedCornerShape(23.dp))
                      .background(Color.White, RoundedCornerShape(23.dp))
                      .clickable { onSearchClick() }
                      .padding(horizontal = 16.dp),
                  verticalAlignment = Alignment.CenterVertically
              ) {
                  Icon(Icons.Outlined.Search, contentDescription = "Search", tint = Color.Gray)
                  Spacer(Modifier.width(8.dp))
                  Text("Search products, brands and stores", color = Color.Gray, fontSize = 14.sp, modifier = Modifier.weight(1f))
                  Icon(
                      Icons.Outlined.CameraAlt, 
                      contentDescription = "Image Search", 
                      tint = MaterialTheme.colorScheme.primary, 
                      modifier = Modifier.padding(horizontal = 8.dp).size(20.dp).clickable(
                         interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() },
                         indication = null
                      ) { 
                         try { context.startActivity(chooserIntent) } catch(e: Exception) {} 
                      }
                  )
                  Icon(
                      Icons.Outlined.Mic, 
                      contentDescription = "Voice Search", 
                      tint = MaterialTheme.colorScheme.primary, 
                      modifier = Modifier.padding(start = 8.dp).size(20.dp).clickable(
                         interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() },
                         indication = null
                      ) { 
                         try { context.startActivity(voiceIntent) } catch(e: Exception) {} 
                      }
                  )
              }
           }"""

# Replace search bar in HomeScreen
content = re.sub(
    r'// Search Bar overlaying the banner at the top[\s\S]*?// Pager Indicators',
    lambda m: replace_search_bar(m) + '\n           // Pager Indicators',
    content
)

# Remove the `.clip(RoundedCornerShape(bottomStart = 24.dp, bottomEnd = 24.dp))`
content = content.replace(
    '.clip(RoundedCornerShape(bottomStart = 24.dp, bottomEnd = 24.dp))',
    ''
)

# Remove the stray `Text("See All", ...)` at the end of the Banner box
content = re.sub(
    r'Text\("See All"[^)]*\)\n\s*\}\n\s*\}\n\s*item \{\n\s*// Circle Deals',
    r'}\n      }\n\n      item {\n        // Circle Deals',
    content
)


# 3. ProductCard: Replace rating with what user wants: rating and sold count instead of progress bar.
# The user wants "Show: Discount badge, Product image, Product title (max 2 lines), Current price, Original price, Rating, Sold count"
# And "Cards must have a premium appearance with rounded corners, soft shadows, and smooth touch animations."
product_card_replacement = """@Composable
fun ProductCard(product: Product, modifier: Modifier = Modifier, isCircleDeal: Boolean = false) {
  var isPressed by remember { mutableStateOf(false) }
  val scale by androidx.compose.animation.core.animateFloatAsState(
     targetValue = if (isPressed) 0.95f else 1f, 
     label = "scale"
  )
  
  Card(
    modifier = modifier
        .androidx.compose.ui.graphics.graphicsLayer {
            scaleX = scale
            scaleY = scale
        }
        .clickable(
           interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() },
           indication = androidx.compose.material.ripple.rememberRipple()
        ) { isPressed = true }
        .shadow(4.dp, RoundedCornerShape(12.dp)),
    colors = CardDefaults.cardColors(containerColor = Color.White),
    elevation = CardDefaults.cardElevation(defaultElevation = 0.dp),
    shape = RoundedCornerShape(12.dp)
  ) {
    Column(modifier = Modifier.padding(8.dp)) {
      Box(modifier = Modifier.fillMaxWidth().aspectRatio(1f).clip(RoundedCornerShape(8.dp)).background(Color(0xFFF5F5F5))) {
        AsyncImage(
          model = product.imageUrl,
          contentDescription = product.title,
          contentScale = ContentScale.Crop,
          modifier = Modifier.fillMaxSize()
        )
        if (product.discount != null) {
          Box(
            modifier = Modifier
              .align(Alignment.TopStart)
              .clip(RoundedCornerShape(bottomEnd = 8.dp))
              .background(MaterialTheme.colorScheme.primary)
              .padding(horizontal = 6.dp, vertical = 2.dp)
          ) {
            Text("-${product.discount}%", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold)
          }
        }
      }
      Spacer(modifier = Modifier.height(8.dp))
      Text(
        product.title,
        style = MaterialTheme.typography.bodyMedium,
        fontWeight = FontWeight.Medium,
        maxLines = 2,
        overflow = TextOverflow.Ellipsis,
        color = Color.Black,
        lineHeight = 16.sp
      )
      Spacer(modifier = Modifier.height(4.dp))
      Row(verticalAlignment = Alignment.Bottom) {
        Text(
          "৳ ${product.price.toInt()}",
          style = MaterialTheme.typography.titleMedium,
          fontWeight = FontWeight.Bold,
          color = MaterialTheme.colorScheme.primary
        )
        if (product.oldPrice != null) {
          Spacer(modifier = Modifier.width(6.dp))
          Text(
            "৳ ${product.oldPrice.toInt()}",
            style = MaterialTheme.typography.bodySmall,
            color = Color.Gray,
            textDecoration = TextDecoration.LineThrough
          )
        }
      }
      Spacer(modifier = Modifier.height(6.dp))
      Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
        Row(verticalAlignment = Alignment.CenterVertically) {
          Icon(Icons.Filled.Star, contentDescription = "Rating", tint = Color(0xFFFFB300), modifier = Modifier.size(12.dp))
          Spacer(modifier = Modifier.width(2.dp))
          Text("${product.rating}", fontSize = 10.sp, color = Color.Black, fontWeight = FontWeight.Medium)
          Spacer(modifier = Modifier.width(4.dp))
          Text("|", fontSize = 10.sp, color = Color.LightGray)
          Spacer(modifier = Modifier.width(4.dp))
          Text("${product.soldCount} Sold", fontSize = 10.sp, color = Color.Gray)
        }
      }
    }
  }
}"""

content = re.sub(
    r'@Composable\nfun ProductCard\(product: Product, modifier: Modifier = Modifier, isCircleDeal: Boolean = false\) \{[\s\S]*?\n\}\n\n@Composable\nfun ProfileScreen',
    product_card_replacement + '\n\n@Composable\nfun ProfileScreen',
    content
)


# 4. SearchScreen Implementation
search_screen_replacement = """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SearchScreen(onBack: () -> Unit) {
  var query by remember { mutableStateOf("") }
  val focusRequester = remember { androidx.compose.ui.focus.FocusRequester() }
  val context = androidx.compose.ui.platform.LocalContext.current
  val prefs = remember { context.getSharedPreferences("search_history", android.content.Context.MODE_PRIVATE) }
  var history by remember { mutableStateOf(prefs.getStringSet("history", emptySet())?.toList() ?: emptyList()) }

  val voiceIntent = remember { android.content.Intent(android.speech.RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply { putExtra(android.speech.RecognizerIntent.EXTRA_LANGUAGE_MODEL, android.speech.RecognizerIntent.LANGUAGE_MODEL_FREE_FORM) } }
  val pickIntent = remember { android.content.Intent(android.content.Intent.ACTION_PICK, android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI) }
  val takePhotoIntent = remember { android.content.Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE) }
  val chooserIntent = remember { android.content.Intent.createChooser(pickIntent, "Select Image").apply { putExtra(android.content.Intent.EXTRA_INITIAL_INTENTS, arrayOf(takePhotoIntent)) } }

  fun saveQuery(q: String) {
      if (q.isNotBlank()) {
          val newHistory = (listOf(q) + history).distinct().take(15)
          history = newHistory
          prefs.edit().putStringSet("history", newHistory.toSet()).apply()
      }
  }

  LaunchedEffect(Unit) {
      focusRequester.requestFocus()
  }

  Column(modifier = Modifier.fillMaxSize().background(Color(0xFFF8F9FA))) {
    // White Header
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .background(Color.White)
            .statusBarsPadding()
            .padding(vertical = 8.dp, horizontal = 4.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        IconButton(onClick = onBack) { Icon(Icons.Outlined.ArrowBack, contentDescription = "Back", tint = Color.Black) }
        
        BasicTextField(
            value = query,
            onValueChange = { query = it },
            modifier = Modifier
                .weight(1f)
                .height(40.dp)
                .background(Color(0xFFF1F3F4), RoundedCornerShape(20.dp))
                .padding(horizontal = 16.dp)
                .androidx.compose.ui.focus.focusRequester(focusRequester),
            singleLine = true,
            textStyle = androidx.compose.ui.text.TextStyle(fontSize = 14.sp, color = Color.Black),
            keyboardOptions = androidx.compose.foundation.text.KeyboardOptions(imeAction = androidx.compose.ui.text.input.ImeAction.Search),
            keyboardActions = androidx.compose.foundation.text.KeyboardActions(onSearch = { saveQuery(query) }),
            decorationBox = { innerTextField ->
                Row(verticalAlignment = Alignment.CenterVertically) {
                    if (query.isEmpty()) {
                        Text("Search products, brands...", color = Color.Gray, fontSize = 14.sp)
                    }
                    innerTextField()
                }
            }
        )
        
        Spacer(Modifier.width(8.dp))
        Icon(
            Icons.Outlined.CameraAlt, 
            contentDescription = "Image Search", 
            tint = Color.Black, 
            modifier = Modifier.padding(8.dp).size(24.dp).clickable(
                interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() },
                indication = null
            ) { try { context.startActivity(chooserIntent) } catch(e: Exception) {} }
        )
        Icon(
            Icons.Outlined.Mic, 
            contentDescription = "Voice Search", 
            tint = Color.Black, 
            modifier = Modifier.padding(8.dp).size(24.dp).clickable(
                interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() },
                indication = null
            ) { try { context.startActivity(voiceIntent) } catch(e: Exception) {} }
        )
        Spacer(Modifier.width(8.dp))
    }
    
    // Search History
    if (history.isNotEmpty()) {
        Row(modifier = Modifier.fillMaxWidth().padding(16.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
            Text("Recent Searches", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
            Text("Clear All", color = MaterialTheme.colorScheme.primary, fontSize = 12.sp, modifier = Modifier.clickable {
                history = emptyList()
                prefs.edit().putStringSet("history", emptySet()).apply()
            })
        }
        LazyColumn(modifier = Modifier.fillMaxWidth()) {
            items(history) { item ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { query = item; saveQuery(item) }
                        .padding(horizontal = 16.dp, vertical = 12.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(Icons.Outlined.History, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(20.dp))
                    Spacer(Modifier.width(16.dp))
                    Text(item, modifier = Modifier.weight(1f), fontSize = 14.sp)
                    Icon(
                        Icons.Outlined.Close, 
                        contentDescription = "Remove", 
                        tint = Color.Gray, 
                        modifier = Modifier.size(20.dp).clickable {
                            val newHistory = history.filter { it != item }
                            history = newHistory
                            prefs.edit().putStringSet("history", newHistory.toSet()).apply()
                        }
                    )
                }
            }
        }
    } else {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Icon(Icons.Outlined.Search, contentDescription = null, modifier = Modifier.size(48.dp), tint = Color.LightGray)
                Spacer(modifier = Modifier.height(16.dp))
                Text("Search for premium products", color = Color.Gray)
            }
        }
    }
  }
}"""

content = re.sub(
    r'@OptIn\(ExperimentalMaterial3Api::class\)\n@Composable\nfun SearchScreen\(onBack: \(\) -> Unit\) \{[\s\S]*?\n\}\n\n@Composable\nfun CameraSearchScreen',
    search_screen_replacement + '\n\n@Composable\nfun CameraSearchScreen',
    content
)


# 5. Fix Home Page's LazyRow to show the first 20 products in the Circle Deals grid instead?
# The prompt says: "Circle Deals Section: Redesign the Circle Deals product grid. Make each product card slightly slimmer and more compact. Display exactly 20 products initially. Arrange them in a two-column grid (2 products per row, total 10 rows)."
# But wait, Home Page has a LazyRow for circle deals. Does the user want the Home Page Circle Deals section to be a two-column grid (10 rows)? 
# "Arrange them in a two-column grid (2 products per row, total 10 rows)." Yes, this is usually a vertical grid.
# Let's replace the `LazyRow` under Circle Deals with a grid in the `LazyColumn`.

# Wait, `HomeScreen` `LazyColumn` currently has:
# item { Circle Deals Title and Timer }
# item { LazyRow }
# item { Categories }
# item { Just For You }
# items(chunkedProducts)
# The user wants "Circle Deals Section ... Arrange them in a two-column grid (2 products per row, total 10 rows)."
# I will change the Circle Deals section in `HomeScreen` to display the grid directly, OR maybe they meant the `CircleDealsScreen`?
# "Circle Deals Section ... Arrange them in a two-column grid (2 products per row, total 10 rows)."
# If they mean the Home Page section, then `LazyRow` is wrong.
# Let's change the Home Page section to the 10 rows.

circle_deals_replacement = """        // Circle Deals Section
        Row(
           modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),
           horizontalArrangement = Arrangement.SpaceBetween,
           verticalAlignment = Alignment.CenterVertically
        ) {
           Row(verticalAlignment = Alignment.CenterVertically) {
             val infiniteTransition = androidx.compose.animation.core.rememberInfiniteTransition(label = "shimmer")
             val translateAnim = infiniteTransition.animateFloat(
                initialValue = 0f,
                targetValue = 1000f,
                animationSpec = androidx.compose.animation.core.infiniteRepeatable(
                    animation = androidx.compose.animation.core.tween(durationMillis = 3000, easing = androidx.compose.animation.core.LinearEasing),
                    repeatMode = androidx.compose.animation.core.RepeatMode.Restart
                ), label = "shimmerTranslate"
             )
             val brush = androidx.compose.ui.graphics.Brush.linearGradient(
                colors = listOf(Color(0xFF4CAF50), Color(0xFFFFC107), Color(0xFFFF9800), Color(0xFFFFD700), Color(0xFF4CAF50)),
                start = androidx.compose.ui.geometry.Offset(translateAnim.value, translateAnim.value),
                end = androidx.compose.ui.geometry.Offset(translateAnim.value + 200f, translateAnim.value + 200f)
             )
             Text(
                text = "CIRCLE DEALS", 
                style = MaterialTheme.typography.titleLarge.copy(
                    fontWeight = FontWeight.ExtraBold,
                    letterSpacing = 1.sp,
                    brush = brush,
                    shadow = androidx.compose.ui.graphics.Shadow(
                        color = Color(0xFFFFC107).copy(alpha = 0.5f), 
                        offset = androidx.compose.ui.geometry.Offset(0f, 4f), 
                        blurRadius = 8f
                    )
                )
             )
             Spacer(modifier = Modifier.width(12.dp))
             val timerBg = Color(0xFFFFB300)
             val timerText = Color.Black
             Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                 Box(modifier = Modifier.clip(RoundedCornerShape(6.dp)).background(timerBg).padding(horizontal = 6.dp, vertical = 3.dp)) {
                     Text("02", color = timerText, fontSize = 12.sp, fontWeight = FontWeight.ExtraBold)
                 }
                 Text(":", color = timerBg, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                 Box(modifier = Modifier.clip(RoundedCornerShape(6.dp)).background(timerBg).padding(horizontal = 6.dp, vertical = 3.dp)) {
                     Text("45", color = timerText, fontSize = 12.sp, fontWeight = FontWeight.ExtraBold)
                 }
                 Text(":", color = timerBg, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                 Box(modifier = Modifier.clip(RoundedCornerShape(6.dp)).background(timerBg).padding(horizontal = 6.dp, vertical = 3.dp)) {
                     Text("12", color = timerText, fontSize = 12.sp, fontWeight = FontWeight.ExtraBold)
                 }
             }
           }
        }
        Spacer(modifier = Modifier.height(12.dp))
      }
      
      // Circle Deals Grid (10 rows, 2 columns, exactly 20 products)
      val circleDealsProducts = mockProducts.take(20).chunked(2)
      items(circleDealsProducts) { rowProducts ->
        Row(
          modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 6.dp),
          horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
          for (product in rowProducts) {
            ProductCard(product, modifier = Modifier.weight(1f))
          }
          if (rowProducts.size == 1) {
            Spacer(modifier = Modifier.weight(1f))
          }
        }
      }
      
      item {
        Spacer(modifier = Modifier.height(24.dp))
"""

content = re.sub(
    r'// Circle Deals\n\s*Row\([\s\S]*?Spacer\(modifier = Modifier\.height\(24\.dp\)\)\n\s*\}\n\s*item \{\n\s*SectionTitle\("Categories"',
    circle_deals_replacement + '        SectionTitle("Categories"',
    content
)


# Add missing imports for SearchScreen BasicTextField
if 'import androidx.compose.foundation.text.BasicTextField' not in content:
    content = content.replace('import androidx.compose.foundation.layout.*', 'import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.text.BasicTextField')


with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

