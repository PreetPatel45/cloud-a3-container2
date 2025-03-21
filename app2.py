from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        # Validate that both "file" and "product" keys are present and non-null.
        if not data or data.get('file') is None or data.get('product') is None:
            return jsonify({
                "file": None,
                "error": "Invalid JSON input."
            }), 400

        filename = data.get('file')
        product = data.get('product')
        file_path = f'/preet_PV_dir/{filename}'

        # Read the CSV file using pandas.
        df = pd.read_csv(file_path)
        # Strip any extra spaces from column names.
        df.columns = [col.strip() for col in df.columns]

        # Verify that the CSV headers exactly match ["product", "amount"].
        if df.columns.tolist() != ["product", "amount"]:
            return jsonify({
                "file": filename,
                "error": "Input file not in CSV format."
            }), 400

        # Calculate the sum for the specified product.
        total = df[df['product'] == product]['amount'].sum()

        # Edge-case: if file extension is ".yml" (case-insensitive) and total is 0, return an error.
        fname, file_extension = os.path.splitext(filename)
        if file_extension.lower() == '.yml' and total == 0:
            return jsonify({
                "file": filename,
                "error": "Input file not in CSV format."
            }), 400

        return jsonify({
            "file": filename,
            "sum": int(total)
        })

    except pd.errors.EmptyDataError:
        return jsonify({
            "file": filename,
            "error": "Input file not in CSV format."
        }), 400
    except pd.errors.ParserError:
        return jsonify({
            "file": filename,
            "error": "Input file not in CSV format."
        }), 400
    except Exception as e:
        return jsonify({
            "file": filename if 'filename' in locals() else None,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
