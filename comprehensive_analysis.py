import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os

# Styling
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

print("="*80)
print("COMPREHENSIVE AADHAAR DATA ANALYSIS")
print("="*80)

# ============================================
# LOAD ALL DATA
# ============================================
print("\n📊 LOADING DATA...")

# Load Biometric Data
print("\n1. Biometric Data:")
biometric_files = glob.glob('data/api_data_aadhar_biometric/**/*.csv', recursive=True)
biometric_list = [pd.read_csv(f) for f in sorted(biometric_files)]
biometric = pd.concat(biometric_list, ignore_index=True)
print(f"   ✓ {len(biometric):,} records loaded")
print(f"   Columns: {list(biometric.columns)}")

# Load Demographic Data
print("\n2. Demographic Data:")
demographic_files = glob.glob('data/api_data_aadhar_demographic/**/*.csv', recursive=True)
demographic_list = [pd.read_csv(f) for f in sorted(demographic_files)]
demographic = pd.concat(demographic_list, ignore_index=True)
print(f"   ✓ {len(demographic):,} records loaded")
print(f"   Columns: {list(demographic.columns)}")

# Load Enrolment Data
print("\n3. Enrolment Data:")
enrolment_files = glob.glob('data/api_data_aadhar_enrolment/**/*.csv', recursive=True)
enrolment_list = [pd.read_csv(f) for f in sorted(enrolment_files)]
enrolment = pd.concat(enrolment_list, ignore_index=True)
print(f"   ✓ {len(enrolment):,} records loaded")
print(f"   Columns: {list(enrolment.columns)}")

# ============================================
# DATASET OVERVIEW
# ============================================
print("\n" + "="*80)
print("📋 DATASET OVERVIEW")
print("="*80)

datasets = {
    'Biometric': biometric,
    'Demographic': demographic,
    'Enrolment': enrolment
}

for name, df in datasets.items():
    print(f"\n--- {name.upper()} DATA ---")
    print(f"Total Rows: {len(df):,}")
    print(f"Total Columns: {len(df.columns)}")
    print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"Missing Values: {df.isnull().sum().sum():,}")
    print(f"\nColumn Info:")
    print(df.dtypes)

# ============================================
# ANALYSIS 1: BIOMETRIC DATA ANALYSIS
# ============================================
print("\n" + "="*80)
print("👁️ BIOMETRIC DATA ANALYSIS")
print("="*80)

print("\nFirst 5 rows:")
print(biometric.head())

print("\nBasic Statistics:")
print(biometric.describe())

# Check for common biometric columns
if 'fingerprint_quality' in biometric.columns or any('quality' in col.lower() for col in biometric.columns):
    print("\n📊 Quality Metrics Found!")
    
# Save biometric summary
biometric.describe().to_csv('visualizations/biometric_summary.csv')
print("\n✓ Saved: visualizations/biometric_summary.csv")

# ============================================
# ANALYSIS 2: DEMOGRAPHIC DATA ANALYSIS
# ============================================
print("\n" + "="*80)
print("👥 DEMOGRAPHIC DATA ANALYSIS")
print("="*80)

print("\nFirst 5 rows:")
print(demographic.head())

# Gender Analysis (if available)
gender_cols = [col for col in demographic.columns if 'gender' in col.lower()]
if gender_cols:
    print(f"\n📊 Gender Distribution (using {gender_cols[0]}):")
    gender_dist = demographic[gender_cols[0]].value_counts()
    print(gender_dist)
    
    # Plot gender distribution
    plt.figure(figsize=(10, 6))
    gender_dist.plot(kind='bar', color=['#3498db', '#e74c3c', '#95a5a6'])
    plt.title('Gender Distribution in Aadhaar Data', fontsize=16, fontweight='bold')
    plt.xlabel('Gender')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('visualizations/gender_distribution.png', dpi=300)
    plt.close()
    print("✓ Saved: visualizations/gender_distribution.png")

# Age Analysis (if available)
age_cols = [col for col in demographic.columns if 'age' in col.lower()]
if age_cols:
    print(f"\n📊 Age Statistics (using {age_cols[0]}):")
    print(demographic[age_cols[0]].describe())
    
    # Plot age distribution
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Histogram
    ax1.hist(demographic[age_cols[0]].dropna(), bins=50, color='green', alpha=0.7, edgecolor='black')
    ax1.set_title('Age Distribution', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Age')
    ax1.set_ylabel('Frequency')
    ax1.grid(True, alpha=0.3)
    
    # Box plot
    ax2.boxplot(demographic[age_cols[0]].dropna(), vert=True)
    ax2.set_title('Age Box Plot', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Age')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('visualizations/age_analysis.png', dpi=300)
    plt.close()
    print("✓ Saved: visualizations/age_analysis.png")

# State Analysis (if available)
state_cols = [col for col in demographic.columns if 'state' in col.lower()]
if state_cols:
    print(f"\n📊 Top 15 States (using {state_cols[0]}):")
    state_dist = demographic[state_cols[0]].value_counts().head(15)
    print(state_dist)
    
    # Plot state distribution
    plt.figure(figsize=(14, 8))
    state_dist.plot(kind='barh', color='skyblue')
    plt.title('Top 15 States by Aadhaar Records', fontsize=16, fontweight='bold')
    plt.xlabel('Number of Records')
    plt.ylabel('State')
    plt.tight_layout()
    plt.savefig('visualizations/state_distribution.png', dpi=300)
    plt.close()
    print("✓ Saved: visualizations/state_distribution.png")

# ============================================
# ANALYSIS 3: ENROLMENT DATA ANALYSIS
# ============================================
print("\n" + "="*80)
print("📝 ENROLMENT DATA ANALYSIS")
print("="*80)

print("\nFirst 5 rows:")
print(enrolment.head())

# Date analysis (if available)
date_cols = [col for col in enrolment.columns if 'date' in col.lower() or 'time' in col.lower()]
if date_cols:
    print(f"\n📊 Date Column Found: {date_cols}")
    for date_col in date_cols:
        try:
            enrolment[date_col] = pd.to_datetime(enrolment[date_col])
            print(f"\n{date_col} Statistics:")
            print(f"Earliest: {enrolment[date_col].min()}")
            print(f"Latest: {enrolment[date_col].max()}")
            print(f"Date Range: {(enrolment[date_col].max() - enrolment[date_col].min()).days} days")
            
            # Enrolment over time
            enrolment_by_date = enrolment.groupby(enrolment[date_col].dt.date).size()
            
            plt.figure(figsize=(14, 6))
            enrolment_by_date.plot(kind='line', color='purple', linewidth=2)
            plt.title('Enrolments Over Time', fontsize=16, fontweight='bold')
            plt.xlabel('Date')
            plt.ylabel('Number of Enrolments')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig('visualizations/enrolment_timeline.png', dpi=300)
            plt.close()
            print("✓ Saved: visualizations/enrolment_timeline.png")
            break
        except:
            pass

# ============================================
# CROSS-DATASET ANALYSIS
# ============================================
print("\n" + "="*80)
print("🔗 CROSS-DATASET INSIGHTS")
print("="*80)

print(f"\nTotal Records Across All Datasets:")
print(f"  - Biometric: {len(biometric):,}")
print(f"  - Demographic: {len(demographic):,}")
print(f"  - Enrolment: {len(enrolment):,}")

# ============================================
# KEY INSIGHTS SUMMARY
# ============================================
print("\n" + "="*80)
print("🎯 KEY INSIGHTS SUMMARY")
print("="*80)

print(f"\n📊 Dataset Statistics:")
print(f"  ✓ Total Biometric Records: {len(biometric):,}")
print(f"  ✓ Total Demographic Records: {len(demographic):,}")
print(f"  ✓ Total Enrolment Records: {len(enrolment):,}")
print(f"  ✓ Total Combined Records: {len(biometric) + len(demographic) + len(enrolment):,}")

if gender_cols:
    print(f"\n👥 Demographics:")
    gender_dist = demographic[gender_cols[0]].value_counts()
    for gender, count in gender_dist.items():
        pct = (count / len(demographic)) * 100
        print(f"  ✓ {gender}: {count:,} ({pct:.1f}%)")

if state_cols:
    top_state = demographic[state_cols[0]].value_counts().index[0]
    top_state_count = demographic[state_cols[0]].value_counts().values[0]
    print(f"\n🗺️ Geographic:")
    print(f"  ✓ Top State: {top_state} ({top_state_count:,} records)")
    print(f"  ✓ Total States: {demographic[state_cols[0]].nunique()}")

print(f"\n📅 Analysis Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")

print("\n" + "="*80)
print("✅ ANALYSIS COMPLETE!")
print("="*80)
print("\nGenerated Visualizations:")
print("  - visualizations/gender_distribution.png")
print("  - visualizations/age_analysis.png")
print("  - visualizations/state_distribution.png")
print("  - visualizations/enrolment_timeline.png")
print("  - visualizations/biometric_summary.csv")
print("\nAll analysis complete! Check the visualizations folder for charts.")
