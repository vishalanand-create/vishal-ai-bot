from flask import Flask, request, jsonify
import pandas as pd
import io
import os

app = Flask(__name__)

# Import report_skill from skills module
try:
    from skills.core_skills import report_skill
except ImportError:
    report_skill = None

@app.route('/chat', methods=['POST'])
def chat():
    """
    Chat endpoint to interact with Agent Vish.
    Expects JSON with 'message' field and returns bot response.
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate input
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Missing required field: message'
            }), 400
        
        user_message = data['message']
        
        # TODO: Replace this with actual Agent Vish logic
        # For now, this is a simple echo response
        bot_response = f"Agent Vish received: {user_message}"
        
        # Return bot response as JSON
        return jsonify({
            'status': 'success',
            'message': user_message,
            'response': bot_response
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/summarize_report', methods=['POST'])
def summarize_report():
    """
    API endpoint to summarize uploaded CSV/Excel reports.
    
    Accepts:
        - file: CSV or Excel file (multipart/form-data)
        - Optional parameters in form data
    
    Returns:
        JSON object containing:
        - summary: Statistical summary of the data
        - recommendations: AI-generated recommendations based on data analysis
        - status: success or error
    
    Example Usage:
        curl -X POST http://localhost:5000/api/summarize_report \
             -F "file=@report.csv"
    
    Response Format:
        {
            "status": "success",
            "summary": {
                "total_rows": 100,
                "total_columns": 5,
                "column_info": {...},
                "statistics": {...}
            },
            "recommendations": [
                "Recommendation 1",
                "Recommendation 2"
            ]
        }
    """
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            return jsonify({
                'status': 'error',
                'error': 'No file provided. Please upload a CSV or Excel file.'
            }), 400
        
        file = request.files['file']
        
        # Check if filename is empty
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'error': 'No file selected'
            }), 400
        
        # Get file extension
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        # Read file based on extension
        try:
            file_content = file.read()
            file_stream = io.BytesIO(file_content)
            
            if file_extension == '.csv':
                df = pd.read_csv(file_stream)
            elif file_extension in ['.xlsx', '.xls']:
                df = pd.read_excel(file_stream)
            else:
                return jsonify({
                    'status': 'error',
                    'error': f'Unsupported file format: {file_extension}. Please upload CSV or Excel files.'
                }), 400
        except Exception as e:
            return jsonify({
                'status': 'error',
                'error': f'Error reading file: {str(e)}'
            }), 400
        
        # Process with report_skill if available
        if report_skill:
            result = report_skill(df)
        else:
            # Fallback: Generate basic summary if report_skill is not available
            result = generate_basic_summary(df)
        
        return jsonify({
            'status': 'success',
            'summary': result.get('summary', {}),
            'recommendations': result.get('recommendations', [])
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': f'An unexpected error occurred: {str(e)}'
        }), 500

def generate_basic_summary(df):
    """
    Generate a basic summary of the dataframe when report_skill is not available.
    
    Args:
        df: pandas DataFrame
    
    Returns:
        dict: Summary and recommendations
    """
    summary = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'columns': list(df.columns),
        'column_types': df.dtypes.astype(str).to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'statistics': {}
    }
    
    # Add statistics for numeric columns
    numeric_columns = df.select_dtypes(include=['number']).columns
    if len(numeric_columns) > 0:
        summary['statistics'] = df[numeric_columns].describe().to_dict()
    
    # Generate basic recommendations
    recommendations = []
    
    # Check for missing values
    missing_count = df.isnull().sum().sum()
    if missing_count > 0:
        recommendations.append(f"Dataset contains {missing_count} missing values. Consider data cleaning or imputation.")
    
    # Check for numeric columns
    if len(numeric_columns) > 0:
        recommendations.append(f"Dataset has {len(numeric_columns)} numeric columns suitable for statistical analysis.")
    
    # Check dataset size
    if len(df) < 30:
        recommendations.append("Small dataset size. Results may have limited statistical significance.")
    elif len(df) > 10000:
        recommendations.append("Large dataset detected. Consider sampling for faster exploratory analysis.")
    
    # Check for potential duplicates
    duplicate_count = df.duplicated().sum()
    if duplicate_count > 0:
        recommendations.append(f"Found {duplicate_count} duplicate rows. Consider removing duplicates if appropriate.")
    
    return {
        'summary': summary,
        'recommendations': recommendations
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
