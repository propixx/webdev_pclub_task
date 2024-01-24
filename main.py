from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Load your Excel data into a DataFrame
excel_data = pd.read_excel('studentsearch.xlsx', sheet_name='Sheet1')

@app.route('/')
def home():
    return "Welcome to the Excel API!"

@app.route('/api/excel_data', methods=['GET'])
def get_excel_data():
    # Convert DataFrame to JSON for the ultimate data freedom!
    json_data = excel_data.to_json(orient='records')
    return jsonify(json_data)

@app.route('/api/group/<string:group_name>', methods=['GET'])
def get_group_data(group_name):
    # Filter data based on the requested group
    group_data = excel_data[excel_data['w'] == group_name]
    
    if group_data.empty:
        return jsonify({"message": f"No names found under the group '{group_name}'"}), 404
    
    # Extract the 'Name' column from the filtered DataFrame
    names = group_data['n'].tolist()
    return jsonify({"group": group_name, "names": names})

@app.route('/api/WingiesOrNot', methods=['POST'])
def WingiesOrNot():
    try:
        # Get names from the request
        
        roll1 = request.args.get('roll1')
        roll2 = request.args.get('roll2')

        # Check if names are in the same group
        group_roll1 = excel_data.loc[excel_data['i'] == roll1, 'w'].iloc[0]
        group_roll2 = excel_data.loc[excel_data['i'] == roll2, 'w'].iloc[0]

        result = {"roll1": roll1, "roll2": roll2, "in same wing": group_roll1 == group_roll2}
        return jsonify(result)
    except Exception as e:
        return jsonify({"not in same wing": str(e)}), 400
    
def find_roommates(roll_number):
    student = excel_data[excel_data['i'] == roll_number]
    if not student.empty:
        roommates = excel_data[(excel_data['w'] == student['w'].iloc[0]) & (excel_data['i'] != roll_number)]
        return roommates.to_dict(orient='records')
    return None


@app.route('/api/students', methods=['GET'])
def get_students():
    return jsonify(excel_data.to_dict(orient='records'))

@app.route('/api/find_roommates', methods=['GET'])
def get_roommates():
    try:
        roll_number = int(request.args.get('roll_number'))
        roommates = find_roommates(roll_number)
        if roommates:
            return jsonify({"roommates": roommates})
        return jsonify({"message": f"No roommates found for roll number {roll_number}"}), 404
    except ValueError:
        return jsonify({"error": "Invalid roll number"}), 400    

if __name__ == '__main__':
    app.run(debug=True)
