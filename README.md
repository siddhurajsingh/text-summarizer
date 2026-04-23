# 📝 AI Text Summarizer

A powerful, user-friendly web application for summarizing text using advanced NLP techniques.

## Features

- ✨ **Instant Summarization** - Convert long texts into concise summaries
- 🎨 **Beautiful UI** - Modern, gradient-based Streamlit interface
- 📊 **Advanced Analytics** - Word count, character count, compression ratio analysis
- 📥 **Export Options** - Download summaries as text files
- 📚 **Example Texts** - Pre-loaded examples for quick testing
- ⚙️ **Customizable** - Adjust summary length with simple slider

## Installation

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/siddhurajsingh/text-summarizer.git
cd text-summarizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
python -m streamlit run app.py
```

The app will open at `http://localhost:8501`

## Usage

1. **Choose Input Method:**
   - Paste your text directly in the "Text Input" tab
   - Or select a pre-loaded example from the "Examples" tab

2. **Adjust Settings:**
   - Use the sidebar slider to set the number of sentences in the summary
   - Range: 1-10 sentences

3. **Generate Summary:**
   - Click the "✨ Generate Summary" button
   - View results with detailed analytics

4. **Export:**
   - Download the summary or full report as a text file

## How It Works

The summarizer uses **Extractive Text Summarization** powered by:
- **NLTK (Natural Language Toolkit)** - For tokenization and text processing
- **Word Frequency Analysis** - To identify important sentences
- **Sentence Scoring** - Ranks sentences based on keyword importance

### Algorithm Steps:
1. Tokenize text into sentences
2. Remove stopwords and filter punctuation
3. Calculate word frequencies
4. Score sentences based on word frequency
5. Select top-ranked sentences while preserving order
6. Return summary

## Requirements

- Python 3.8+
- streamlit==1.28.1
- nltk==3.8.1

## File Structure

```
text-summarizer/
├── app.py                    # Main Streamlit application
├── text_summarisation.py     # Core summarization logic (CLI version)
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Deployed Version

Access the live application at:
🚀 [Streamlit Cloud Deployment](https://text-summarizer.streamlit.app)

## Technologies Used

- **Frontend:** Streamlit
- **NLP:** NLTK (Natural Language Toolkit)
- **Language:** Python 3
- **Hosting:** Streamlit Cloud

## Future Enhancements

- [ ] Support for multiple languages
- [ ] GPU-accelerated transformer models (BART, T5)
- [ ] PDF/Document upload support
- [ ] Abstract summarization (AI-generated summaries)
- [ ] User authentication and saved summaries
- [ ] API endpoints for integration
- [ ] Batch processing of multiple files

## Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Author

**Siddhu Raj Singh** - [GitHub](https://github.com/siddhurajsingh)

## Support

For issues, questions, or suggestions, please [open an issue](https://github.com/siddhurajsingh/text-summarizer/issues) on GitHub.

---

**Made with ❤️ using Streamlit & NLTK**
