
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Setup ---
# Set a professional style for the plots
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("colorblind")
CHART_DIR = "charts"
if not os.path.exists(CHART_DIR):
    os.makedirs(CHART_DIR)

import sys

# --- Data Loading and Cleaning ---
try:
    if len(sys.argv) > 1:
        dataset_path = sys.argv[1]
    else:
        dataset_path = "ai_human_content_detection_dataset.csv"
    df = pd.read_csv(dataset_path)

    # Impute missing values with the median
    df['sentiment_score'].fillna(df['sentiment_score'].median(), inplace=True)
    df['gunning_fog_index'].fillna(df['gunning_fog_index'].median(), inplace=True)

    # Add a human-readable label for charts
    df['source'] = df['label'].apply(lambda x: 'AI-Generated' if x == 1 else 'Human-Written')

    print("Data loaded and cleaned successfully.")

except FileNotFoundError:
    print("Error: The dataset file 'ai_human_content_detection_dataset.csv' was not found.")
    exit()


# --- Visualizations ---

# Insight 1: AI vs. Human Content Distribution
plt.figure(figsize=(8, 6))
ax = sns.countplot(x='source', data=df, hue='source', palette={'AI-Generated': '#4c72b0', 'Human-Written': '#dd8452'}, dodge=False, legend=False)
plt.title('Overall Content Distribution: AI vs. Human', fontsize=16, weight='bold')
plt.xlabel('Content Source', fontsize=12)
plt.ylabel('Number of Articles', fontsize=12)
for p in ax.patches:
    ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', fontsize=11, color='black', xytext=(0, 5),
                textcoords='offset points')
plt.savefig(os.path.join(CHART_DIR, "1_content_distribution.png"))
plt.close()

# Insight 2: Content Distribution by Type
plt.figure(figsize=(10, 8))
sns.countplot(y='content_type', data=df, order=df['content_type'].value_counts().index, palette='viridis', hue='content_type', dodge=False, legend=False)
plt.title('Number of Articles by Content Type', fontsize=16, weight='bold')
plt.xlabel('Number of Articles', fontsize=12)
plt.ylabel('Content Type', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "2_content_by_type.png"))
plt.close()

# Insight 3: Lexical Diversity: AI vs. Human
plt.figure(figsize=(10, 7))
sns.boxplot(x='source', y='lexical_diversity', data=df, palette={'AI-Generated': '#4c72b0', 'Human-Written': '#dd8452'}, hue='source', legend=False)
plt.title('Lexical Diversity: AI-Generated vs. Human-Written', fontsize=16, weight='bold')
plt.xlabel('Content Source', fontsize=12)
plt.ylabel('Lexical Diversity Score', fontsize=12)
plt.savefig(os.path.join(CHART_DIR, "3_lexical_diversity.png"))
plt.close()

# Insight 4: Predictability Score: A Key Differentiator
plt.figure(figsize=(10, 7))
sns.kdeplot(data=df, x='predictability_score', hue='source', fill=True, common_norm=False, palette={'AI-Generated': '#4c72b0', 'Human-Written': '#dd8452'})
plt.title('Distribution of Predictability Scores', fontsize=16, weight='bold')
plt.xlabel('Predictability Score', fontsize=12)
plt.ylabel('Density', fontsize=12)
plt.savefig(os.path.join(CHART_DIR, "4_predictability_score.png"))
plt.close()

# Insight 5: Burstiness: The Rhythm of Writing
plt.figure(figsize=(10, 7))
sns.violinplot(x='source', y='burstiness', data=df, palette={'AI-Generated': '#4c72b0', 'Human-Written': '#dd8452'}, hue='source', legend=False)
plt.title('Writing Burstiness: AI-Generated vs. Human-Written', fontsize=16, weight='bold')
plt.xlabel('Content Source', fontsize=12)
plt.ylabel('Burstiness Score', fontsize=12)
plt.savefig(os.path.join(CHART_DIR, "5_burstiness.png"))
plt.close()

# Insight 6: Sentiment Analysis: The Emotional Tone
plt.figure(figsize=(10, 7))
sns.barplot(x='source', y='sentiment_score', data=df, palette={'AI-Generated': '#4c72b0', 'Human-Written': '#dd8452'}, hue='source', dodge=False, legend=False, estimator=lambda x: sum(x) / len(x)) # Using mean estimator
plt.title('Average Sentiment Score: AI vs. Human', fontsize=16, weight='bold')
plt.xlabel('Content Source', fontsize=12)
plt.ylabel('Average Sentiment Score', fontsize=12)
plt.axhline(0, color='grey', linewidth=0.8)
plt.savefig(os.path.join(CHART_DIR, "6_sentiment_analysis.png"))
plt.close()

# Insight 7: Readability (Flesch Score): AI vs. Human
plt.figure(figsize=(10, 7))
sns.kdeplot(data=df, x='flesch_reading_ease', hue='source', fill=True, common_norm=False, palette={'AI-Generated': '#4c72b0', 'Human-Written': '#dd8452'})
plt.title('Distribution of Flesch Reading Ease Scores', fontsize=16, weight='bold')
plt.xlabel('Flesch Reading Ease Score', fontsize=12)
plt.ylabel('Density', fontsize=12)
plt.savefig(os.path.join(CHART_DIR, "7_readability.png"))
plt.close()

# Insight 8: Word Count vs. Sentence Count
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df, x='word_count', y='sentence_count', hue='source', alpha=0.6, palette={'AI-Generated': '#4c72b0', 'Human-Written': '#dd8452'})
plt.title('Word Count vs. Sentence Count', fontsize=16, weight='bold')
plt.xlabel('Word Count', fontsize=12)
plt.ylabel('Sentence Count', fontsize=12)
plt.xscale('log')
plt.yscale('log')
plt.savefig(os.path.join(CHART_DIR, "8_word_vs_sentence.png"))
plt.close()

# Insight 9: Grammar Errors Across Content Types
plt.figure(figsize=(12, 8))
avg_errors = df.groupby(['content_type', 'source'])['grammar_errors'].mean().reset_index()
sns.barplot(x='grammar_errors', y='content_type', hue='source', data=avg_errors, palette={'AI-Generated': '#4c72b0', 'Human-Written': '#dd8452'})
plt.title('Average Grammar Errors per Content Type', fontsize=16, weight='bold')
plt.xlabel('Average Number of Grammar Errors', fontsize=12)
plt.ylabel('Content Type', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "9_grammar_errors.png"))
plt.close()

# Insight 10: Correlation of Linguistic Features
plt.figure(figsize=(14, 10))
# Select only numeric columns for correlation
numeric_cols = df.select_dtypes(include=['number']).columns
corr_matrix = df[numeric_cols].corr()
sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', linewidths=.5)
plt.title('Correlation Matrix of Linguistic Features', fontsize=16, weight='bold')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "10_correlation_heatmap.png"))
plt.close()

print("10 visualization charts have been successfully generated and saved to the 'charts' directory.")
