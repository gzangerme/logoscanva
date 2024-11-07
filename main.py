from jinja2 import Template
import plotly.graph_objs as go
from plotly.io import to_html
import pandas as pd


def read_template(template_path):
    """
    Reads an HTML template from a specified file path.

    Args:
        template_path (str): Path to the HTML template file.

    Returns:
        str: HTML content of the template.
    """
    with open(template_path, 'r') as file:
        return file.read()

def calculate_mean_scores(data, level, category_column='CATEGORIA'):
    """
    Calculates the mean scores for a specified level and each category.

    Args:
        data (pd.DataFrame): DataFrame containing engineer scores.
        level (str): Level to filter data (e.g., 'Junior', 'Senior').
        category_column (str): Column name containing categories.

    Returns:
        dict: Dictionary of categories and their mean scores for the specified level.
    """
    mean_scores = data[data['NIVEL'] == level].groupby(category_column)['PONTUACAO'].mean().to_dict()
    return mean_scores

def create_bar_chart(data1, data2, labels, title, yaxis_title):
    """
    Creates an interactive bar chart comparing two data sets.

    Args:
        data1 (dict): First data set to plot (e.g., Juniors).
        data2 (dict): Second data set to plot (e.g., Seniors).
        labels (list): Labels for each category.
        title (str): Title of the chart.
        yaxis_title (str): Y-axis title.

    Returns:
        str: HTML representation of the Plotly figure.
    """
    fig = go.Figure()
    fig.add_trace(go.Bar(x=labels, y=[data1.get(label, 0) for label in labels], name='Juniors'))
    fig.add_trace(go.Bar(x=labels, y=[data2.get(label, 0) for label in labels], name='Seniors'))
    fig.update_layout(
        title=title,
        yaxis_title=yaxis_title,
        barmode='group',
        xaxis_tickangle=-45
    )
    return to_html(fig, full_html=False)

def create_senior_comparison_chart(data_senior_data, data_senior_analytics, categories, title, yaxis_title):
    """
    Creates an interactive bar chart comparing senior scores between Data Engineers and Analytics Engineers.

    Args:
        data_senior_data (dict): Senior Data Engineer scores by category.
        data_senior_analytics (dict): Senior Analytics Engineer scores by category.
        categories (list): List of categories.
        title (str): Title of the chart.
        yaxis_title (str): Y-axis title.

    Returns:
        str: HTML representation of the Plotly figure.
    """
    fig = go.Figure()
    fig.add_trace(go.Bar(x=categories, y=[data_senior_data.get(cat, 0) for cat in categories], name='Data Engineers Senior'))
    fig.add_trace(go.Bar(x=categories, y=[data_senior_analytics.get(cat, 0) for cat in categories], name='Analytics Engineers Senior'))
    fig.update_layout(
        title=title,
        yaxis_title=yaxis_title,
        barmode='group',
        xaxis_tickangle=-45
    )
    return to_html(fig, full_html=False)

def generate_interactive_report(data, template_path="templates/template.html", output_path="engineering_insights_interactive_report.html"):
    """
    Generates an HTML report with interactive Plotly charts embedded in a template.

    Args:
        data (pd.DataFrame): DataFrame containing engineer data.
        template_path (str): Path to the HTML template file.
        output_path (str): Path to save the generated HTML report.

    Returns:
        str: Path to the saved HTML report.
    """
    # Load template
    template_content = read_template(template_path)
    
    # Calculate mean scores for each level by category
    categories = sorted(data['CATEGORIA'].unique())
    junior_data = calculate_mean_scores(data[data['CARGO'] == 'ENGENHARIA DE DADOS'], 'Junior')
    senior_data = calculate_mean_scores(data[data['CARGO'] == 'ENGENHARIA DE DADOS'], 'Sênior')
    junior_analytics = calculate_mean_scores(data[data['CARGO'] == 'ENGENHARIA DE ANALYTICS'], 'Junior')
    senior_analytics = calculate_mean_scores(data[data['CARGO'] == 'ENGENHARIA DE ANALYTICS'], 'Sênior')
    pleno_data = calculate_mean_scores(data[data['CARGO'] == 'ENGENHARIA DE DADOS'], 'Pleno')
    pleno_analytics = calculate_mean_scores(data[data['CARGO'] == 'ENGENHARIA DE ANALYTICS'], 'Pleno')

    # Generate charts
    junior_senior_chart_data = create_bar_chart(
        junior_data, senior_data, categories,
        "Comparação de Pontuação Média: Juniors vs Seniors (Data Engineers)",
        "Pontuação Média"
    )
    pleno_senior_chart_data = create_bar_chart(
        pleno_data, senior_data, categories,
        "Comparação de Pontuação Média: Plenos vs Seniors (Data Engineers)",
        "Pontuação Média"
    )
    junior_senior_chart_analytics = create_bar_chart(
        junior_analytics, senior_analytics, categories,
        "Comparação de Pontuação Média: Juniors vs Seniors (Analytics Engineers)",
        "Pontuação Média"
    )
    pleno_senior_chart_analytics = create_bar_chart(
        pleno_analytics, senior_analytics, categories,
        "Comparação de Pontuação Média: Plenos vs Seniors (Analytics Engineers)",
        "Pontuação Média"
    )
    senior_comparison_chart = create_senior_comparison_chart(
        senior_data, senior_analytics, categories,
        "Comparação de Pontuação Média: Seniors (Data vs Analytics Engineers)",
        "Pontuação Média"
    )

    # Render template with charts
    template = Template(template_content)
    html_report = template.render(
        junior_senior_chart_data=junior_senior_chart_data,
        pleno_senior_chart_data=pleno_senior_chart_data,
        junior_senior_chart_analytics=junior_senior_chart_analytics,
        pleno_senior_chart_analytics=pleno_senior_chart_analytics,
        senior_comparison_chart=senior_comparison_chart
    )
    
    # Save the report
    with open(output_path, "w") as file:
        file.write(html_report)

    return output_path




df = pd.read_csv('data/data.csv')

generate_interactive_report(df)

