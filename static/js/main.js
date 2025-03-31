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
    console.log('DOM fully loaded');
    
    // Text analysis
    if (analyzeTextBtn) {
        analyzeTextBtn.addEventListener('click', analyzeText);
        textInput.addEventListener('input', () => {
            analyzeTextBtn.disabled = !textInput.value.trim();
        });
    }
    
    // Image analysis
    if (imageInput) {
        imageInput.addEventListener('change', handleImageSelection);
    }
    
    if (analyzeImageBtn) {
        analyzeImageBtn.addEventListener('click', analyzeImage);
    }
    
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
        analyzeTextBtn.innerHTML = '<span class="button-text"><i class="fas fa-search"></i> Analyze Text</span><span class="button-icon"><i class="fas fa-arrow-right"></i></span>';
    }
}

function displayTextResults(result) {
    // Show results container
    textResults.classList.remove('d-none');
    
    // Display sentiment
    const sentimentLabel = document.getElementById('sentimentLabel');
    const sentimentScore = document.getElementById('sentimentScore');
    const sentimentIcon = document.getElementById('sentimentIcon');
    
    sentimentLabel.textContent = result.sentiment.label;
    sentimentScore.style.width = `${result.sentiment.score * 100}%`;
    
    // Set sentiment icon
    if (result.sentiment.label === 'POSITIVE') {
        sentimentIcon.innerHTML = '<i class="fas fa-smile text-success"></i>';
    } else {
        sentimentIcon.innerHTML = '<i class="fas fa-frown text-danger"></i>';
    }
    
    // Display dominant emotion
    const emotionLabel = document.getElementById('emotionLabel');
    const emotionScore = document.getElementById('emotionScore');
    const emotionIcon = document.getElementById('emotionIcon');
    
    emotionLabel.textContent = `${result.dominant_emotion.label} (${(result.dominant_emotion.score * 100).toFixed(2)}%)`;
    emotionScore.style.width = `${result.dominant_emotion.score * 100}%`;
    
    // Set emotion icon
    setEmotionIcon(emotionIcon, result.dominant_emotion.label);
    
    // Create emotion chart
    createEmotionChart(result.emotions);
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

function loadSampleImage(src) {
    fetch(src)
        .then(response => response.blob())
        .then(blob => {
            const reader = new FileReader();
            reader.onloadend = () => {
                selectedImageData = reader.result;
                selectedImage.src = selectedImageData;
                analyzeImageBtn.disabled = false;
            };
            reader.readAsDataURL(blob);
        })
        .catch(error => {
            console.error('Error loading sample image:', error);
        });
}

async function analyzeImage() {
    if (!selectedImageData) return;

    // Show loading state
    analyzeImageBtn.disabled = true;
    analyzeImageBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Analyzing...';

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
        analyzeImageBtn.innerHTML = '<span class="button-text"><i class="fas fa-search"></i> Analyze Image</span><span class="button-icon"><i class="fas fa-arrow-right"></i></span>';
    }
}

// Function to display image analysis results with fixed percentage calculations
function displayImageResults(result) {
    // Show results container
    imageResults.classList.remove('d-none');

    // Display dominant emotion with proper percentage formatting
    const imageEmotionLabel = document.getElementById("imageEmotionLabel");
    const imageEmotionScoreBar = document.getElementById("imageEmotionScore");
    const imageEmotionIcon = document.getElementById("imageEmotionIcon");

    // Validate and safely convert the score to percentage
    let score = 0;
    if (result.dominant_emotion && typeof result.dominant_emotion.score === 'number') {
        // Ensure score is between 0 and 1 before converting to percentage
        score = Math.max(0, Math.min(1, result.dominant_emotion.score));
    }
    
    // Format percentage with 2 decimal places
    const formattedScore = (score * 100).toFixed(2);
    
    // Update DOM elements
    imageEmotionLabel.textContent = `${result.dominant_emotion.label} (${formattedScore}%)`;
    imageEmotionScoreBar.style.width = `${score * 100}%`;
    
    // Set appropriate icon based on emotion
    setEmotionIcon(imageEmotionIcon, result.dominant_emotion.label);
    
    // Create emotion breakdown chart with validated data
    createImageEmotionChart(result.emotions);
}

// Function to create emotion breakdown chart with proper data validation
function createImageEmotionChart(emotions) {
    const ctx = document.getElementById('imageEmotionsChart').getContext('2d');
    
    // Destroy previous chart if it exists
    if (window.imageChart) {
        window.imageChart.destroy();
    }
    
    // Validate emotions data
    if (!emotions || typeof emotions !== 'object') {
        console.error("Invalid emotions data:", emotions);
        return;
    }
    
    // Prepare data for chart with validation
    const labels = Object.keys(emotions);
    const data = [];
    
    // Process each emotion value with proper validation
    for (const emotion of labels) {
        let value = emotions[emotion];
        
        // Convert to number if it's not already
        if (typeof value !== 'number') {
            value = parseFloat(value);
        }
        
        // Validate the value is a number and in proper range
        if (isNaN(value)) {
            value = 0;
        } else {
            // Ensure value is between 0 and 1
            value = Math.max(0, Math.min(1, value));
        }
        
        // Convert to percentage for display
        data.push(value * 100);
    }
    
    // Create color array based on emotions
    const backgroundColors = labels.map(emotion => {
        switch(emotion.toLowerCase()) {
            case 'happy': return '#4cc9f0';
            case 'sad': return '#3a0ca3';
            case 'angry': return '#f72585';
            case 'fear': return '#7209b7';
            case 'surprise': return '#4361ee';
            case 'neutral': return '#4895ef';
            case 'disgust': return '#560bad';
            default: return '#4895ef';
        }
    });
    
    // Create new chart with validated data
    window.imageChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Emotion Intensity (%)',
                data: data,
                backgroundColor: backgroundColors,
                borderColor: 'rgba(0, 0, 0, 0.1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Percentage (%)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.raw.toFixed(2)}%`;
                        }
                    }
                }
            }
        }
    });
}


function createImageEmotionChart(emotions) {
    const ctx = document.getElementById('imageEmotionsChart').getContext('2d');
    
    // Destroy previous chart if it exists
    if (imageChart) {
        imageChart.destroy();
    }
    
    // Ensure emotions is not null or undefined
    if (!emotions) {
        console.error("No emotion data available");
        return;
    }
    
    // Prepare data for chart
    const labels = Object.keys(emotions);
    const data = [];
    
    // Safely convert values to percentages, handling any non-numeric values
    for (const key of labels) {
        const value = emotions[key];
        if (typeof value === 'number') {
            data.push((value * 100).toFixed(2));
        } else if (typeof value === 'string') {
            const parsed = parseFloat(value);
            data.push(isNaN(parsed) ? 0 : (parsed * 100).toFixed(2));
        } else {
            data.push(0);
        }
    }
    
    // Create color array based on emotions
    const backgroundColors = labels.map(emotion => {
        switch(emotion.toLowerCase()) {
            case 'happy': return '#4cc9f0';
            case 'sad': return '#3a0ca3';
            case 'angry': return '#f72585';
            case 'fear': return '#7209b7';
            case 'surprise': return '#4361ee';
            case 'neutral': return '#4895ef';
            case 'disgust': return '#560bad';
            default: return '#4895ef';
        }
    });
    
    try {
        // Create new chart with error handling
        imageChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Emotion Intensity (%)',
                    data: data,
                    backgroundColor: backgroundColors,
                    borderColor: 'rgba(0, 0, 0, 0.1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Percentage (%)'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.raw}%`;
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error("Error creating emotion chart:", error);
    }
}


// Helper function to set emotion icons
function setEmotionIcon(iconElement, emotion) {
    iconElement.className = 'result-icon me-2 fs-3';
    
    switch(emotion.toLowerCase()) {
        case 'happy':
            iconElement.innerHTML = '<i class="fas fa-smile text-primary"></i>';
            break;
        case 'sad':
            iconElement.innerHTML = '<i class="fas fa-frown text-primary"></i>';
            break;
        case 'angry':
            iconElement.innerHTML = '<i class="fas fa-angry text-danger"></i>';
            break;
        case 'fear':
            iconElement.innerHTML = '<i class="fas fa-grimace text-warning"></i>';
            break;
        case 'surprise':
            iconElement.innerHTML = '<i class="fas fa-surprise text-info"></i>';
            break;
        case 'neutral':
            iconElement.innerHTML = '<i class="fas fa-meh text-secondary"></i>';
            break;
        case 'disgust':
            iconElement.innerHTML = '<i class="fas fa-dizzy text-success"></i>';
            break;
        default:
            iconElement.innerHTML = '<i class="fas fa-question-circle"></i>';
    }
}

// Helper function to get emotion colors
function getEmotionColors(emotions) {
    return emotions.map(emotion => {
        switch(emotion.toLowerCase()) {
            case 'happy': return '#4cc9f0';
            case 'sad': return '#3a0ca3';
            case 'angry': return '#f72585';
            case 'fear': return '#7209b7';
            case 'surprise': return '#4361ee';
            case 'neutral': return '#4895ef';
            case 'disgust': return '#560bad';
            default: return '#4895ef';
        }
    });
}
