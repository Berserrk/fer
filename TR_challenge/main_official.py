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
    # Read the txt file
    with open('data/TRDataChallenge2023.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    print(f"File size: {len(content)} characters")

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
        # print("Sample JSON object:")
        # print(json.dumps(data[0], indent=2))
        
        print("\nKeys in the JSON objects:")
        all_keys = set()
        for obj in data:
            if isinstance(obj, dict):
                all_keys.update(obj.keys())
        
        for key in sorted(all_keys):
            print(f"- {key}")






    data = []
    lines = content.strip().split('\n')

    for i, line in enumerate(lines):
        if line.strip():
            try:
                json_obj = json.loads(line)

                # ➡️ Here: Process and combine text from sections
                sections = json_obj.get("sections", [])
                text_parts = []

                for sec in sections:
                    headtext = sec.get("headtext", "")
                    if headtext:
                        text_parts.append("[HEAD] " + headtext)
                    paragraphs = sec.get("paragraphs", [])
                    for para in paragraphs:
                        text_parts.append("[PARA] " + para)

                # Join sections with [SEP]
                full_text = " [SEP] ".join(text_parts)

                # Save new keys to the object
                json_obj["combined_text"] = full_text

                # Append to data list
                data.append(json_obj)

            except json.JSONDecodeError as e:
                print(f"Error parsing line {i+1}: {e}")
                print(f"Line content: {line[:100]}...")

    print(f"\nSuccessfully parsed {len(data)} JSON objects")

    # Example: print first processed document
    print("\nExample processed text:")
    print(data[0]["combined_text"][:1000])  # Print first 1000 characters to check



    df = pd.DataFrame([
        {
            "documentId": d["documentId"],
            "labels": d["postures"],
            "text": d["combined_text"]
        }
        for d in data
    ])

    print(df.head())

if __name__ == "__main__":
    main()