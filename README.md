# EmotionPulse

EmotionPulse is an advanced web application designed to analyze and visualize emotions from text inputs using state-of-the-art Natural Language Processing (NLP) techniques. This project leverages HTML, Python, JavaScript, and CSS to provide real-time emotion analysis and visualization, making it an indispensable tool for researchers, psychologists, and developers interested in sentiment analysis.

## Features

- **Emotion Analysis**: Detect and analyze the emotions conveyed in text inputs.
- **Real-Time Processing**: Provides instant feedback and visualization of emotions.
- **Interactive Visualization**: Visualize the analysis results in an engaging and user-friendly interface.
- **Multi-language Support**: Analyze text in multiple languages.
- **Extensible**: Easily extendable with additional NLP models and visualization tools.

## Technologies Used

EmotionPulse is built using a variety of modern technologies:

- **HTML**: For structuring the web pages.
- **CSS**: For styling and layout.
- **JavaScript**: For client-side scripting and interactive features.
- **Python**: For backend processing and NLP tasks.
- **NLP Libraries**: Leveraging libraries like NLTK, SpaCy, and TextBlob for emotion analysis.
- **Visualization Libraries**: Using D3.js and Chart.js for creating dynamic and interactive visualizations.

## Prerequisites

Ensure you have the following installed on your system:

- **Python 3.7 or higher**
- **Node.js and npm**

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/ninaadsaxena/EmotionPulse.git
   cd EmotionPulse
   ```

2. Install the Python dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Install the JavaScript dependencies:
   ```sh
   npm install
   ```

4. Start the development server:
   ```sh
   npm start
   ```

## How It Works

1. The application uses NLP libraries to analyze the text input.
2. Custom logic processes the text to classify emotions based on the content.
3. The recognized emotions are visualized in an interactive and user-friendly interface.

### Supported Emotions

1. **Happiness**: Positive and uplifting emotions.
2. **Sadness**: Negative and downhearted emotions.
3. **Anger**: Strong feelings of displeasure or hostility.
4. **Fear**: An unpleasant emotion caused by the threat of danger or harm.
5. **Surprise**: A feeling of shock or astonishment.
6. **Disgust**: A feeling of revulsion or strong disapproval.

## Usage

1. Open your browser and navigate to `http://localhost:3000`.
2. Enter the text you want to analyze in the input field.
3. View the emotion analysis results and visualizations.

## Development Environment

- **Code Editor**: Visual Studio Code
- **Languages**: HTML, CSS, JavaScript, Python

## Customization

- **Add New Emotions**: Modify the `analyze_emotion` method to define new emotion conditions based on text analysis.
- **Change Visualization Style**: Adjust the D3.js or Chart.js configurations for your desired visualization style.

## Example Output

- **Happiness**: Displays "Detected Emotion: Happiness" with a corresponding visualization.
- **Sadness**: Displays "Detected Emotion: Sadness" with a corresponding visualization.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request. For significant changes, please open an issue first to discuss your ideas.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

- [NLTK](https://www.nltk.org/) for providing powerful NLP tools.
- [SpaCy](https://spacy.io/) for efficient text processing.
- [Chart.js](https://www.chartjs.org/) and [D3.js](https://d3js.org/) for interactive visualizations.

## Author

Developed by **Ninaad Saxena**. Feel free to connect on [LinkedIn](https://www.linkedin.com/in/ninaadsaxena/).

---
