package com.example.articaltrainer

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import java.io.IOException
import kotlin.random.Random

// --- DATA MODELS (Equivalent to your JSON structure) ---
data class NounData(
    val word: String,
    val article: String,
    val meaning: String,
    val sentences: Map<String, String>
)

data class Question(
    val noun: String,
    val meaning: String,
    val sentence: String,
    val case: String,
    val correctArticle: String,
    val articleOptions: List<String>,
    val meaningOptions: List<String>
)

// --- MAIN ACTIVITY (Equivalent to your App class) ---
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                GermanTrainerApp()
            }
        }
    }
}

// --- APP NAVIGATION & STATE ---
enum class Screen { STAGE_SELECT, GAME, RESULT }

@Composable
fun GermanTrainerApp() {
    // These variables replace your Kivy Properties (StringProperty, etc.)
    var currentScreen by remember { mutableStateOf(Screen.STAGE_SELECT) }
    var currentStage by remember { mutableStateOf(1) }
    var unlockedStages by remember { mutableStateOf(1) }
    var questionsPerStage = 11
    
    // Game State
    var questionCount by remember { mutableStateOf(0) }
    var correctCount by remember { mutableStateOf(0) }
    var currentQuestion by remember { mutableStateOf<Question?>(null) }
    var lastExplanation by remember { mutableStateOf("") }
    var resultMessage by remember { mutableStateOf("") }
    
    // Load Data Helper
    val context = LocalContext.current
    fun loadStageData(stage: Int): List<NounData> {
        val jsonString: String
        try {
            jsonString = context.assets.open("stages/stage_$stage.json")
                .bufferedReader().use { it.readText() }
            val listType = object : TypeToken<List<NounData>>() {}.type
            return Gson().fromJson(jsonString, listType)
        } catch (ioException: IOException) {
            ioException.printStackTrace()
            return emptyList()
        }
    }

    // Question Generator Logic
    fun generateQuestion(nouns: MutableList<NounData>) {
        if (nouns.isEmpty()) return

        val nounData = nouns.removeAt(nouns.lastIndex) // Pop equivalent
        val case = listOf("Nominativ", "Akkusativ", "Dativ").random()
        
        // Article Logic
        val cases = mapOf(
            "Nominativ" to mapOf("der" to "der", "die" to "die", "das" to "das"),
            "Akkusativ" to mapOf("der" to "den", "die" to "die", "das" to "das"),
            "Dativ" to mapOf("der" to "dem", "die" to "der", "das" to "dem")
        )
        val correctArticle = cases[case]!![nounData.article]!!
        
        val allArticles = listOf("der", "die", "das", "den", "dem")
        val wrongArticles = allArticles.filter { it != correctArticle }.shuffled().take(2)
        val articleOptions = (wrongArticles + correctArticle).shuffled()

        // Meaning Logic
        // (Simplified for brevity: In real app, load other meanings from full list)
        val meaningOptions = listOf(nounData.meaning, "Falsch 1", "Falsch 2").shuffled()

        currentQuestion = Question(
            noun = nounData.word,
            meaning = nounData.meaning, // ARABIC WORKS AUTOMATICALLY HERE!
            sentence = nounData.sentences[case] ?: "",
            case = case,
            correctArticle = correctArticle,
            articleOptions = articleOptions,
            meaningOptions = meaningOptions
        )
    }

    // --- SCREEN SWITCHER ---
    when (currentScreen) {
        Screen.STAGE_SELECT -> {
            StageSelectScreen(
                unlockedStages = unlockedStages,
                onStageClicked = { stage ->
                    currentStage = stage
                    questionCount = 1
                    correctCount = 0
                    // Load nouns logic would go here
                    // For demo, we assume data is loaded
                    currentScreen = Screen.GAME
                }
            )
        }
        Screen.GAME -> {
            // NOTE: In a real app, you would hold the NounList in a ViewModel
            // This is a placeholder for the UI logic
            GameScreen(
                questionNum = "$questionCount / $questionsPerStage",
                question = currentQuestion ?: Question("Test", "عربي", "Das ist...", "Nom", "das", listOf("der","die","das"), listOf("A","B","C")), 
                onAnswer = { selectedArt, selectedMean ->
                    val q = currentQuestion!!
                    val isCorrect = (selectedArt == q.correctArticle && selectedMean == q.meaning)
                    
                    if (isCorrect) {
                        correctCount++
                        resultMessage = "✅ Richtig!"
                        // Logic to next question
                    } else {
                        resultMessage = "❌ Falsch"
                        lastExplanation = "Wort: ${q.noun}\nBedeutung: ${q.meaning}\nRichtig: ${q.correctArticle}"
                        currentScreen = Screen.RESULT
                    }
                }
            )
        }
        Screen.RESULT -> {
            ResultScreen(
                explanation = lastExplanation,
                onNext = {
                    if (questionCount >= questionsPerStage) {
                        currentScreen = Screen.STAGE_SELECT
                    } else {
                        questionCount++
                        // generateQuestion() would be called here
                        currentScreen = Screen.GAME
                    }
                }
            )
        }
    }
}

// --- UI COMPONENTS (Equivalent to your KV file) ---

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun StageSelectScreen(unlockedStages: Int, onStageClicked: (Int) -> Unit) {
    Scaffold(
        topBar = { CenterAlignedTopAppBar(title = { Text("Artikel Lernen (العربية)") }) }
    ) { padding ->
        LazyVerticalGrid(
            columns = GridCells.Fixed(3),
            contentPadding = PaddingValues(16.dp),
            modifier = Modifier.padding(padding)
        ) {
            items(100) { index ->
                val stageNum = index + 1
                val isLocked = stageNum > unlockedStages
                Button(
                    onClick = { onStageClicked(stageNum) },
                    enabled = !isLocked,
                    modifier = Modifier.padding(4.dp),
                    colors = ButtonDefaults.buttonColors(
                        containerColor = if (isLocked) Color.Gray else Color(0xFF2196F3)
                    )
                ) {
                    Text(text = "$stageNum")
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun GameScreen(
    questionNum: String, 
    question: Question, 
    onAnswer: (String, String) -> Unit
) {
    var selectedArticle by remember { mutableStateOf("") }
    var selectedMeaning by remember { mutableStateOf("") }

    Scaffold(
        topBar = { CenterAlignedTopAppBar(title = { Text(questionNum) }) }
    ) { padding ->
        Column(
            modifier = Modifier
                .padding(padding)
                .fillMaxSize()
                .padding(16.dp)
                .verticalScroll(rememberScrollState()), // Makes it scrollable like MDScrollView
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // Sentence
            Text(
                text = question.sentence,
                style = MaterialTheme.typography.headlineSmall,
                textAlign = TextAlign.Center
            )

            // Article Buttons
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                question.articleOptions.forEach { article ->
                    Button(
                        onClick = { selectedArticle = article },
                        colors = ButtonDefaults.buttonColors(
                            containerColor = if (selectedArticle == article) Color(0xFF3F51B5) else Color(0xFF2196F3)
                        ),
                        modifier = Modifier.weight(1f)
                    ) {
                        Text(article)
                    }
                }
            }

            Text("Bedeutung:", style = MaterialTheme.typography.titleMedium)

            // Meaning Buttons (Arabic works automatically here!)
            question.meaningOptions.forEach { meaning ->
                Button(
                    onClick = { selectedMeaning = meaning },
                    colors = ButtonDefaults.buttonColors(
                        containerColor = if (selectedMeaning == meaning) Color(0xFF3F51B5) else Color(0xFF2196F3)
                    ),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text(text = meaning, fontSize = 20.sp) // Auto-RTL support
                }
            }

            Spacer(modifier = Modifier.height(20.dp))

            // Check Button
            Button(
                onClick = { onAnswer(selectedArticle, selectedMeaning) },
                enabled = selectedArticle.isNotEmpty() && selectedMeaning.isNotEmpty(),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF4CAF50)),
                modifier = Modifier.fillMaxWidth().height(50.dp)
            ) {
                Text("PRÜFEN")
            }
        }
    }
}

@Composable
fun ResultScreen(explanation: String, onNext: () -> Unit) {
    Column(
        modifier = Modifier.fillMaxSize().padding(30.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("Erklärung", style = MaterialTheme.typography.headlineMedium)
        Spacer(modifier = Modifier.height(20.dp))
        
        // This text will render Arabic correctly mixed with German
        Text(
            text = explanation,
            style = MaterialTheme.typography.bodyLarge,
            textAlign = TextAlign.Center
        )
        
        Spacer(modifier = Modifier.height(40.dp))
        
        Button(onClick = onNext, modifier = Modifier.fillMaxWidth()) {
            Text("Weiter")
        }
    }
}
