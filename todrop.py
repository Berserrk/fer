def merge_connected_entries(dictionary):
    """
    Merges dictionary entries that share common names.
    
    Args:
        dictionary: A dictionary with keys mapping to lists of names
        
    Returns:
        A new dictionary with connected entries merged
    """
    # Map each name to all keys it appears in
    name_to_keys = {}
    for key, names in dictionary.items():
        for name in names:
            if name not in name_to_keys:
                name_to_keys[name] = []
            name_to_keys[name].append(key)
    
    # Track which keys have been processed
    processed_keys = set()
    result = {}
    
    # Process each key
    for key in dictionary:
        # Skip if already processed
        if key in processed_keys:
            continue
        
        # Start with current key and its names
        connected_keys = [key]
        connected_names = set(dictionary[key])
        
        # Find all connected keys through common names
        changed = True
        while changed:
            changed = False
            
            # For current set of names, find all related keys
            for name in list(connected_names):
                for related_key in name_to_keys[name]:
                    if related_key not in connected_keys:
                        connected_keys.append(related_key)
                        # Add all names from this key
                        for related_name in dictionary[related_key]:
                            if related_name not in connected_names:
                                connected_names.add(related_name)
                                changed = True
        
        # Mark all these keys as processed
        for k in connected_keys:
            processed_keys.add(k)
        
        # Add to result using the first key
        result[key] = list(connected_names)
    
    return result

# Example usage
if __name__ == "__main__":
    dic_a = {
        "match1": ["name1", "name2"],
        "match2": ["name2", "name3"],
        "match3": ["name5", "name4"]
    }
    
    new_dic_a = merge_connected_entries(dic_a)
    print("Original dictionary:", dic_a)
    print("New dictionary:", new_dic_a)
