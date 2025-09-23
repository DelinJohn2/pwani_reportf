import re, json

def extract_json_blocks(text):
    """Extract and parse JSON code blocks from markdown text"""
    blocks = re.findall(r'```json(.*?)```', text, re.DOTALL | re.IGNORECASE)
    results = []
    for block in blocks:
        cleaned = re.sub(r'//.*', '', block)              # remove // comments
        cleaned = re.sub(r'(\d),(\d)', r'\1\2', cleaned)  # remove commas in numbers
        try:
            results.append({"valid": True, "json_dict": json.loads(cleaned.strip())})
        except Exception as e:
            results.append({"valid": False, "error": str(e)})
    return {p['json_dict']['chart_type']: p['json_dict']['data'] 
            for p in results if p['valid']}
