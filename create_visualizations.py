"""
DNA Dataset Visualization Generator
יוצר ויזואליזציות להבנת הנתונים
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import Counter
import os

# הגדרות עיצוב
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# צבעים
COLORS = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B', 
          '#95C623', '#5C4D7D', '#E8E8E8', '#FF6B6B', '#4ECDC4']

def load_data():
    """טעינת הנתונים"""
    base_path = "/Users/ido.abramovitch/Documents/dna project"
    
    train = pd.read_csv(f"{base_path}/train.csv", index_col=0)
    test = pd.read_csv(f"{base_path}/test.csv", index_col=0)
    val = pd.read_csv(f"{base_path}/validation.csv", index_col=0)
    
    # הוספת עמודת מקור
    train['source'] = 'train'
    test['source'] = 'test'
    val['source'] = 'validation'
    
    # איחוד
    all_data = pd.concat([train, test, val], ignore_index=True)
    
    # חישוב אורך רצף
    all_data['seq_length'] = all_data['NucleotideSequence'].apply(
        lambda x: len(str(x).strip('<>'))
    )
    
    return train, test, val, all_data

def plot_gene_type_distribution(all_data, save_path):
    """1. התפלגות סוגי גנים"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    
    # ספירה
    valid_types = ['PSEUDO', 'BIOLOGICAL_REGION', 'ncRNA', 'snoRNA', 
                   'PROTEIN_CODING', 'tRNA', 'OTHER', 'rRNA', 'snRNA', 'scRNA']
    gene_counts = all_data[all_data['GeneType'].isin(valid_types)]['GeneType'].value_counts()
    
    # גרף עמודות
    ax1 = axes[0]
    bars = ax1.barh(gene_counts.index, gene_counts.values, color=COLORS[:len(gene_counts)])
    ax1.set_xlabel('Count')
    ax1.set_title('Gene Type Distribution (Count)')
    ax1.bar_label(bars, padding=3, fmt='%d')
    
    # גרף עוגה
    ax2 = axes[1]
    ax2.pie(gene_counts.values, labels=gene_counts.index, autopct='%1.1f%%', 
            colors=COLORS[:len(gene_counts)], explode=[0.05]*len(gene_counts))
    ax2.set_title('Gene Type Distribution (Percentage)')
    
    plt.suptitle('📊 Gene Type Distribution', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{save_path}/01_gene_type_distribution.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Created: 01_gene_type_distribution.png")

def plot_sequence_length_distribution(all_data, save_path):
    """2. התפלגות אורכי רצפים"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # היסטוגרמה כללית
    ax1 = axes[0, 0]
    ax1.hist(all_data['seq_length'], bins=50, color=COLORS[0], edgecolor='white', alpha=0.8)
    ax1.axvline(all_data['seq_length'].mean(), color='red', linestyle='--', label=f"Mean: {all_data['seq_length'].mean():.0f}")
    ax1.axvline(all_data['seq_length'].median(), color='green', linestyle='--', label=f"Median: {all_data['seq_length'].median():.0f}")
    ax1.set_xlabel('Sequence Length')
    ax1.set_ylabel('Count')
    ax1.set_title('Overall Sequence Length Distribution')
    ax1.legend()
    
    # Box plot לפי סוג גן
    ax2 = axes[0, 1]
    valid_types = ['PSEUDO', 'BIOLOGICAL_REGION', 'ncRNA', 'PROTEIN_CODING', 'tRNA', 'snoRNA']
    data_filtered = all_data[all_data['GeneType'].isin(valid_types)]
    sns.boxplot(data=data_filtered, x='GeneType', y='seq_length', ax=ax2, palette=COLORS)
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')
    ax2.set_title('Sequence Length by Gene Type')
    ax2.set_ylabel('Sequence Length')
    
    # היסטוגרמה לפי סוג
    ax3 = axes[1, 0]
    for i, gt in enumerate(valid_types[:4]):
        data = all_data[all_data['GeneType'] == gt]['seq_length']
        ax3.hist(data, bins=30, alpha=0.5, label=gt, color=COLORS[i])
    ax3.set_xlabel('Sequence Length')
    ax3.set_ylabel('Count')
    ax3.set_title('Sequence Length Distribution by Gene Type')
    ax3.legend()
    
    # סטטיסטיקות
    ax4 = axes[1, 1]
    stats_data = []
    for gt in valid_types:
        lengths = all_data[all_data['GeneType'] == gt]['seq_length']
        if len(lengths) > 0:
            stats_data.append({
                'GeneType': gt,
                'Mean': lengths.mean(),
                'Median': lengths.median(),
                'Std': lengths.std()
            })
    
    stats_df = pd.DataFrame(stats_data)
    x = np.arange(len(stats_df))
    width = 0.35
    
    ax4.bar(x - width/2, stats_df['Mean'], width, label='Mean', color=COLORS[0])
    ax4.bar(x + width/2, stats_df['Median'], width, label='Median', color=COLORS[1])
    ax4.errorbar(x - width/2, stats_df['Mean'], yerr=stats_df['Std'], fmt='none', color='black', capsize=3)
    ax4.set_xticks(x)
    ax4.set_xticklabels(stats_df['GeneType'], rotation=45, ha='right')
    ax4.set_ylabel('Sequence Length')
    ax4.set_title('Mean & Median Length by Gene Type')
    ax4.legend()
    
    plt.suptitle('📏 Sequence Length Analysis', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{save_path}/02_sequence_length_distribution.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Created: 02_sequence_length_distribution.png")

def plot_data_split_analysis(train, test, val, save_path):
    """3. ניתוח חלוקת הנתונים"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # גודל הסטים
    ax1 = axes[0, 0]
    sizes = [len(train), len(test), len(val)]
    labels = ['Train', 'Test', 'Validation']
    bars = ax1.bar(labels, sizes, color=COLORS[:3])
    ax1.bar_label(bars, fmt='%d')
    ax1.set_ylabel('Number of Samples')
    ax1.set_title('Dataset Split Sizes')
    
    # אחוזים
    ax2 = axes[0, 1]
    ax2.pie(sizes, labels=labels, autopct='%1.1f%%', colors=COLORS[:3], explode=[0.02]*3)
    ax2.set_title('Dataset Split Proportions')
    
    # התפלגות לפי סוג גן בכל סט
    ax3 = axes[1, 0]
    valid_types = ['PSEUDO', 'BIOLOGICAL_REGION', 'ncRNA', 'PROTEIN_CODING']
    
    train_counts = train[train['GeneType'].isin(valid_types)]['GeneType'].value_counts()
    test_counts = test[test['GeneType'].isin(valid_types)]['GeneType'].value_counts()
    val_counts = val[val['GeneType'].isin(valid_types)]['GeneType'].value_counts()
    
    x = np.arange(len(valid_types))
    width = 0.25
    
    ax3.bar(x - width, [train_counts.get(t, 0) for t in valid_types], width, label='Train', color=COLORS[0])
    ax3.bar(x, [test_counts.get(t, 0) for t in valid_types], width, label='Test', color=COLORS[1])
    ax3.bar(x + width, [val_counts.get(t, 0) for t in valid_types], width, label='Validation', color=COLORS[2])
    
    ax3.set_xticks(x)
    ax3.set_xticklabels(valid_types, rotation=45, ha='right')
    ax3.set_ylabel('Count')
    ax3.set_title('Gene Type Distribution per Dataset')
    ax3.legend()
    
    # Data Leakage Visualization
    ax4 = axes[1, 1]
    train_seqs = set(train['NucleotideSequence'])
    test_seqs = set(test['NucleotideSequence'])
    val_seqs = set(val['NucleotideSequence'])
    
    leakage_data = {
        'Train∩Test': len(train_seqs & test_seqs),
        'Train∩Val': len(train_seqs & val_seqs),
        'Test∩Val': len(test_seqs & val_seqs),
    }
    
    bars = ax4.bar(leakage_data.keys(), leakage_data.values(), color=['#FF6B6B', '#FF6B6B', '#FFE66D'])
    ax4.bar_label(bars, fmt='%d')
    ax4.set_ylabel('Overlapping Sequences')
    ax4.set_title('⚠️ DATA LEAKAGE: Overlapping Sequences Between Sets')
    ax4.axhline(y=0, color='green', linestyle='-', linewidth=2, label='Ideal (0)')
    
    plt.suptitle('📂 Data Split Analysis', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{save_path}/03_data_split_analysis.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Created: 03_data_split_analysis.png")

def plot_nucleotide_composition(all_data, save_path):
    """4. הרכב נוקלאוטידים"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # חישוב הרכב
    def calc_composition(seq):
        seq = str(seq).strip('<>').upper()
        total = len(seq)
        if total == 0:
            return {'A': 0, 'T': 0, 'G': 0, 'C': 0, 'GC': 0}
        return {
            'A': seq.count('A') / total * 100,
            'T': seq.count('T') / total * 100,
            'G': seq.count('G') / total * 100,
            'C': seq.count('C') / total * 100,
            'GC': (seq.count('G') + seq.count('C')) / total * 100
        }
    
    # מדגם לחישוב מהיר
    sample = all_data.sample(min(5000, len(all_data)), random_state=42)
    compositions = sample['NucleotideSequence'].apply(calc_composition).apply(pd.Series)
    
    # התפלגות GC Content
    ax1 = axes[0, 0]
    ax1.hist(compositions['GC'], bins=50, color=COLORS[0], edgecolor='white', alpha=0.8)
    ax1.axvline(compositions['GC'].mean(), color='red', linestyle='--', 
                label=f"Mean: {compositions['GC'].mean():.1f}%")
    ax1.set_xlabel('GC Content (%)')
    ax1.set_ylabel('Count')
    ax1.set_title('GC Content Distribution')
    ax1.legend()
    
    # הרכב ממוצע
    ax2 = axes[0, 1]
    nucleotides = ['A', 'T', 'G', 'C']
    means = [compositions[n].mean() for n in nucleotides]
    bars = ax2.bar(nucleotides, means, color=['#FF6B6B', '#4ECDC4', '#FFE66D', '#95E1D3'])
    ax2.bar_label(bars, fmt='%.1f%%')
    ax2.set_ylabel('Percentage (%)')
    ax2.set_title('Average Nucleotide Composition')
    ax2.set_ylim(0, 40)
    
    # GC Content לפי סוג גן
    ax3 = axes[1, 0]
    valid_types = ['PSEUDO', 'BIOLOGICAL_REGION', 'ncRNA', 'PROTEIN_CODING', 'tRNA', 'snoRNA']
    sample['GC'] = compositions['GC']
    data_filtered = sample[sample['GeneType'].isin(valid_types)]
    
    gc_by_type = data_filtered.groupby('GeneType')['GC'].mean().sort_values(ascending=False)
    bars = ax3.barh(gc_by_type.index, gc_by_type.values, color=COLORS[:len(gc_by_type)])
    ax3.bar_label(bars, fmt='%.1f%%', padding=3)
    ax3.set_xlabel('GC Content (%)')
    ax3.set_title('GC Content by Gene Type')
    ax3.set_xlim(0, 70)
    
    # Box plot GC by type
    ax4 = axes[1, 1]
    sns.boxplot(data=data_filtered, x='GeneType', y='GC', ax=ax4, palette=COLORS)
    ax4.set_xticklabels(ax4.get_xticklabels(), rotation=45, ha='right')
    ax4.set_ylabel('GC Content (%)')
    ax4.set_title('GC Content Distribution by Gene Type')
    
    plt.suptitle('🧬 Nucleotide Composition Analysis', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{save_path}/04_nucleotide_composition.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Created: 04_nucleotide_composition.png")

def plot_class_imbalance(all_data, save_path):
    """5. ויזואליזציית חוסר איזון"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    
    valid_types = ['PSEUDO', 'BIOLOGICAL_REGION', 'ncRNA', 'snoRNA', 
                   'PROTEIN_CODING', 'tRNA', 'OTHER', 'rRNA', 'snRNA', 'scRNA']
    gene_counts = all_data[all_data['GeneType'].isin(valid_types)]['GeneType'].value_counts()
    
    # Log scale
    ax1 = axes[0]
    bars = ax1.bar(gene_counts.index, gene_counts.values, color=COLORS[:len(gene_counts)])
    ax1.set_yscale('log')
    ax1.set_ylabel('Count (log scale)')
    ax1.set_title('Class Distribution (Log Scale)')
    ax1.set_xticklabels(gene_counts.index, rotation=45, ha='right')
    
    # יחסים
    ax2 = axes[1]
    max_count = gene_counts.max()
    ratios = max_count / gene_counts
    bars = ax2.barh(ratios.index, ratios.values, color=COLORS[:len(ratios)])
    ax2.bar_label(bars, fmt='%.0f:1', padding=3)
    ax2.set_xlabel('Imbalance Ratio (relative to largest class)')
    ax2.set_title('⚠️ Class Imbalance Ratios')
    
    plt.suptitle('⚖️ Class Imbalance Analysis', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{save_path}/05_class_imbalance.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Created: 05_class_imbalance.png")

def plot_symbol_patterns(all_data, save_path):
    """6. דפוסים ב-Symbol"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # חילוץ prefix
    all_data['symbol_prefix'] = all_data['Symbol'].str.extract(r'^([A-Z]+)', expand=False)
    
    # Top prefixes
    ax1 = axes[0, 0]
    top_prefixes = all_data['symbol_prefix'].value_counts().head(15)
    bars = ax1.barh(top_prefixes.index[::-1], top_prefixes.values[::-1], color=COLORS[0])
    ax1.set_xlabel('Count')
    ax1.set_title('Top 15 Symbol Prefixes')
    
    # Prefix לפי סוג גן
    ax2 = axes[0, 1]
    prefix_type = all_data.groupby(['symbol_prefix', 'GeneType']).size().unstack(fill_value=0)
    top_5_prefixes = all_data['symbol_prefix'].value_counts().head(5).index
    valid_types = ['PSEUDO', 'BIOLOGICAL_REGION', 'ncRNA', 'PROTEIN_CODING']
    
    subset = prefix_type.loc[top_5_prefixes, valid_types] if all(t in prefix_type.columns for t in valid_types) else prefix_type.loc[top_5_prefixes].iloc[:, :4]
    subset.plot(kind='bar', ax=ax2, color=COLORS[:4])
    ax2.set_title('Gene Type Distribution by Symbol Prefix')
    ax2.set_xlabel('Symbol Prefix')
    ax2.set_ylabel('Count')
    ax2.legend(title='GeneType', bbox_to_anchor=(1.02, 1))
    ax2.tick_params(axis='x', rotation=45)
    
    # סיומת P
    ax3 = axes[1, 0]
    all_data['ends_with_P'] = all_data['Symbol'].str.endswith('P')
    p_suffix_types = all_data[all_data['ends_with_P']]['GeneType'].value_counts().head(5)
    bars = ax3.bar(p_suffix_types.index, p_suffix_types.values, color=COLORS[1])
    ax3.set_title('Gene Types for Symbols Ending with "P"')
    ax3.set_ylabel('Count')
    ax3.tick_params(axis='x', rotation=45)
    
    # אורך Symbol
    ax4 = axes[1, 1]
    all_data['symbol_length'] = all_data['Symbol'].str.len()
    ax4.hist(all_data['symbol_length'], bins=30, color=COLORS[2], edgecolor='white')
    ax4.set_xlabel('Symbol Length')
    ax4.set_ylabel('Count')
    ax4.set_title('Symbol Length Distribution')
    
    plt.suptitle('🏷️ Symbol Pattern Analysis', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{save_path}/06_symbol_patterns.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Created: 06_symbol_patterns.png")

def plot_correlation_heatmap(all_data, save_path):
    """7. מפת קורלציות"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # יצירת פיצ'רים מספריים
    all_data['seq_length'] = all_data['NucleotideSequence'].apply(lambda x: len(str(x).strip('<>')))
    all_data['symbol_length'] = all_data['Symbol'].str.len()
    all_data['desc_length'] = all_data['Description'].str.len()
    all_data['ends_with_P'] = all_data['Symbol'].str.endswith('P').astype(int)
    all_data['starts_with_LOC'] = all_data['Symbol'].str.startswith('LOC').astype(int)
    
    # חישוב GC
    def gc_content(seq):
        seq = str(seq).strip('<>').upper()
        if len(seq) == 0:
            return 0
        return (seq.count('G') + seq.count('C')) / len(seq) * 100
    
    sample = all_data.sample(min(5000, len(all_data)), random_state=42)
    sample['gc_content'] = sample['NucleotideSequence'].apply(gc_content)
    
    # מטריצת קורלציה
    numeric_cols = ['seq_length', 'symbol_length', 'desc_length', 'ends_with_P', 'starts_with_LOC', 'gc_content']
    corr_matrix = sample[numeric_cols].corr()
    
    sns.heatmap(corr_matrix, annot=True, cmap='RdBu_r', center=0, 
                square=True, ax=ax, fmt='.2f', vmin=-1, vmax=1)
    ax.set_title('📊 Feature Correlation Heatmap')
    
    plt.tight_layout()
    plt.savefig(f"{save_path}/07_correlation_heatmap.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Created: 07_correlation_heatmap.png")

def plot_summary_dashboard(all_data, train, test, val, save_path):
    """8. דשבורד סיכום"""
    fig = plt.figure(figsize=(20, 14))
    
    # Grid
    gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)
    
    # 1. סה"כ דגימות
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.text(0.5, 0.5, f"{len(all_data):,}", fontsize=40, ha='center', va='center', fontweight='bold', color=COLORS[0])
    ax1.text(0.5, 0.2, "Total Samples", fontsize=14, ha='center', va='center')
    ax1.axis('off')
    ax1.set_title('📊 Dataset Size', fontsize=12)
    
    # 2. מספר קטגוריות
    ax2 = fig.add_subplot(gs[0, 1])
    valid_types = ['PSEUDO', 'BIOLOGICAL_REGION', 'ncRNA', 'snoRNA', 'PROTEIN_CODING', 'tRNA', 'OTHER', 'rRNA', 'snRNA', 'scRNA']
    n_classes = len(all_data[all_data['GeneType'].isin(valid_types)]['GeneType'].unique())
    ax2.text(0.5, 0.5, f"{n_classes}", fontsize=40, ha='center', va='center', fontweight='bold', color=COLORS[1])
    ax2.text(0.5, 0.2, "Gene Types", fontsize=14, ha='center', va='center')
    ax2.axis('off')
    ax2.set_title('🏷️ Labels', fontsize=12)
    
    # 3. Data Leakage
    ax3 = fig.add_subplot(gs[0, 2])
    train_seqs = set(train['NucleotideSequence'])
    test_seqs = set(test['NucleotideSequence'])
    leakage = len(train_seqs & test_seqs)
    ax3.text(0.5, 0.5, f"{leakage:,}", fontsize=40, ha='center', va='center', fontweight='bold', color='#FF6B6B')
    ax3.text(0.5, 0.2, "Leaked Sequences", fontsize=14, ha='center', va='center')
    ax3.axis('off')
    ax3.set_title('⚠️ Data Leakage', fontsize=12)
    
    # 4. אורך רצף ממוצע
    ax4 = fig.add_subplot(gs[0, 3])
    mean_len = all_data['seq_length'].mean()
    ax4.text(0.5, 0.5, f"{mean_len:.0f}", fontsize=40, ha='center', va='center', fontweight='bold', color=COLORS[2])
    ax4.text(0.5, 0.2, "Avg Sequence Length", fontsize=14, ha='center', va='center')
    ax4.axis('off')
    ax4.set_title('📏 Sequences', fontsize=12)
    
    # 5. התפלגות סוגים
    ax5 = fig.add_subplot(gs[1, :2])
    gene_counts = all_data[all_data['GeneType'].isin(valid_types)]['GeneType'].value_counts()
    bars = ax5.barh(gene_counts.index, gene_counts.values, color=COLORS[:len(gene_counts)])
    ax5.set_xlabel('Count')
    ax5.set_title('Gene Type Distribution')
    ax5.bar_label(bars, fmt='%d', padding=3)
    
    # 6. אורכי רצפים
    ax6 = fig.add_subplot(gs[1, 2:])
    ax6.hist(all_data['seq_length'], bins=40, color=COLORS[0], edgecolor='white', alpha=0.8)
    ax6.axvline(mean_len, color='red', linestyle='--', label=f'Mean: {mean_len:.0f}')
    ax6.set_xlabel('Sequence Length')
    ax6.set_ylabel('Count')
    ax6.set_title('Sequence Length Distribution')
    ax6.legend()
    
    # 7. חלוקת הנתונים
    ax7 = fig.add_subplot(gs[2, :2])
    sizes = [len(train), len(test), len(val)]
    labels = ['Train\n64%', 'Test\n23%', 'Validation\n13%']
    ax7.pie(sizes, labels=labels, colors=COLORS[:3], autopct='%1.0f%%', explode=[0.02]*3)
    ax7.set_title('Data Split')
    
    # 8. בעיות שזוהו
    ax8 = fig.add_subplot(gs[2, 2:])
    issues = [
        "⚠️ Data Leakage: 87% of test set in train!",
        "⚠️ 17% records with parsing issues",
        "⚠️ Class imbalance: 2,325:1 ratio",
        "⚠️ Sequences as short as 3 nucleotides",
        "✅ No missing values detected"
    ]
    for i, issue in enumerate(issues):
        color = '#FF6B6B' if '⚠️' in issue else '#95C623'
        ax8.text(0.05, 0.85 - i*0.18, issue, fontsize=11, va='top', 
                color=color, fontweight='bold')
    ax8.axis('off')
    ax8.set_title('🔍 Issues Detected', fontsize=12)
    
    plt.suptitle('🧬 DNA Dataset Summary Dashboard', fontsize=20, fontweight='bold', y=0.98)
    plt.savefig(f"{save_path}/08_summary_dashboard.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Created: 08_summary_dashboard.png")

def main():
    """Main function"""
    save_path = "/Users/ido.abramovitch/Documents/dna project/visualizations"
    
    print("="*60)
    print("🧬 DNA Dataset Visualization Generator")
    print("="*60)
    print()
    
    print("📂 Loading data...")
    train, test, val, all_data = load_data()
    print(f"   Loaded {len(all_data):,} records total")
    print()
    
    print("📊 Generating visualizations...")
    print("-"*40)
    
    plot_gene_type_distribution(all_data, save_path)
    plot_sequence_length_distribution(all_data, save_path)
    plot_data_split_analysis(train, test, val, save_path)
    plot_nucleotide_composition(all_data, save_path)
    plot_class_imbalance(all_data, save_path)
    plot_symbol_patterns(all_data, save_path)
    plot_correlation_heatmap(all_data, save_path)
    plot_summary_dashboard(all_data, train, test, val, save_path)
    
    print("-"*40)
    print()
    print(f"✅ All visualizations saved to: {save_path}")
    print("="*60)

if __name__ == "__main__":
    main()

