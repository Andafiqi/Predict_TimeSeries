from flask import Flask, request, render_template_string, jsonify
import pickle
import streamlit

app = Flask(__name__)

# Load the trained model
model = pickle.load(open('modelrf1.pkl', 'rb'))

def predict(year):
    year = int(year)
    prediction = model.predict([[year]])
    return {
        'Schizophrenia_disorders': prediction[0][0],
        'Depressive_disorders': prediction[0][1],
        'Anxiety_disorders': prediction[0][2],
        'Bipolar_disorders': prediction[0][3],
        'Eating_disorders': prediction[0][4]
    }

@app.route('/predict', methods=['POST'])
def predict_view():
    year = request.form['Year']
    try:
        prediction = predict(year)
        return jsonify(prediction)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Prediksi Time Series</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-size: cover;
                margin: 0;
                font-family: Arial, sans-serif;
            }
            .container {
                background-color: rgba(255, 255, 255, 0.8);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
                padding: 8px;
                text-align: left;
            }
            table {
                width: 100%;
                margin-top: 20px;
            }
            form {
                margin-bottom: 20px;
            }
        </style>
        <script>
            function resetForm() {
                document.getElementById('prediction-results').innerHTML = '';
            }

            function submitForm(event) {
                event.preventDefault();
                const form = event.target;
                const formData = new FormData(form);
                fetch('/predict', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    const resultsDiv = document.getElementById('prediction-results');
                    if (data.error) {
                        resultsDiv.innerHTML = `<h2 style="color: red;">${data.error}</h2>`;
                    } else {
                        resultsDiv.innerHTML = `
                            <h2>Hasil Prediksi:</h2>
                            <table>
                                <tr>
                                    <th>Disorder</th>
                                    <th>Prediction</th>
                                </tr>
                                <tr>
                                    <td>Schizophrenia disorders</td>
                                    <td>${data.Schizophrenia_disorders}</td>
                                </tr>
                                <tr>
                                    <td>Depressive disorders</td>
                                    <td>${data.Depressive_disorders}</td>
                                </tr>
                                <tr>
                                    <td>Anxiety disorders</td>
                                    <td>${data.Anxiety_disorders}</td>
                                </tr>
                                <tr>
                                    <td>Bipolar disorders</td>
                                    <td>${data.Bipolar_disorders}</td>
                                </tr>
                                <tr>
                                    <td>Eating disorders</td>
                                    <td>${data.Eating_disorders}</td>
                                </tr>
                            </table>
                        `;
                    }
                })
                .catch(error => {
                    const resultsDiv = document.getElementById('prediction-results');
                    resultsDiv.innerHTML = `<h2 style="color: red;">${error.message}</h2>`;
                });
            }
        </script>
    </head>
    <body>
        <div class="container">
            <h1>Prediksi Time Series</h1>
            <form method="post" action="/predict" onsubmit="submitForm(event)" onreset="resetForm()">
                <label for="Year">Masukkan Tahun:</label><br>
                <input type="text" id="Year" name="Year" required><br><br>
                <input type="submit" value="Prediksi">
                <input type="reset" value="Reset">
            </form>

            <div id="prediction-results"></div>
        </div>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=4445)

