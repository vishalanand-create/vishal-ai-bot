import pandas as pd
import numpy as np

def greet_skill(user_input):
    """
    Greet skill - responds to greetings from users
    """
    greetings = ['hello', 'hi', 'hey', 'greetings']
    user_input_lower = user_input.lower()
    
    for greeting in greetings:
        if greeting in user_input_lower:
            return "Hello! How can I help you today?"
    
    return None

def faq_skill(user_input):
    """
    FAQ skill - responds to frequently asked questions
    """
    faqs = {
        'what is your name': 'I am Agent Vish, your virtual assistant.',
        'what can you do': 'I can help you with greetings, answer FAQs, and assist with various tasks.',
        'how are you': 'I am doing great! Thank you for asking. How can I assist you?',
        'who created you': 'I was created by Vishal Anand.'
    }
    
    user_input_lower = user_input.lower().strip()
    
    for question, answer in faqs.items():
        if question in user_input_lower:
            return answer
    
    return None

def report_skill(df):
    """
    Report analysis skill - processes CSV/Excel data and generates summary with recommendations.
    
    Args:
        df (pandas.DataFrame): Input dataframe containing the report data
    
    Returns:
        dict: Dictionary containing 'summary' and 'recommendations' keys with analysis results
    """
    try:
        # Initialize result structure
        result = {
            'summary': {},
            'recommendations': []
        }
        
        # Basic dataset information
        result['summary']['total_rows'] = len(df)
        result['summary']['total_columns'] = len(df.columns)
        result['summary']['columns'] = list(df.columns)
        result['summary']['column_types'] = df.dtypes.astype(str).to_dict()
        
        # Missing value analysis
        missing_values = df.isnull().sum().to_dict()
        result['summary']['missing_values'] = missing_values
        total_missing = sum(missing_values.values())
        result['summary']['total_missing_values'] = total_missing
        
        # Memory usage
        result['summary']['memory_usage_mb'] = round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2)
        
        # Numeric columns analysis
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        result['summary']['numeric_columns'] = numeric_columns
        result['summary']['numeric_column_count'] = len(numeric_columns)
        
        if len(numeric_columns) > 0:
            # Statistical summary for numeric columns
            stats = df[numeric_columns].describe().to_dict()
            result['summary']['statistics'] = stats
            
            # Correlation analysis
            if len(numeric_columns) > 1:
                correlation_matrix = df[numeric_columns].corr()
                # Find strong correlations (>0.7 or <-0.7)
                strong_correlations = []
                for i in range(len(correlation_matrix.columns)):
                    for j in range(i+1, len(correlation_matrix.columns)):
                        corr_value = correlation_matrix.iloc[i, j]
                        if abs(corr_value) > 0.7:
                            strong_correlations.append({
                                'column1': correlation_matrix.columns[i],
                                'column2': correlation_matrix.columns[j],
                                'correlation': round(corr_value, 3)
                            })
                result['summary']['strong_correlations'] = strong_correlations
        
        # Categorical columns analysis
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
        result['summary']['categorical_columns'] = categorical_columns
        result['summary']['categorical_column_count'] = len(categorical_columns)
        
        if len(categorical_columns) > 0:
            # Unique value counts for categorical columns
            unique_counts = {col: df[col].nunique() for col in categorical_columns}
            result['summary']['unique_value_counts'] = unique_counts
        
        # Duplicate rows analysis
        duplicate_count = df.duplicated().sum()
        result['summary']['duplicate_rows'] = duplicate_count
        
        # Generate recommendations based on analysis
        recommendations = generate_recommendations(df, result['summary'])
        result['recommendations'] = recommendations
        
        return result
        
    except Exception as e:
        return {
            'summary': {'error': str(e)},
            'recommendations': [f'Error processing report: {str(e)}']
        }

def generate_recommendations(df, summary):
    """
    Generate actionable recommendations based on data analysis.
    
    Args:
        df (pandas.DataFrame): Input dataframe
        summary (dict): Summary statistics dictionary
    
    Returns:
        list: List of recommendation strings
    """
    recommendations = []
    
    # Data quality recommendations
    if summary.get('total_missing_values', 0) > 0:
        missing_pct = (summary['total_missing_values'] / (summary['total_rows'] * summary['total_columns'])) * 100
        if missing_pct > 10:
            recommendations.append(
                f"High missing data rate ({missing_pct:.1f}%). Consider imputation strategies or collecting more complete data."
            )
        else:
            recommendations.append(
                f"Dataset has {summary['total_missing_values']} missing values ({missing_pct:.1f}%). Review data collection process."
            )
    else:
        recommendations.append("Excellent data quality: No missing values detected.")
    
    # Duplicate data recommendations
    if summary.get('duplicate_rows', 0) > 0:
        dup_pct = (summary['duplicate_rows'] / summary['total_rows']) * 100
        recommendations.append(
            f"Found {summary['duplicate_rows']} duplicate rows ({dup_pct:.1f}%). Consider deduplication to improve data quality."
        )
    
    # Dataset size recommendations
    total_rows = summary['total_rows']
    if total_rows < 30:
        recommendations.append(
            "Small sample size detected. Statistical conclusions may have limited reliability. Consider collecting more data."
        )
    elif total_rows < 100:
        recommendations.append(
            "Moderate sample size. Ensure statistical tests account for sample size limitations."
        )
    elif total_rows > 100000:
        recommendations.append(
            "Large dataset detected. Consider implementing sampling strategies for exploratory analysis and data visualization."
        )
    
    # Correlation recommendations
    if 'strong_correlations' in summary and len(summary['strong_correlations']) > 0:
        corr_pairs = len(summary['strong_correlations'])
        recommendations.append(
            f"Found {corr_pairs} strong correlation(s) between numeric variables. Review for potential multicollinearity in predictive models."
        )
    
    # Numeric data recommendations
    if summary.get('numeric_column_count', 0) > 0:
        recommendations.append(
            f"Dataset contains {summary['numeric_column_count']} numeric column(s). Consider statistical analysis, trend analysis, and predictive modeling."
        )
        
        # Check for outliers in numeric columns
        if 'statistics' in summary:
            for col, stats in summary['statistics'].items():
                if 'std' in stats and stats['std'] > 0:
                    # Simple outlier check using IQR
                    q1 = stats.get('25%', 0)
                    q3 = stats.get('75%', 0)
                    iqr = q3 - q1
                    if iqr > 0:
                        lower_bound = q1 - 1.5 * iqr
                        upper_bound = q3 + 1.5 * iqr
                        outlier_count = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
                        if outlier_count > 0:
                            outlier_pct = (outlier_count / len(df)) * 100
                            if outlier_pct > 5:
                                recommendations.append(
                                    f"Column '{col}' has {outlier_count} potential outliers ({outlier_pct:.1f}%). Consider outlier treatment strategies."
                                )
                                break  # Only report first significant outlier case
    
    # Categorical data recommendations
    if summary.get('categorical_column_count', 0) > 0:
        recommendations.append(
            f"Dataset has {summary['categorical_column_count']} categorical column(s). Consider encoding strategies for machine learning applications."
        )
        
        # Check for high cardinality
        if 'unique_value_counts' in summary:
            high_cardinality_cols = [col for col, count in summary['unique_value_counts'].items() 
                                    if count > total_rows * 0.5]
            if high_cardinality_cols:
                recommendations.append(
                    f"High cardinality detected in column(s): {', '.join(high_cardinality_cols[:3])}. Consider grouping or dimensionality reduction."
                )
    
    # Memory optimization recommendations
    if summary.get('memory_usage_mb', 0) > 100:
        recommendations.append(
            f"Large memory footprint ({summary['memory_usage_mb']} MB). Consider data type optimization or chunked processing for better performance."
        )
    
    # General analysis recommendations
    if summary.get('numeric_column_count', 0) >= 2:
        recommendations.append(
            "Consider creating visualizations: scatter plots, correlation heatmaps, and distribution plots for deeper insights."
        )
    
    if summary.get('categorical_column_count', 0) > 0 and summary.get('numeric_column_count', 0) > 0:
        recommendations.append(
            "Mixed data types present. Consider segmentation analysis and group comparisons for meaningful insights."
        )
    
    return recommendations
