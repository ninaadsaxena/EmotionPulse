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
    const sent
