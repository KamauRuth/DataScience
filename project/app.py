from flask import Flask, request, jsonify, render_template_string
from transformers import BertTokenizer, BertForSequenceClassification
import torch

app = Flask(__name__)

# Load tokenizer and model
tokenizer = BertTokenizer.from_pretrained('./model')
model = BertForSequenceClassification.from_pretrained('./model')
model.eval()

# HTML + JavaScript interface
html_template = '''
<!doctype html>
<html lang="en">
<head>
    <title>Phishing Email Detector</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding-top: 50px;
        }
        textarea {
            width: 60%;
            height: 200px;
            font-size: 16px;
            padding: 10px;
        }
        #result {
            margin-top: 20px;
            font-size: 20px;
            font-weight: bold;
        }
        button {
            padding: 10px 30px;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <h1>Phishing Email Detector</h1>
    <textarea id="text-input" placeholder="Paste email content here..."></textarea><br><br>
    <button onclick="detectPhishing()">Detect</button>
    <div id="result"></div>

    <script>
        async function detectPhishing() {
            const text = document.getElementById('text-input').value;
            const resultDiv = document.getElementById('result');

            if (!text) {
                resultDiv.textContent = 'Please enter some text.';
                return;
            }

            resultDiv.textContent = 'Detecting...';

            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });

            const data = await response.json();
            resultDiv.textContent = 'Prediction: ' + data.prediction;
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(html_template)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data.get('text')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Tokenize and predict
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        pred = torch.argmax(logits, dim=1).item()

    label = "Phishing" if pred == 1 else "Legit"
    return jsonify({'prediction': label})

if __name__ == '__main__':
    app.run(debug=True)
