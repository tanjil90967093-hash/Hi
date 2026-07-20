with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Fix modifier chaining
content = content.replace('.androidx.compose.ui.graphics.graphicsLayer {', '.graphicsLayer {')
content = content.replace('.androidx.compose.ui.focus.focusRequester(', '.focusRequester(')

# Fix rememberRipple warning (optional but good)
content = content.replace('androidx.compose.material.ripple.rememberRipple()', 'androidx.compose.material3.ripple()')

# Add imports
imports = """
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.focus.focusRequester
import androidx.compose.animation.core.animateFloatAsState
"""
if 'import androidx.compose.ui.graphics.graphicsLayer' not in content:
    content = content.replace('import androidx.compose.ui.graphics.Color', imports + 'import androidx.compose.ui.graphics.Color')

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
