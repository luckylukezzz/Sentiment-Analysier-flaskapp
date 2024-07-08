from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Welcome to the Analytics API. Use the /analytics endpoint to POST your data.'
    })


@app.route('/analytics', methods=['POST'])
def analytics():
    # Get JSON data from the request
    data = request.get_json()
    
    # Simple analytics logic: calculate the sum and average of a list of numbers
    numbers = data.get('numbers', [])
    if not numbers:
        return jsonify({'error': 'No numbers provided'}), 400
    
    total = sum(numbers)
    average = total / len(numbers)
    
    # Return the results as JSON
    return jsonify({
        'total': total,
        'average': average
    })

if __name__ == '__main__':
    app.run(debug=True)
