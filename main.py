from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import pickle
import pandas as pd

app = FastAPI()

# Load the trained model
with open('best_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>Sentiment Prediction</title>
            <style>
                /* Center align content */
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .container {
                    text-align: center;
                    max-width: 600px; /* Adjust as needed */
                    margin: auto; /* Center align container */
                }
                .prediction-section {
                    margin-top: 30px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Sentiment Prediction</h1>
                <form action="/predict" method="post" id="predict-form">
                    <label for="review">Enter your review:</label><br>
                    <textarea id="review" name="review" rows="4" cols="50"></textarea><br><br>
                    <input type="submit" value="Predict">
                </form>
                
                <div class="prediction-section" id="prediction">
                    <!-- Prediction result will be inserted here -->
                </div>

                <!-- Bookmarks/Anchors -->
                <p><a href="https://www.linkedin.com/in/rahul-kumar-1b2b0613b" target="_blank">#creator profile</a> | <a href="https://www.geeksforgeeks.org/getting-started-with-classification/" target="_blank">#Machine learning in NLP</a> | <a href="https://colab.research.google.com/drive/15vCkKnWOoTANLmMPHAjqwL3GJ7SVgiJz?usp=sharing" target="_blank">#project_code_file</a></p>

                <!-- Detailed information -->
                <h2 id="creator">Creator Name: Rahul Kumar</h2>
                <p>Methods Applied: NLP (Natural Language Processing)</p>
                <p>Project Name: Sentiment Prediction using Machine Learning Algorithms</p>

                <script>
                    document.getElementById("predict-form").addEventListener("submit", function(event) {
                        event.preventDefault(); // Prevent form submission

                        var formData = new FormData(event.target);
                        fetch('/predict', {
                            method: 'POST',
                            body: formData
                        })
                        .then(response => response.text())
                        .then(data => {
                            document.getElementById("prediction").innerHTML = data;
                            // Optional: Scroll to prediction section after displaying
                            document.getElementById("prediction").scrollIntoView({ behavior: 'smooth' });

                            setTimeout(function() {
                                location.reload(); // Refresh the page after displaying the prediction
                            }, 3000); // Adjust the timeout (in milliseconds) as needed
                        })
                        .catch(error => {
                            console.error('Error:', error);
                        });
                    });
                </script>
            </div>
        </body>
    </html>
    """

@app.post("/predict", response_class=HTMLResponse)
async def predict(review: str = Form(...)):
    review_series = pd.Series([review])
    prediction = model.predict(review_series)
    return f"""
    <h2>Prediction: {prediction[0]}</h2>
    """
