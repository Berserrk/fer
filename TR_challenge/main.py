#!/usr/bin/env python3
"""
TRDataChallenge2023 Analysis Script

This script analyzes the TRDataChallenge2023.txt file containing JSON dictionaries
of legal documents with comprehensive analysis including document structure,
legal postures, and multi-posture document patterns.
"""

import json
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    """Main analysis function"""
    
    print("TRDataChallenge2023 Analysis")
    print("=" * 50)
    
    # 1. Read and parse the data
    print("\n1. READING AND PARSING DATA")
    print("-" * 30)
    
    # Read the txt file
    with open('data/TRDataChallenge2023.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    print(f"File size: {len(content)} characters")
    print(f"First 500 characters:")
    print(content[:500])

    # Parse JSON dictionaries from the file
    data = []
    lines = content.strip().split('\n')

    for i, line in enumerate(lines):
        if line.strip():
            try:
                json_obj = json.loads(line)
                data.append(json_obj)
            except json.JSONDecodeError as e:
                print(f"Error parsing line {i+1}: {e}")
                print(f"Line content: {line[:100]}...")

    print(f"\nSuccessfully parsed {len(data)} JSON objects")

    # 2. Structure analysis
    print("\n2. DATA STRUCTURE ANALYSIS")
    print("-" * 30)
    
    if data:
        print("Sample JSON object:")
        print(json.dumps(data[0], indent=2))
        
        print("\nKeys in the JSON objects:")
        all_keys = set()
        for obj in data:
            if isinstance(obj, dict):
                all_keys.update(obj.keys())
        
        for key in sorted(all_keys):
            print(f"- {key}")

    # 3. Convert to DataFrame for easier analysis
    print("\n3. DATAFRAME CONVERSION")
    print("-" * 30)
    
    if data and isinstance(data[0], dict):
        df = pd.DataFrame(data)
        print(f"DataFrame shape: {df.shape}")
        print("\nDataFrame info:")
        df.info()
        print("\nFirst few rows:")
        print(df.head())
    else:
        print("Data is not in expected dictionary format")
        return

    # 4. Descriptive statistics and data exploration
    print("\n4. DESCRIPTIVE STATISTICS")
    print("-" * 30)
    
    if not df.empty:
        print("Missing values:")
        print(df.isnull().sum())
        
        print("\nData types:")
        print(df.dtypes)
        
        print(f"\nDataset Overview:")
        print(f"- Total documents: {len(df)}")
        print(f"- Unique document IDs: {df['documentId'].nunique()}")
        
        # Analyze postures column
        print(f"\nPostures Analysis:")
        all_postures = []
        num_empty_postures = (df['postures'].apply(lambda x: isinstance(x, list) and len(x) == 0)).sum()
        print(f"Documents with empty posture lists: {num_empty_postures}")
                
        posture_counts = Counter(all_postures)
        print(f"Total unique postures: {len(posture_counts)}")
        print("Most common postures:")
        for posture, count in posture_counts.most_common(10):
            print(f"  {posture}: {count}")
        
        # Analyze sections structure
        print(f"\nSections Analysis:")
        section_counts = []
        for sections in df['sections']:
            if isinstance(sections, list):
                section_counts.append(len(sections))
        
        if section_counts:
            print(f"Average sections per document: {np.mean(section_counts):.2f}")
            print(f"Min sections: {min(section_counts)}")
            print(f"Max sections: {max(section_counts)}")
            
        # Sample section analysis
        print(f"\nSample Section Structure:")
        if df['sections'].iloc[0] and isinstance(df['sections'].iloc[0], list):
            sample_section = df['sections'].iloc[0][0]
            if isinstance(sample_section, dict):
                print(f"Section keys: {list(sample_section.keys())}")
                if 'paragraphs' in sample_section and isinstance(sample_section['paragraphs'], list):
                    print(f"Paragraphs in first section: {len(sample_section['paragraphs'])}")
    else:
        print("DataFrame is not available or empty")

    # 5. Comprehensive counts
    print("\n5. DATASET COMPREHENSIVE COUNTS")
    print("-" * 30)

    # Count total documents
    total_documents = len(df)
    print(f"📄 Total Documents: {total_documents:,}")

    # Count unique postures across all documents
    all_postures = []
    for posture_list in df['postures']:
        if isinstance(posture_list, list):
            all_postures.extend(posture_list)

    unique_postures = set(all_postures)
    total_posture_instances = len(all_postures)
    print(f"⚖️  Total Posture Instances: {total_posture_instances:,}")
    print(f"⚖️  Unique Postures: {len(unique_postures):,}")

    # Count total paragraphs across all documents
    total_paragraphs = 0
    for sections_list in df['sections']:
        if isinstance(sections_list, list):
            for section in sections_list:
                if isinstance(section, dict) and 'paragraphs' in section:
                    if isinstance(section['paragraphs'], list):
                        total_paragraphs += len(section['paragraphs'])

    print(f"📝 Total Paragraphs: {total_paragraphs:,}")

    # Additional insights
    print(f"\nADDITIONAL INSIGHTS:")
    avg_postures_per_doc = total_posture_instances / total_documents
    avg_paragraphs_per_doc = total_paragraphs / total_documents

    print(f"📊 Average Postures per Document: {avg_postures_per_doc:.2f}")
    print(f"📊 Average Paragraphs per Document: {avg_paragraphs_per_doc:.2f}")

    # Documents with multiple postures
    multi_posture_docs_count = sum(1 for postures in df['postures'] if isinstance(postures, list) and len(postures) > 1)
    print(f"📊 Documents with Multiple Postures: {multi_posture_docs_count:,} ({(multi_posture_docs_count/total_documents)*100:.1f}%)")

    # Detailed posture count distribution
    print(f"\n📊 DOCUMENTS BY NUMBER OF POSTURES:")
    postures_per_document = []
    for postures in df['postures']:
        if isinstance(postures, list):
            postures_per_document.append(len(postures))
        else:
            postures_per_document.append(0)
    
    posture_distribution = Counter(postures_per_document)
    print(f"{'Postures':<12} {'Documents':<12} {'Percentage':<12}")
    print("-" * 36)
    
    for num_postures in sorted(posture_distribution.keys()):
        count = posture_distribution[num_postures]
        percentage = (count / total_documents) * 100
        posture_label = f"{num_postures} posture{'s' if num_postures != 1 else ''}"
        print(f"{posture_label:<12} {count:<12,} {percentage:<11.1f}%")
    
    print(f"\nSummary:")
    single_posture_count = posture_distribution.get(1, 0)
    multi_posture_total = sum(count for postures, count in posture_distribution.items() if postures > 1)
    print(f"• Single posture documents: {single_posture_count:,} ({(single_posture_count/total_documents)*100:.1f}%)")
    print(f"• Multi-posture documents: {multi_posture_total:,} ({(multi_posture_total/total_documents)*100:.1f}%)")
    print(f"• Maximum postures in one document: {max(postures_per_document)}")

    # Most common postures (top 10)
    posture_counts = Counter(all_postures)
    print(f"\n🏆 TOP 10 MOST COMMON POSTURES:")
    for i, (posture, count) in enumerate(posture_counts.most_common(10), 1):
        percentage = (count / total_posture_instances) * 100
        print(f"{i:2d}. {posture}: {count:,} ({percentage:.1f}%)")

    # 6. Multi-posture documents analysis
    print("\n6. MULTI-POSTURE DOCUMENTS ANALYSIS")
    print("-" * 30)

    # Find documents with multiple postures
    multi_posture_docs = []
    single_posture_docs = []

    for idx, postures in enumerate(df['postures']):
        if isinstance(postures, list):
            if len(postures) > 1:
                multi_posture_docs.append({
                    'index': idx,
                    'documentId': df.iloc[idx]['documentId'],
                    'postures': postures,
                    'num_postures': len(postures)
                })
            elif len(postures) == 1:
                single_posture_docs.append({
                    'index': idx,
                    'postures': postures
                })

    print(f"📊 Multi-posture documents: {len(multi_posture_docs):,}")
    print(f"📊 Single-posture documents: {len(single_posture_docs):,}")

    # Show examples of multi-posture documents
    print(f"\n🔍 EXAMPLES OF MULTI-POSTURE DOCUMENTS:")
    for i, doc in enumerate(multi_posture_docs[:10]):  # Show first 10 examples
        print(f"{i+1:2d}. Document ID: {doc['documentId']}")
        print(f"    Postures ({doc['num_postures']}): {', '.join(doc['postures'])}")
        print()

    # Distribution of number of postures per document
    posture_count_distribution = Counter([doc['num_postures'] for doc in multi_posture_docs])
    print(f"📈 DISTRIBUTION OF POSTURES IN MULTI-POSTURE DOCUMENTS:")
    for num_postures in sorted(posture_count_distribution.keys()):
        count = posture_count_distribution[num_postures]
        percentage = (count / len(multi_posture_docs)) * 100
        print(f"  {num_postures} postures: {count:,} documents ({percentage:.1f}%)")

    # Analyze which postures appear in multi-posture vs single-posture documents
    postures_in_multi = []
    postures_in_single = []

    for doc in multi_posture_docs:
        postures_in_multi.extend(doc['postures'])

    for doc in single_posture_docs:
        postures_in_single.extend(doc['postures'])

    # Count frequencies
    multi_posture_counts = Counter(postures_in_multi)
    single_posture_counts = Counter(postures_in_single)

    # All unique postures
    all_unique_postures = set(postures_in_multi + postures_in_single)

    # Calculate statistics for each posture
    posture_stats = {}
    for posture in all_unique_postures:
        multi_freq = multi_posture_counts.get(posture, 0)
        single_freq = single_posture_counts.get(posture, 0)
        total_freq = multi_freq + single_freq
        
        multi_percentage = (multi_freq / total_freq) * 100 if total_freq > 0 else 0
        
        posture_stats[posture] = {
            'multi_freq': multi_freq,
            'single_freq': single_freq,
            'total_freq': total_freq,
            'multi_percentage': multi_percentage
        }

    # Sort by multi-posture percentage (descending)
    sorted_by_multi = sorted(posture_stats.items(), key=lambda x: x[1]['multi_percentage'], reverse=True)

    print(f"\n🏆 TOP 15 POSTURES MOST INVOLVED IN MULTI-POSTURE DOCUMENTS:")
    print(f"{'Rank':<4} {'Posture':<40} {'Multi':<6} {'Single':<7} {'Total':<7} {'Multi%':<8}")
    print("-" * 80)

    for i, (posture, stats) in enumerate(sorted_by_multi[:15], 1):
        posture_short = posture[:38]
        multi_pct = f"{stats['multi_percentage']:.1f}%"
        print(f"{i:<4} {posture_short:<40} {stats['multi_freq']:<6} {stats['single_freq']:<7} {stats['total_freq']:<7} {multi_pct:<8}")

    # Sort by multi-posture percentage (ascending) - least involved
    sorted_by_single = sorted(posture_stats.items(), key=lambda x: x[1]['multi_percentage'])

    print(f"\n🏆 TOP 15 POSTURES LEAST INVOLVED IN MULTI-POSTURE DOCUMENTS:")
    print(f"{'Rank':<4} {'Posture':<40} {'Multi':<6} {'Single':<7} {'Total':<7} {'Multi%':<8}")
    print("-" * 80)

    for i, (posture, stats) in enumerate(sorted_by_single[:15], 1):
        posture_short = posture[:38]
        multi_pct = f"{stats['multi_percentage']:.1f}%"
        print(f"{i:<4} {posture_short:<40} {stats['multi_freq']:<6} {stats['single_freq']:<7} {stats['total_freq']:<7} {multi_pct:<8}")

    # Most common posture combinations in multi-posture documents
    print(f"\n🔗 MOST COMMON POSTURE COMBINATIONS:")
    combinations = [tuple(sorted(doc['postures'])) for doc in multi_posture_docs]
    combination_counts = Counter(combinations)

    for i, (combo, count) in enumerate(combination_counts.most_common(10), 1):
        percentage = (count / len(multi_posture_docs)) * 100
        print(f"{i:2d}. {' + '.join(combo)}")
        print(f"    Count: {count:,} ({percentage:.1f}% of multi-posture docs)")
        print()

    # 7. Visualizations
    print("\n7. GENERATING VISUALIZATIONS")
    print("-" * 30)
    
    # Create visualizations
    plt.figure(figsize=(15, 10))

    # Document length analysis
    document_lengths = []
    total_text_lengths = []

    for sections in df['sections']:
        if isinstance(sections, list):
            doc_length = len(sections)
            document_lengths.append(doc_length)
            
            # Calculate total text length
            total_text = 0
            for section in sections:
                if isinstance(section, dict) and 'paragraphs' in section:
                    for paragraph in section['paragraphs']:
                        if isinstance(paragraph, str):
                            total_text += len(paragraph)
            total_text_lengths.append(total_text)

        # Create DataFrame with documentId and text length
    document_lengths_df = pd.DataFrame({
        'documentId': df['documentId'],
        'text_length': total_text_lengths
    })

    # Print summary statistics per documentId
    print("\n📄 TEXT LENGTH STATISTICS PER DOCUMENT:")
    print(document_lengths_df.describe())

    # Optional: Save to CSV for further analysis
    document_lengths_df.to_csv('document_text_lengths.csv', index=False)

    # Example: Show top 10 longest documents
    longest_docs = document_lengths_df.sort_values(by='text_length', ascending=False).head(10)
    print("\n🔍 TOP 10 LONGEST DOCUMENTS BY TEXT LENGTH:")
    print(longest_docs)

    # Plot 1: Distribution of document lengths (number of sections)
    plt.subplot(2, 3, 1)
    plt.hist(document_lengths, bins=50, alpha=0.7, color='skyblue')
    plt.title('Distribution of Document Lengths\n(Number of Sections)')
    plt.xlabel('Number of Sections')
    plt.ylabel('Frequency')

    # Plot 2: Distribution of total text lengths
    plt.subplot(2, 3, 2)
    plt.hist(total_text_lengths, bins=50, alpha=0.7, color='lightgreen')
    plt.title('Distribution of Total Text Lengths\n(Characters)')
    plt.xlabel('Total Characters')
    plt.ylabel('Frequency')

    # Plot 3: Postures frequency
    plt.subplot(2, 3, 3)
    top_postures = dict(posture_counts.most_common(10))
    plt.barh(list(top_postures.keys()), list(top_postures.values()))
    plt.title('Top 10 Most Common Postures')
    plt.xlabel('Frequency')

    # Plot 4: Document length vs text length scatter
    plt.subplot(2, 3, 4)
    plt.scatter(document_lengths, total_text_lengths, alpha=0.5, color='orange')
    plt.title('Document Sections vs Total Text Length')
    plt.xlabel('Number of Sections')
    plt.ylabel('Total Characters')

    # Plot 5: Boxplot of text lengths by number of postures
    plt.subplot(2, 3, 5)
    postures_per_doc = [len(postures) if isinstance(postures, list) else 0 for postures in df['postures']]
    df_temp = pd.DataFrame({'postures_count': postures_per_doc, 'text_length': total_text_lengths})
    df_temp.boxplot(column='text_length', by='postures_count', ax=plt.gca())
    plt.title('Text Length Distribution by Number of Postures')
    plt.xlabel('Number of Postures')
    plt.ylabel('Text Length')

    # Plot 6: Cumulative distribution of document lengths
    plt.subplot(2, 3, 6)
    sorted_lengths = np.sort(document_lengths)
    cumulative_prob = np.arange(1, len(sorted_lengths) + 1) / len(sorted_lengths)
    plt.plot(sorted_lengths, cumulative_prob, color='red')
    plt.title('Cumulative Distribution of Document Lengths')
    plt.xlabel('Number of Sections')
    plt.ylabel('Cumulative Probability')

    plt.tight_layout()
    plt.savefig('legal_documents_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

    # Summary statistics
    print("\nSUMMARY STATISTICS:")
    print(f"Document Lengths (sections):")
    print(f"  Mean: {np.mean(document_lengths):.2f}")
    print(f"  Median: {np.median(document_lengths):.2f}")
    print(f"  Std: {np.std(document_lengths):.2f}")

    print(f"\nText Lengths (characters):")
    print(f"  Mean: {np.mean(total_text_lengths):,.0f}")
    print(f"  Median: {np.median(total_text_lengths):,.0f}")
    print(f"  Std: {np.std(total_text_lengths):,.0f}")

    print(f"\nPostures per Document:")
    print(f"  Mean: {np.mean(postures_per_doc):.2f}")
    print(f"  Median: {np.median(postures_per_doc):.2f}")
    print(f"  Most common count: {Counter(postures_per_doc).most_common(1)[0]}")

    # 8. Final analysis summary
    print("\n8. ANALYSIS SUMMARY")
    print("-" * 30)
    
    print(f"📋 FINAL SUMMARY:")
    print(f"Total unique postures: {len(all_unique_postures):,}")
    print(f"Postures appearing in multi-posture docs: {len([p for p in posture_stats if posture_stats[p]['multi_freq'] > 0]):,}")
    print(f"Postures only in single-posture docs: {len([p for p in posture_stats if posture_stats[p]['multi_freq'] == 0]):,}")
    if sorted_by_multi:
        print(f"Most multi-posture prone: {sorted_by_multi[0][0]} ({sorted_by_multi[0][1]['multi_percentage']:.1f}%)")
    if sorted_by_single:
        print(f"Least multi-posture prone: {sorted_by_single[0][0]} ({sorted_by_single[0][1]['multi_percentage']:.1f}%)")

    # Generate comprehensive analysis request
    analysis_request = """
    COMPREHENSIVE ANALYSIS REQUEST FOR TRDataChallenge2023 LEGAL DOCUMENTS DATASET

    Based on the exploration of the legal documents dataset containing 18,000 legal case documents, 
    this analysis provides insights into:

    1. LEGAL DOCUMENT STRUCTURE ANALYSIS
    2. LEGAL POSTURES AND PROCEDURAL ANALYSIS  
    3. CONTENT AND TEXT ANALYSIS
    4. COMPARATIVE ANALYSIS
    5. LEGAL INSIGHTS AND PATTERNS
    6. VISUALIZATIONS AND REPORTING
    7. DATASET QUALITY AND RECOMMENDATIONS

    The dataset contains rich legal document information suitable for:
    - Legal document classification by posture/procedure type
    - Court decision analysis and pattern recognition
    - Legal text mining and information extraction
    - Comparative legal procedure analysis
    - Legal document complexity scoring
    """

    print(f"\n{analysis_request}")
    print(f"\nAnalysis completed successfully!")
    print(f"Visualization saved as 'legal_documents_analysis.png'")

if __name__ == "__main__":
    main()