dependencies {
    // These replace your Kivy/MD requirements
    implementation("androidx.compose.ui:ui:1.5.0")
    implementation("androidx.compose.material3:material3:1.1.0")
    
    // This replaces 'json' and 'pillow' for data handling
    implementation("com.google.code.gson:gson:2.10.1")
    
    // Note: No 'arabic_reshaper' or 'python-bidi' needed! 
    // Android handles this automatically.
}
