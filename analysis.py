import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================
# Step 1: Data Load Karo
# ============================================
print("Data load kar rahe hain...")

# Aadhaar data CSV file se load karo
# (iska file naam apna actual filename hona chahiye)
df = pd.read_csv('data/aadhaar_enrollment.csv')

print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")

# ============================================
# Step 2: Data Explore Karo
# ============================================
print("\n" + "="*50)
print("DATA OVERVIEW")
print("="*50)

# Pehle 5 rows dekho
print("\nPehle 5 rows:")
print(df.head())

# Column names dekho
print("\nColumn names:")
print(df.columns.tolist())

# Data types dekho
print("\nData types:")
print(df.dtypes)

# ============================================
# Step 3: Basic Statistics
# ============================================
print("\n" + "="*50)
print("BASIC ANALYSIS")
print("="*50)

# Kitne null values hain?
print("\nMissing values per column:")
print(df.isnull().sum())

# Gender distribution
if 'gender' in df.columns:
    print("\nGender Distribution:")
    print(df['gender'].value_counts())

# Age distribution
if 'age' in df.columns:
    print("\nAge Statistics:")
    print(df['age'].describe())

# State-wise count
if 'state' in df.columns:
    print("\nTop 10 States by enrollment:")
    print(df['state'].value_counts().head(10))

# ============================================
# Step 4: Simple Visualization
# ============================================
if 'gender' in df.columns:
    plt.figure(figsize=(8, 5))
    df['gender'].value_counts().plot(kind='bar')
    plt.title('Gender Distribution in Aadhaar')
    plt.xlabel('Gender')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('visualizations/gender_distribution.png')  # Save hote hai
    plt.show()

print("\n✓ Analysis complete! Check visualizations/gender_distribution.png")
