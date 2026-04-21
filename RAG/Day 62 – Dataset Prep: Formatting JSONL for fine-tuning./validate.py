import json

# Step 1: Validate single example
def validate_example(example):
    required_fields = ["instruction", "input", "output"]
    for field in required_fields:
        if field not in example:
            return False, f"Missing field: {field}"
    return True, "Valid"

# Step 2: Validate entire JSONL file
def validate_jsonl(filepath):
    errors = []
    valid_count = 0

    with open(filepath, "r") as f:
        for i, line in enumerate(f):
            try:
                example = json.loads(line)
                is_valid, msg = validate_example(example)
                if not is_valid:
                    errors.append(f"Line {i+1}: {msg}")
                else:
                    valid_count += 1
            except json.JSONDecodeError:
                errors.append(f"Line {i+1}: Invalid JSON")

    # Step 3: Print results
    print(f"\n✅ Valid examples: {valid_count}")
    print(f"❌ Errors found: {len(errors)}")
    if errors:
        for error in errors:
            print(f"   → {error}")
    else:
        print("🎉 Dataset is clean and ready for fine-tuning!")

# Run it
validate_jsonl("train.jsonl")