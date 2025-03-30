// Global variables
let textChart = null;
let imageChart = null;
let selectedImageData = null;

// DOM elements
const textInput = document.getElementById('textInput');
const analyzeTextBtn = document.getElementById('analyzeTextBtn');
const textResults = document.getElementById('textResults');

const imageInput = document.getElementById('imageInput');
const analyzeImageBtn = document.getElementById('analyzeImageBtn');
const imageResults = document.getElementById('imageResults');
const selectedImage = document.getElementById('selectedImage');
const sampleImages = document.querySelectorAll('.sample-image');

// New DOM elements for training and evaluation
const trainModelBtn = document.getElementById('trainModelBtn');
const evaluateModelBtn = document.getElementById('evaluateModelBtn');
const trainResultsDiv = document.getElementById('trainResults');
const evaluateResultsDiv = document.getElementById('evaluateResults');

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Text analysis
    analyzeTextBtn.addEventListener('click', analyzeText);
    textInput.addEventListener('input', () => {
        analyzeTextBtn.disabled = !textInput.value.trim();
    });
    
    // Image analysis
    imageInput.addEventListener('change', handleImageSelection);
    analyzeImageBtn.addEventListener('click', analyzeImage);
    
    // Sample images
    sampleImages.forEach(img => {
        img.addEventListener('click', () => {
            loadSampleImage(img.src);
        });
    });

    // Model training and evaluation
    trainModelBtn.addEventListener('click', trainModel);
    evaluateModelBtn.addEventListener('click', evaluateModel);
});

// Text analysis functions
async function analyzeText() {
    const text = textInput.value.trim();
    if (!text) return;
    
    // Show loading state
    analyzeTextBtn.disabled = true;
    analyzeTextBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Analyzing...';
    
    try {
        const response = await fetch('/analyze/text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        });
        
        const result = await response.json();
        
        if (result.error) {
            alert('Error: ' + result.error);
            return;
        }
        
        displayTextResults(result);
    } catch (error) {
        console.error('Error analyzing text:', error);
        alert('An error occurred while analyzing the text.');
    } finally {
        // Reset button
        analyzeTextBtn.disabled = false;
        analyzeTextBtn.innerHTML = '<i class="fas fa-search"></i> Analyze Text';
    }
}

function displayTextResults(result) {
    // Show results container
    textResults.classList.remove('d-none');
    
    // Display sentiment
    const sentimentLabel = document.getElementById('sentimentLabel');
    const sentimentScoreBar = document.getElementById('sentimentScore');

    sentimentLabel.textContent = result.sentiment.label;
    sentimentScoreBar.style.width = `${result.sentiment.score * 100}%`;
}

// Image analysis functions
function handleImageSelection(event) {
    const file = event.target.files[0];
    
    if (file) {
        const reader = new FileReader();
        reader.onloadend = () => {
            selectedImageData = reader.result;
            selectedImage.src = selectedImageData;
            analyzeImageBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    }
}

async function analyzeImage() {
    if (!selectedImageData) return;

    // Show loading state
    analyzeImageBtn.disabled = true;
    analyzeImageBtn.innerHTML =
        '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Analyzing...';

    try {
        const response = await fetch('/analyze/image', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: selectedImageData }),
        });

        const result = await response.json();

        if (result.error) {
            alert('Error: ' + result.error);
            return;
        }

        displayImageResults(result);
    } catch (error) {
        console.error('Error analyzing image:', error);
        alert('An error occurred while analyzing the image.');
    } finally {
        // Reset button
        analyzeImageBtn.disabled = false;
        analyzeImageBtn.innerHTML =
            '<i class="fas fa-search"></i> Analyze Image';
    }
}

function displayImageResults(result) {
    // Show results container
    imageResults.classList.remove('d-none');

    // Display dominant emotion
    const imageEmotionLabel = document.getElementById("imageEmotionLabel");
    const imageEmotionScoreBar = document.getElementById("imageEmotionScore");

    imageEmotionLabel.textContent =
        result.dominant_emotion.label + " (" + (result.dominant_emotion.score * 100).toFixed(2) + "%)";
    
    imageEmotionScoreBar.style.width =
        `${result.dominant_emotion.score * 100}%`;
}

// Model training functions
async function trainModel() {
    trainResultsDiv.innerHTML =
        "<p>Training in progress... This may take a few minutes.</p>";

    try {
        const response = await fetch("/train-model", { method: "POST" });
        const data = await response.json();

        if (data.error) {
            trainResultsDiv.innerHTML =
                `<p>Error occurred while training the model: ${data.error}</p>`;
            return;
        }

        trainResultsDiv.innerHTML =
            `<p>Training completed successfully! Training history:</p>
             <pre>${JSON.stringify(data.history, null, 2)}</pre>`;
        
        alert("Model training completed successfully!");
    } catch (error) {
        console.error("Error training model:", error);
        trainResultsDiv.innerHTML =
            `<p>An error occurred during training. Please check the logs.</p>`;
    }
}

// Model evaluation functions
async function evaluateModel() {
    evaluateResultsDiv.innerHTML =
        "<p>Evaluating model... Please wait.</p>";

    try {
        const response = await fetch("/evaluate-model", { method: "POST" });
        const data = await response.json();

        if (data.error) {
            evaluateResultsDiv.innerHTML =
                `<p>Error occurred while evaluating the model: ${data.error}</p>`;
            return;
        }

        evaluateResultsDiv.innerHTML =
            `<p>Evaluation completed successfully! Metrics:</p>
             <pre>${JSON.stringify(data.metrics, null, 2)}</pre>`;
        
        alert("Model evaluation completed successfully!");
    } catch (error) {
        console.error("Error evaluating model:", error);
        evaluateResultsDiv.innerHTML =
            `<p>An error occurred during evaluation. Please check the logs.</p>`;
    }
}
