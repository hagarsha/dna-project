"""
DNA Data Summary Report Generator
Generates a comprehensive summary of variables and labels from the DNA dataset
"""

import pandas as pd
import os

def generate_summary_report():
    # Load the datasets
    data_dir = "/Users/ido.abramovitch/Documents/dna project"
    
    print("=" * 80)
    print("דוח מסכם - נתוני DNA")
    print("DNA Dataset Summary Report")
    print("=" * 80)
    print()
    
    # Load all three datasets
    train_df = pd.read_csv(os.path.join(data_dir, "train.csv"), index_col=0)
    test_df = pd.read_csv(os.path.join(data_dir, "test.csv"), index_col=0)
    val_df = pd.read_csv(os.path.join(data_dir, "validation.csv"), index_col=0)
    
    # ========== SECTION 1: Dataset Overview ==========
    print("=" * 80)
    print("1. סקירת הנתונים | Dataset Overview")
    print("=" * 80)
    print()
    
    print(f"{'קובץ':<20} | {'מספר שורות':<15} | {'מספר עמודות':<15}")
    print(f"{'File':<20} | {'Rows':<15} | {'Columns':<15}")
    print("-" * 60)
    print(f"{'train.csv':<20} | {len(train_df):<15,} | {len(train_df.columns):<15}")
    print(f"{'test.csv':<20} | {len(test_df):<15,} | {len(test_df.columns):<15}")
    print(f"{'validation.csv':<20} | {len(val_df):<15,} | {len(val_df.columns):<15}")
    print("-" * 60)
    print(f"{'סה\"כ | Total':<20} | {len(train_df) + len(test_df) + len(val_df):<15,} |")
    print()
    
    # ========== SECTION 2: Variables (Columns) ==========
    print("=" * 80)
    print("2. משתנים (עמודות) | Variables (Columns)")
    print("=" * 80)
    print()
    
    columns = train_df.columns.tolist()
    print(f"מספר משתנים: {len(columns)}")
    print(f"Number of variables: {len(columns)}")
    print()
    
    for i, col in enumerate(columns, 1):
        dtype = train_df[col].dtype
        non_null = train_df[col].notna().sum()
        null_count = train_df[col].isna().sum()
        unique = train_df[col].nunique()
        
        print(f"{i}. {col}")
        print(f"   סוג: {dtype} | Type: {dtype}")
        print(f"   ערכים ייחודיים: {unique:,} | Unique values: {unique:,}")
        print(f"   ערכים חסרים: {null_count:,} | Missing values: {null_count:,}")
        print()
    
    # ========== SECTION 3: Label Analysis (GeneType) ==========
    print("=" * 80)
    print("3. ניתוח התיוגים (GeneType) | Label Analysis (GeneType)")
    print("=" * 80)
    print()
    
    # Combine all datasets for comprehensive label analysis
    all_data = pd.concat([train_df, test_df, val_df], ignore_index=True)
    
    print("התפלגות התיוגים בכל הנתונים:")
    print("Label distribution across all data:")
    print()
    
    gene_type_counts = all_data['GeneType'].value_counts()
    total_samples = len(all_data)
    
    print(f"{'GeneType':<30} | {'כמות':<12} | {'אחוז':<10}")
    print(f"{'GeneType':<30} | {'Count':<12} | {'Percent':<10}")
    print("-" * 60)
    
    for gene_type, count in gene_type_counts.items():
        pct = (count / total_samples) * 100
        print(f"{gene_type:<30} | {count:<12,} | {pct:<10.2f}%")
    
    print("-" * 60)
    print(f"{'סה\"כ | Total':<30} | {total_samples:<12,} | {'100.00':<10}%")
    print()
    
    # Label distribution per dataset
    print("התפלגות התיוגים לפי קובץ:")
    print("Label distribution by file:")
    print()
    
    datasets = {
        'train.csv': train_df,
        'test.csv': test_df,
        'validation.csv': val_df
    }
    
    gene_types = gene_type_counts.index.tolist()
    
    # Print header
    header = f"{'GeneType':<25}"
    for ds_name in datasets.keys():
        header += f" | {ds_name:<15}"
    print(header)
    print("-" * (25 + 18 * len(datasets)))
    
    for gt in gene_types:
        row = f"{gt:<25}"
        for ds_name, ds in datasets.items():
            count = (ds['GeneType'] == gt).sum()
            row += f" | {count:<15,}"
        print(row)
    
    print()
    
    # ========== SECTION 4: GeneGroupMethod Analysis ==========
    print("=" * 80)
    print("4. ניתוח GeneGroupMethod | GeneGroupMethod Analysis")
    print("=" * 80)
    print()
    
    method_counts = all_data['GeneGroupMethod'].value_counts()
    
    print(f"{'GeneGroupMethod':<30} | {'כמות':<12} | {'אחוז':<10}")
    print(f"{'GeneGroupMethod':<30} | {'Count':<12} | {'Percent':<10}")
    print("-" * 60)
    
    for method, count in method_counts.items():
        pct = (count / total_samples) * 100
        print(f"{method:<30} | {count:<12,} | {pct:<10.2f}%")
    
    print()
    
    # ========== SECTION 5: Sequence Analysis ==========
    print("=" * 80)
    print("5. ניתוח רצפי DNA | DNA Sequence Analysis")
    print("=" * 80)
    print()
    
    # Calculate sequence lengths (removing < and > markers)
    def get_seq_length(seq):
        if pd.isna(seq):
            return 0
        seq = str(seq).strip('<>').strip()
        return len(seq)
    
    all_data['seq_length'] = all_data['NucleotideSequence'].apply(get_seq_length)
    
    print("סטטיסטיקות אורך הרצפים:")
    print("Sequence length statistics:")
    print()
    print(f"  אורך מינימלי | Min length:    {all_data['seq_length'].min():,}")
    print(f"  אורך מקסימלי | Max length:    {all_data['seq_length'].max():,}")
    print(f"  אורך ממוצע | Mean length:     {all_data['seq_length'].mean():,.2f}")
    print(f"  חציון | Median length:        {all_data['seq_length'].median():,.0f}")
    print(f"  סטיית תקן | Std deviation:   {all_data['seq_length'].std():,.2f}")
    print()
    
    # Sequence length by GeneType
    print("אורך רצף ממוצע לפי סוג גן:")
    print("Average sequence length by GeneType:")
    print()
    
    seq_by_type = all_data.groupby('GeneType')['seq_length'].agg(['mean', 'min', 'max', 'count'])
    seq_by_type = seq_by_type.sort_values('count', ascending=False)
    
    print(f"{'GeneType':<25} | {'ממוצע':<10} | {'מינ':<8} | {'מקס':<10} | {'כמות':<10}")
    print(f"{'GeneType':<25} | {'Mean':<10} | {'Min':<8} | {'Max':<10} | {'Count':<10}")
    print("-" * 75)
    
    for gt, row in seq_by_type.iterrows():
        print(f"{gt:<25} | {row['mean']:<10.1f} | {row['min']:<8.0f} | {row['max']:<10.0f} | {row['count']:<10.0f}")
    
    print()
    
    # ========== SECTION 6: Sample Data ==========
    print("=" * 80)
    print("6. דוגמאות מהנתונים | Sample Data")
    print("=" * 80)
    print()
    
    print("5 שורות ראשונות מקובץ train.csv:")
    print("First 5 rows from train.csv:")
    print()
    
    sample_df = train_df.head().copy()
    sample_df['NucleotideSequence'] = sample_df['NucleotideSequence'].apply(
        lambda x: str(x)[:50] + '...' if len(str(x)) > 50 else x
    )
    print(sample_df.to_string())
    print()
    
    # ========== SUMMARY ==========
    print("=" * 80)
    print("סיכום | Summary")
    print("=" * 80)
    print()
    print(f"• סה\"כ דגימות: {total_samples:,}")
    print(f"  Total samples: {total_samples:,}")
    print()
    print(f"• מספר סוגי גנים (תיוגים): {len(gene_type_counts)}")
    print(f"  Number of gene types (labels): {len(gene_type_counts)}")
    print()
    print(f"• סוג הגן הנפוץ ביותר: {gene_type_counts.index[0]} ({gene_type_counts.iloc[0]:,} דגימות)")
    print(f"  Most common gene type: {gene_type_counts.index[0]} ({gene_type_counts.iloc[0]:,} samples)")
    print()
    print(f"• אורך רצף ממוצע: {all_data['seq_length'].mean():.1f} נוקלאוטידים")
    print(f"  Average sequence length: {all_data['seq_length'].mean():.1f} nucleotides")
    print()
    
    print("=" * 80)
    print("סוף הדוח | End of Report")
    print("=" * 80)

if __name__ == "__main__":
    generate_summary_report()

