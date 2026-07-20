package com.example

import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.animation.core.RepeatMode


import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.outlined.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.Alignment
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.Modifier
import androidx.compose.ui.input.nestedscroll.nestedScroll
import androidx.compose.ui.draw.clip

import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.focus.focusRequester
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavDestination.Companion.hierarchy
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import coil.compose.AsyncImage
import com.example.ui.theme.MyApplicationTheme

class MainActivity : ComponentActivity() {
  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    enableEdgeToEdge()
    setContent {
      MyApplicationTheme {
        MainScreen()
      }
    }
  }
}

sealed class Screen(val route: String, val title: String, val icon: androidx.compose.ui.graphics.vector.ImageVector, val selectedIcon: androidx.compose.ui.graphics.vector.ImageVector) {
  object Home : Screen("home", "Home", Icons.Outlined.Home, Icons.Filled.Home)
  object Category : Screen("category", "Category", Icons.Outlined.GridView, Icons.Filled.GridView)
  object Cart : Screen("cart", "Cart", Icons.Outlined.ShoppingCart, Icons.Filled.ShoppingCart)
  object Orders : Screen("orders", "Orders", Icons.Outlined.List, Icons.Filled.List)
  object Profile : Screen("profile", "Profile", Icons.Outlined.Person, Icons.Filled.Person)
  object Search : Screen("search", "Search", Icons.Outlined.Search, Icons.Filled.Search)
  object CameraSearch : Screen("camera", "Camera", Icons.Outlined.CameraAlt, Icons.Filled.CameraAlt)
  object CircleDeals : Screen("circle_deals", "Circle Deals", Icons.Outlined.LocalOffer, Icons.Filled.LocalOffer)
}

@Composable
fun MainScreen() {
  val navController = rememberNavController()
  val items = listOf(
    Screen.Home,
    Screen.Category,
    Screen.Cart,
    Screen.Orders,
    Screen.Profile
  )

  val bottomBarHeight = 80.dp
  val bottomBarHeightPx = with(androidx.compose.ui.platform.LocalDensity.current) { bottomBarHeight.toPx() }
  // Allow an extra 40dp for safe area/system nav bar to ensure it hides completely
  val maxOffsetPx = with(androidx.compose.ui.platform.LocalDensity.current) { (bottomBarHeight + 40.dp).toPx() }
  val bottomBarOffsetHeightPx = remember { androidx.compose.runtime.mutableFloatStateOf(0f) }

  val nestedScrollConnection = remember {
      object : androidx.compose.ui.input.nestedscroll.NestedScrollConnection {
          override fun onPreScroll(available: androidx.compose.ui.geometry.Offset, source: androidx.compose.ui.input.nestedscroll.NestedScrollSource): androidx.compose.ui.geometry.Offset {
              val delta = available.y
              val newOffset = bottomBarOffsetHeightPx.floatValue - delta
              bottomBarOffsetHeightPx.floatValue = newOffset.coerceIn(0f, maxOffsetPx)
              return androidx.compose.ui.geometry.Offset.Zero
          }
      }
  }

  Scaffold(
    modifier = Modifier.nestedScroll(nestedScrollConnection),
    bottomBar = {
      NavigationBar(
        modifier = Modifier.offset { androidx.compose.ui.unit.IntOffset(x = 0, y = bottomBarOffsetHeightPx.floatValue.toInt()) },
        containerColor = MaterialTheme.colorScheme.surface,
        tonalElevation = 8.dp
      ) {
        val navBackStackEntry by navController.currentBackStackEntryAsState()
        val currentDestination = navBackStackEntry?.destination
        items.forEach { screen ->
          NavigationBarItem(
            icon = {
              Icon(
                imageVector = if (currentDestination?.hierarchy?.any { it.route == screen.route } == true) screen.selectedIcon else screen.icon,
                contentDescription = screen.title
              )
            },
            label = { Text(screen.title, fontSize = 10.sp) },
            selected = currentDestination?.hierarchy?.any { it.route == screen.route } == true,
            onClick = {
              navController.navigate(screen.route) {
                popUpTo(navController.graph.findStartDestination().id) {
                  saveState = true
                }
                launchSingleTop = true
                restoreState = true
              }
            },
            colors = NavigationBarItemDefaults.colors(
              selectedIconColor = MaterialTheme.colorScheme.onSecondaryContainer,
              selectedTextColor = MaterialTheme.colorScheme.onSecondaryContainer,
              indicatorColor = MaterialTheme.colorScheme.secondaryContainer,
              unselectedIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
              unselectedTextColor = MaterialTheme.colorScheme.onSurfaceVariant
            )
          )
        }
      }
    }
  ) { innerPadding ->
    val currentBottomOffsetDp = with(androidx.compose.ui.platform.LocalDensity.current) { bottomBarOffsetHeightPx.floatValue.toDp() }
    val bottomPadding = maxOf(0.dp, innerPadding.calculateBottomPadding() - currentBottomOffsetDp)
    NavHost(
      navController = navController,
      startDestination = Screen.Home.route,
      modifier = Modifier.padding(bottom = bottomPadding)
    ) {
      composable(Screen.Home.route) { HomeScreen(onSearchClick = { navController.navigate(Screen.Search.route) }, onCameraClick = { navController.navigate(Screen.CameraSearch.route) }, onCircleDealsClick = { navController.navigate(Screen.CircleDeals.route) }) }
      composable(Screen.Category.route) { CategoryScreen() }
      composable(Screen.Cart.route) { CartScreen() }
      composable(Screen.Orders.route) { OrdersScreen() }
      composable(Screen.Profile.route) { ProfileScreen() }
      composable(Screen.Search.route) { SearchScreen(onBack = { navController.popBackStack() }) }
      composable(Screen.CameraSearch.route) { CameraSearchScreen(onBack = { navController.popBackStack() }) }
      composable(
        Screen.CircleDeals.route,
        deepLinks = listOf(androidx.navigation.navDeepLink { uriPattern = "https://circlebazar.com/deals" })
      ) { CircleDealsScreen(onBack = { navController.popBackStack() }) }
    }
  }
}

// Data Models
data class Product(
  val id: Int,
  val title: String,
  val imageUrl: String,
  val price: Double,
  val oldPrice: Double? = null,
  val rating: Double,
  val soldCount: Int,
  val discount: Int? = null,
  val stock: Int = 20,
  val maxStock: Int = 100
)

val images = listOf(
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
}

@OptIn(ExperimentalMaterial3Api::class, androidx.compose.foundation.ExperimentalFoundationApi::class)
@Composable
fun HomeScreen(onSearchClick: () -> Unit = {}, onCameraClick: () -> Unit = {}, onCircleDealsClick: () -> Unit = {}) {
  val listState = rememberLazyListState()
  // Generate 20 products by repeating and shuffling
  var circleDealsList by remember { 
      val doubled = mockProducts + mockProducts
      mutableStateOf(doubled.shuffled().take(20))
  }
  
  LaunchedEffect(Unit) {
      while (true) {
          kotlinx.coroutines.delay(1000) // Sell a product every second
          if (circleDealsList.isNotEmpty()) {
              val randomIndex = circleDealsList.indices.random()
              val product = circleDealsList[randomIndex]
              if (product.stock > 0) {
                  val updatedProduct = product.copy(
                      stock = product.stock - 1,
                      soldCount = product.soldCount + 1
                  )
                  val newList = circleDealsList.toMutableList()
                  newList[randomIndex] = updatedProduct
                  circleDealsList = newList
              }
          }
      }
  }

  val showStickyHeader by remember {
     derivedStateOf { listState.firstVisibleItemIndex > 0 || listState.firstVisibleItemScrollOffset > 0 }
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
                  modifier = Modifier.fillMaxSize()
               )
           }
           
           // Gradient overlay for better status bar visibility
           Box(modifier = Modifier.fillMaxWidth().height(280.dp).background(androidx.compose.ui.graphics.Brush.verticalGradient(listOf(Color.Black.copy(alpha = 0.7f), Color.Transparent))))
           
           // Search Bar overlaying the banner at the top
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
        // Spacer to separate banner and deals
        Spacer(modifier = Modifier.height(24.dp))
        // Circle Deals Section
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
                 }             }
           }
           Text("Show More", color = MaterialTheme.colorScheme.primary, fontSize = 12.sp, fontWeight = FontWeight.Medium, modifier = Modifier.clickable { onCircleDealsClick() })
        }
        Spacer(modifier = Modifier.height(12.dp))
      }
      
      item {
        androidx.compose.foundation.lazy.grid.LazyHorizontalGrid(
            rows = androidx.compose.foundation.lazy.grid.GridCells.Fixed(2),
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
            modifier = Modifier.fillMaxWidth().height(480.dp) // Approximate height for 2 rows of 240dp cards + spacing
        ) {
            items(circleDealsList.size) { index ->
                CircleDealCard(circleDealsList[index], modifier = Modifier.width(130.dp))
            }
        }
      }
      
      item {
        Spacer(modifier = Modifier.height(24.dp))
        SectionTitle("Categories", "See All")
                LazyRow(
          contentPadding = PaddingValues(horizontal = 16.dp),
          horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
          val categories = listOf("Electronics", "Fashion", "Home", "Beauty", "Sports")
          val icons = listOf(Icons.Outlined.Phone, Icons.Outlined.Checkroom, Icons.Outlined.Chair, Icons.Outlined.Face, Icons.Outlined.SportsBasketball)
          items(categories.size) { index ->
            CategoryItem(categories[index], icons[index])
          }
        }
        Spacer(modifier = Modifier.height(16.dp))
      }

      item {
        SectionTitle("Just For You", "")
      }

      // Products Grid
      val chunkedProducts = mockProducts.chunked(2)
      items(chunkedProducts) { rowProducts ->
        Row(
          modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 8.dp, vertical = 6.dp),
          horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
          for (product in rowProducts) {
            ProductCard(product, modifier = Modifier.weight(1f))
          }
          if (rowProducts.size == 1) {
            Spacer(modifier = Modifier.weight(1f))
          }
        }
      }
      
      item { Spacer(modifier = Modifier.height(32.dp)) }
    }

    // Sticky Header
    androidx.compose.animation.AnimatedVisibility(
       visible = showStickyHeader,
       enter = androidx.compose.animation.fadeIn() + androidx.compose.animation.slideInVertically(
           initialOffsetY = { -it }
       ),
       exit = androidx.compose.animation.fadeOut() + androidx.compose.animation.slideOutVertically(
           targetOffsetY = { -it }
       ),
       modifier = Modifier.align(Alignment.TopCenter)
    ) {
       Surface(
         modifier = Modifier.fillMaxWidth(),
         color = Color.White,
         shadowElevation = 8.dp,
         shape = androidx.compose.ui.graphics.RectangleShape // Sharp corners at the bottom
       ) {
           Row(
               modifier = Modifier
                   .fillMaxWidth()
                   .windowInsetsPadding(androidx.compose.foundation.layout.WindowInsets.statusBars)
                   .padding(horizontal = 16.dp, vertical = 6.dp),
               horizontalArrangement = Arrangement.SpaceBetween,
               verticalAlignment = Alignment.CenterVertically
           ) {
               // Logo and Title (Left aligned)
               Row(
                   verticalAlignment = Alignment.CenterVertically
               ) {
                   AsyncImage(
                       model = "https://storage.googleapis.com/aistudio-chat-blob-store/b20464f1d43a60a7d97ab1607ef8987b.jpg",
                       contentDescription = "Logo",
                       modifier = Modifier.size(32.dp).clip(CircleShape),
                       contentScale = ContentScale.Crop
                   )
                   Spacer(modifier = Modifier.width(10.dp))
                   Text(
                       "Circle Bazar", 
                       style = MaterialTheme.typography.titleLarge.copy(
                           fontWeight = FontWeight.ExtraBold,
                           fontStyle = androidx.compose.ui.text.font.FontStyle.Italic,
                           fontFamily = FontFamily.SansSerif,
                           fontSize = 20.sp,
                           color = Color(0xFF00643C)
                       )
                   )
               }
               
               // Icons (Right aligned, better styling)
               Row(
                   horizontalArrangement = Arrangement.spacedBy(16.dp),
                   verticalAlignment = Alignment.CenterVertically
               ) {
                   Icon(painter = androidx.compose.ui.res.painterResource(R.drawable.ic_custom_search), contentDescription = "Search", tint = Color(0xFF333333), modifier = Modifier.size(22.dp).clickable { onSearchClick() })
                   Icon(painter = androidx.compose.ui.res.painterResource(R.drawable.ic_custom_notification), contentDescription = "Notifications", tint = Color(0xFF333333), modifier = Modifier.size(22.dp).clickable { })
               }
           }
       }
    }
  }
}

@Composable
fun SectionTitle(title: String, action: String) {
  Row(
    modifier = Modifier
      .fillMaxWidth()
      .padding(horizontal = 16.dp, vertical = 8.dp),
    horizontalArrangement = Arrangement.SpaceBetween,
    verticalAlignment = Alignment.CenterVertically
  ) {
    Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
    if (action.isNotEmpty()) {
      Text(action, color = MaterialTheme.colorScheme.primary, style = MaterialTheme.typography.bodyMedium)
    }
  }
}

@Composable
fun ProductCard(product: Product, modifier: Modifier = Modifier) {
  Card(
    modifier = modifier.fillMaxWidth(),
    colors = CardDefaults.cardColors(containerColor = Color.White),
    elevation = CardDefaults.cardElevation(defaultElevation = 0.dp),
    shape = RoundedCornerShape(8.dp),
    border = BorderStroke(1.dp, Color(0xFF4CAF50))
  ) {
    Box {
      Column(modifier = Modifier.padding(10.dp)) {
        Box(modifier = Modifier.fillMaxWidth().aspectRatio(1f).padding(top = 12.dp)) {
          AsyncImage(
            model = product.imageUrl,
            contentDescription = product.title,
            contentScale = ContentScale.Fit,
            modifier = Modifier.fillMaxSize()
          )
        }
        Spacer(modifier = Modifier.height(8.dp))
        Text(
          product.title,
          style = MaterialTheme.typography.bodyMedium,
          maxLines = 1,
          overflow = TextOverflow.Ellipsis,
          color = Color.Black
        )
        Spacer(modifier = Modifier.height(4.dp))
        Row(verticalAlignment = Alignment.CenterVertically) {
          Text(
            "৳ ${product.price.toInt()}",
            style = MaterialTheme.typography.titleMedium,
            color = Color(0xFF4CAF50),
            fontWeight = FontWeight.Bold
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
        Spacer(modifier = Modifier.height(8.dp))
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
          Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.weight(1f)) {
            Icon(Icons.Filled.Star, contentDescription = "Rating", tint = Color(0xFFFFC107), modifier = Modifier.size(14.dp))
            Spacer(modifier = Modifier.width(2.dp))
            Text("${product.rating}", fontSize = 11.sp, color = Color.Black, fontWeight = FontWeight.Medium)
            Spacer(modifier = Modifier.width(2.dp))
            Text("(${product.soldCount})", fontSize = 10.sp, color = Color.Gray, maxLines = 1, overflow = TextOverflow.Ellipsis)
            Spacer(modifier = Modifier.width(2.dp))
            Text("|", fontSize = 10.sp, color = Color.LightGray)
            Spacer(modifier = Modifier.width(2.dp))
            Text("Sold ${if(product.soldCount >= 1000) "${product.soldCount/1000.0}k+".replace(".0k+", "k+") else "${product.soldCount}+"}", fontSize = 10.sp, color = Color.Gray, maxLines = 1, overflow = TextOverflow.Ellipsis)
          }
          Spacer(modifier = Modifier.width(4.dp))
          Box(
            modifier = Modifier
              .size(28.dp)
              .clip(RoundedCornerShape(8.dp))
              .background(Color(0xFF4CAF50))
              .clickable { },
            contentAlignment = Alignment.Center
          ) {
            Icon(Icons.Outlined.ShoppingCart, contentDescription = "Add to Cart", tint = Color.White, modifier = Modifier.size(16.dp))
          }
        }
      }
      
      // Top Left Corner - Discount Badge
      if (product.discount != null) {
        Box(
          modifier = Modifier
            .align(Alignment.TopStart)
            .clip(RoundedCornerShape(topStart = 8.dp, bottomEnd = 8.dp))
            .background(Color(0xFF4CAF50))
            .padding(horizontal = 6.dp, vertical = 2.dp)
        ) {
          Text("-${product.discount}%", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold)
        }
      }
      
      // Top Right Corner - Favorite Icon
      Icon(
        Icons.Outlined.FavoriteBorder,
        contentDescription = "Favorite",
        tint = Color.Gray,
        modifier = Modifier
            .align(Alignment.TopEnd)
            .padding(8.dp)
            .size(20.dp)
            .clickable { }
      )
    }
  }
}

@Composable
fun CircleDealCard(product: Product, modifier: Modifier = Modifier) {
  Card(
    modifier = modifier.clickable { },
    colors = CardDefaults.cardColors(containerColor = Color.White),
    elevation = CardDefaults.cardElevation(defaultElevation = 0.dp),
    shape = RoundedCornerShape(8.dp),
    border = BorderStroke(1.dp, Color(0xFF4CAF50))
  ) {
    Box {
      Column(modifier = Modifier.padding(6.dp)) { // Reduced padding from 8dp to 6dp
        Box(modifier = Modifier.fillMaxWidth().aspectRatio(1f).padding(top = 4.dp)) { // Reduced top padding
          AsyncImage(
            model = product.imageUrl,
            contentDescription = product.title,
            contentScale = ContentScale.Fit,
            modifier = Modifier.fillMaxSize()
          )
        }
        Spacer(modifier = Modifier.height(4.dp))
        Text(
          product.title,
          style = MaterialTheme.typography.bodyMedium,
          fontWeight = FontWeight.Medium,
          maxLines = 1,
          overflow = TextOverflow.Ellipsis,
          color = Color.Black
        )
        Spacer(modifier = Modifier.height(2.dp))
        
        Row(verticalAlignment = Alignment.Bottom, modifier = Modifier.fillMaxWidth()) {
          Text(
            "৳ ${product.price.toInt()}",
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.Bold,
            color = Color(0xFF4CAF50)
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
        Spacer(modifier = Modifier.height(6.dp))
        
        // Stock Progress Bar (Green)
        val progress = (product.maxStock - product.stock).toFloat() / product.maxStock.toFloat()
        
        Column(modifier = Modifier.fillMaxWidth()) {
           Text("Only ${product.stock} Left", fontSize = 13.sp, color = Color(0xFF4CAF50), fontWeight = FontWeight.Bold) // Made larger
           Spacer(modifier = Modifier.height(4.dp))
           Box(modifier = Modifier.fillMaxWidth().height(6.dp).clip(RoundedCornerShape(3.dp)).background(Color(0xFFE0E0E0))) { // Made thicker
              Box(modifier = Modifier.fillMaxWidth(progress).height(6.dp).clip(RoundedCornerShape(3.dp)).background(Color(0xFF4CAF50))) // Made thicker
           }
        }
      }
      
      // Top Left Corner - Discount Badge
      if (product.discount != null) {
        Box(
          modifier = Modifier
            .align(Alignment.TopStart)
            .clip(RoundedCornerShape(topStart = 8.dp, bottomEnd = 8.dp))
            .background(Color(0xFF4CAF50))
            .padding(horizontal = 6.dp, vertical = 2.dp)
        ) {
          Text("-${product.discount}%", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold)
        }
      }
      
      // Top Right Corner - Favorite Icon
      Icon(
        Icons.Outlined.FavoriteBorder,
        contentDescription = "Favorite",
        tint = Color.Gray,
        modifier = Modifier
            .align(Alignment.TopEnd)
            .padding(8.dp)
            .size(20.dp)
            .clickable { }
      )
    }
  }
}

@Composable
fun CategoryItem(name: String, icon: androidx.compose.ui.graphics.vector.ImageVector) {
  Column(horizontalAlignment = Alignment.CenterHorizontally) {
    Box(
      modifier = Modifier
        .size(64.dp)
        .clip(CircleShape)
        .background(MaterialTheme.colorScheme.surface)
        .border(1.dp, MaterialTheme.colorScheme.outline, CircleShape)
        .clickable { },
      contentAlignment = Alignment.Center
    ) {
      Box(modifier = Modifier.size(32.dp).clip(RoundedCornerShape(8.dp)).background(MaterialTheme.colorScheme.secondaryContainer), contentAlignment = Alignment.Center) {
          Icon(icon, contentDescription = name, tint = MaterialTheme.colorScheme.onSecondaryContainer, modifier = Modifier.size(20.dp))
      }
    }
    Spacer(modifier = Modifier.height(8.dp))
    Text(name, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.Medium)
  }
}


@Composable
fun ProfileScreen() {
  LazyColumn(
    modifier = Modifier
      .fillMaxSize()
      .background(MaterialTheme.colorScheme.background)
  ) {
    item {
      Box(
        modifier = Modifier
          .fillMaxWidth()
          .background(MaterialTheme.colorScheme.primary)
          .statusBarsPadding()
          .padding(24.dp)
      ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
          Box(
            modifier = Modifier
              .size(72.dp)
              .clip(CircleShape)
              .background(Color.White),
            contentAlignment = Alignment.Center
          ) {
            Icon(Icons.Filled.Person, contentDescription = null, modifier = Modifier.size(40.dp), tint = Color.LightGray)
          }
          Spacer(modifier = Modifier.width(16.dp))
          Column {
            Text("John Doe", color = Color.White, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
            Text("john.doe@example.com", color = Color.White.copy(alpha = 0.8f))
          }
        }
      }
    }
    
    val menuItems = listOf(
      "Orders" to Icons.Outlined.List,
      "Wishlist" to Icons.Outlined.FavoriteBorder,
      "Coupons" to Icons.Outlined.ConfirmationNumber,
      "Wallet" to Icons.Outlined.AccountBalanceWallet,
      "Addresses" to Icons.Outlined.LocationOn,
      "Settings" to Icons.Outlined.Settings,
      "Help" to Icons.Outlined.HelpOutline
    )
    
    items(menuItems) { (title, icon) ->
      Row(
        modifier = Modifier
          .fillMaxWidth()
          .clickable { }
          .padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
      ) {
        Icon(icon, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
        Spacer(modifier = Modifier.width(16.dp))
        Text(title, style = MaterialTheme.typography.bodyLarge, modifier = Modifier.weight(1f))
        Icon(Icons.Outlined.ChevronRight, contentDescription = null, tint = Color.Gray)
      }
      HorizontalDivider(color = MaterialTheme.colorScheme.surfaceVariant, thickness = 1.dp)
    }
    
    item {
      Row(
        modifier = Modifier
          .fillMaxWidth()
          .clickable { }
          .padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
      ) {
        Icon(Icons.Outlined.ExitToApp, contentDescription = null, tint = MaterialTheme.colorScheme.error)
        Spacer(modifier = Modifier.width(16.dp))
        Text("Logout", style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.error)
      }
    }
  }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CategoryScreen() {
  LazyColumn(modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)) {
    item {
      TopAppBar(
        title = { Text("Categories", fontWeight = FontWeight.Bold) },
        colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.surface)
      )
    }
    
    val categoriesList = listOf("Electronics", "Fashion & Apparel", "Home & Kitchen", "Beauty & Health", "Sports & Outdoors", "Automotive", "Toys & Games", "Books & Stationery")
    val iconsList = listOf(Icons.Outlined.Phone, Icons.Outlined.Checkroom, Icons.Outlined.Chair, Icons.Outlined.Face, Icons.Outlined.SportsBasketball, Icons.Outlined.DirectionsCar, Icons.Outlined.Toys, Icons.Outlined.Book)
    
    items(categoriesList.size) { index ->
      Row(
        modifier = Modifier
          .fillMaxWidth()
          .clickable { }
          .padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
      ) {
        Box(
          modifier = Modifier
            .size(48.dp)
            .clip(RoundedCornerShape(8.dp))
            .background(MaterialTheme.colorScheme.primaryContainer),
          contentAlignment = Alignment.Center
        ) {
          Icon(iconsList[index], contentDescription = null, tint = MaterialTheme.colorScheme.primary)
        }
        Spacer(modifier = Modifier.width(16.dp))
        Text(categoriesList[index], style = MaterialTheme.typography.titleMedium, modifier = Modifier.weight(1f))
        Icon(Icons.Outlined.ChevronRight, contentDescription = null, tint = Color.Gray)
      }
      HorizontalDivider(color = MaterialTheme.colorScheme.surfaceVariant, thickness = 1.dp)
    }
  }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CartScreen() {
  Column(modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)) {
    TopAppBar(
      title = { Text("My Cart", fontWeight = FontWeight.Bold) },
      colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.surface)
    )
    
    if (mockProducts.isEmpty()) {
      Box(modifier = Modifier.weight(1f).fillMaxWidth(), contentAlignment = Alignment.Center) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
          Icon(Icons.Outlined.ShoppingCart, contentDescription = null, modifier = Modifier.size(64.dp), tint = Color.LightGray)
          Spacer(modifier = Modifier.height(16.dp))
          Text("Your cart is empty", color = Color.Gray, style = MaterialTheme.typography.titleMedium)
        }
      }
    } else {
      LazyColumn(modifier = Modifier.weight(1f).padding(horizontal = 16.dp)) {
        items(mockProducts.take(2)) { product ->
          Row(
            modifier = Modifier
              .fillMaxWidth()
              .padding(vertical = 8.dp)
              .clip(RoundedCornerShape(12.dp))
              .background(MaterialTheme.colorScheme.surface)
              .padding(8.dp)
          ) {
            AsyncImage(
              model = product.imageUrl,
              contentDescription = null,
              contentScale = ContentScale.Crop,
              modifier = Modifier
                .size(80.dp)
                .clip(RoundedCornerShape(8.dp))
            )
            Spacer(modifier = Modifier.width(12.dp))
            Column(modifier = Modifier.weight(1f)) {
              Text(product.title, style = MaterialTheme.typography.titleSmall, maxLines = 2, overflow = TextOverflow.Ellipsis)
              Spacer(modifier = Modifier.height(4.dp))
              Text("$${product.price}", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
            }
            Column(horizontalAlignment = Alignment.End) {
              Icon(Icons.Outlined.Delete, contentDescription = "Remove", tint = MaterialTheme.colorScheme.error, modifier = Modifier.clickable {  })
              Spacer(modifier = Modifier.height(12.dp))
              Row(verticalAlignment = Alignment.CenterVertically) {
                Box(modifier = Modifier.size(24.dp).clip(CircleShape).background(MaterialTheme.colorScheme.surfaceVariant).clickable { }, contentAlignment = Alignment.Center) {
                  Text("-", fontWeight = FontWeight.Bold)
                }
                Text(" 1 ", modifier = Modifier.padding(horizontal = 8.dp))
                Box(modifier = Modifier.size(24.dp).clip(CircleShape).background(MaterialTheme.colorScheme.primary).clickable { }, contentAlignment = Alignment.Center) {
                  Text("+", color = Color.White, fontWeight = FontWeight.Bold)
                }
              }
            }
          }
        }
      }
      
      // Checkout section
      Column(
        modifier = Modifier
          .fillMaxWidth()
          .background(MaterialTheme.colorScheme.surface)
          .padding(16.dp)
      ) {
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
          Text("Subtotal", color = Color.Gray)
          Text("$528.99", fontWeight = FontWeight.Bold)
        }
        Spacer(modifier = Modifier.height(8.dp))
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
          Text("Delivery", color = Color.Gray)
          Text("$10.00", fontWeight = FontWeight.Bold)
        }
        Spacer(modifier = Modifier.height(8.dp))
        HorizontalDivider()
        Spacer(modifier = Modifier.height(8.dp))
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
          Text("Total", style = MaterialTheme.typography.titleMedium)
          Text("$538.99", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
        }
        Spacer(modifier = Modifier.height(16.dp))
        Button(
          onClick = { },
          modifier = Modifier.fillMaxWidth().height(280.dp),
          colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
        ) {
          Text("Checkout", fontSize = 16.sp)
        }
      }
    }
  }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun OrdersScreen() {
  Column(modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)) {
    TopAppBar(
      title = { Text("My Orders", fontWeight = FontWeight.Bold) },
      colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.surface)
    )
    
    LazyColumn(modifier = Modifier.fillMaxSize().padding(16.dp)) {
      items(3) { index ->
        Card(
          modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp),
          colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
        ) {
          Column(modifier = Modifier.padding(16.dp)) {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
              Text("Order #CB${10045 + index}", fontWeight = FontWeight.Bold)
              Text(
                if (index == 0) "Processing" else "Delivered",
                color = if (index == 0) MaterialTheme.colorScheme.primary else Color.Gray,
                style = MaterialTheme.typography.bodySmall
              )
            }
            Spacer(modifier = Modifier.height(8.dp))
            Text("Date: ${20 - index} Jul, 2026", color = Color.Gray, style = MaterialTheme.typography.bodySmall)
            Spacer(modifier = Modifier.height(12.dp))
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
              Text("Total Amount: $${125.00 * (index + 1)}", fontWeight = FontWeight.Medium)
              OutlinedButton(onClick = { }, modifier = Modifier.height(36.dp)) {
                Text("Track")
              }
            }
          }
        }
      }
    }
  }
}



@OptIn(ExperimentalMaterial3Api::class)
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
                .focusRequester(focusRequester),
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



@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CircleDealsScreen(onBack: () -> Unit = {}) {
  val context = androidx.compose.ui.platform.LocalContext.current
  val shareIntent = android.content.Intent(android.content.Intent.ACTION_SEND).apply {
      type = "text/plain"
      putExtra(android.content.Intent.EXTRA_SUBJECT, "Circle Bazar - Circle Deals")
      putExtra(android.content.Intent.EXTRA_TEXT, "Check out the amazing Circle Deals on Circle Bazar! \n\nhttps://circlebazar.com/deals")
  }
  
  var circleDealsList by remember { 
      mutableStateOf(mockProducts)
  }
  
  LaunchedEffect(Unit) {
      while (true) {
          kotlinx.coroutines.delay(1000) // Sell a product every second
          if (circleDealsList.isNotEmpty()) {
              val randomIndex = circleDealsList.indices.random()
              val product = circleDealsList[randomIndex]
              if (product.stock > 0) {
                  val updatedProduct = product.copy(
                      stock = product.stock - 1,
                      soldCount = product.soldCount + 1
                  )
                  val newList = circleDealsList.toMutableList()
                  newList[randomIndex] = updatedProduct
                  circleDealsList = newList
              }
          }
      }
  }
  
  Scaffold(
      topBar = {
          TopAppBar(
              title = { Text("Circle Deals", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold) },
              navigationIcon = {
                  IconButton(onClick = onBack) {
                      Icon(Icons.Outlined.ArrowBack, contentDescription = "Back")
                  }
              },
              actions = {
                  IconButton(onClick = {
                      val chooser = android.content.Intent.createChooser(shareIntent, "Share Circle Deals")
                      context.startActivity(chooser)
                  }) {
                      Icon(Icons.Outlined.Share, contentDescription = "Share")
                  }
              },
              colors = TopAppBarDefaults.topAppBarColors(
                  containerColor = Color.White,
                  titleContentColor = Color.Black,
                  navigationIconContentColor = Color.Black,
                  actionIconContentColor = Color.Black
              )
          )
      }
  ) { paddingValues ->
      LazyColumn(
          contentPadding = PaddingValues(top = paddingValues.calculateTopPadding(), bottom = 24.dp),
          modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)
      ) {
          val chunkedProducts = circleDealsList.chunked(2)
          items(chunkedProducts) { rowProducts ->
              Row(
                  modifier = Modifier
                      .fillMaxWidth()
                      .padding(horizontal = 8.dp, vertical = 6.dp),
                  horizontalArrangement = Arrangement.spacedBy(8.dp)
              ) {
                  for (product in rowProducts) {
                      CircleDealCard(product, modifier = Modifier.weight(1f))
                  }
                  if (rowProducts.size == 1) {
                      Spacer(modifier = Modifier.weight(1f))
                  }
              }
          }
      }
  }
}
