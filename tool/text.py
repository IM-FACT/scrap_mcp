from trafilatura import fetch_url, extract
import re

def keyword_context(origin: str, keyword: str, context_range: int):
    try:   
        key_pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        matche_idxs = [(m.start(), m.end()) for m in key_pattern.finditer(origin)]

        print(matche_idxs)
        
        if not matche_idxs:
            return []
        
        contexts = []
        for s_idx, e_idx in matche_idxs:
            s_context = max(0, s_idx - context_range)
            e_context = min(len(origin), e_idx + context_range)
            contexts.append((s_context, e_context))
        
        merged_contexts = []
        contexts.sort()
        
        for start, end in contexts:
            if merged_contexts and start <= merged_contexts[-1][1]:
                merged_contexts[-1] = (merged_contexts[-1][0], max(merged_contexts[-1][1], end))
            else:
                merged_contexts.append((start, end))
        
        extracted = []
        results = []
        for start, end in merged_contexts:
            extracted = origin[start:end]
            
            words = extracted.split()
            if len(words) > 1:
                if start > 0:
                    words = words[1:]
                if end < len(origin):
                    words = words[:-1]
            
            if words:
                results.append(' '.join(words))
            if not results:
                results.append("No results found")
        return results
    
    except Exception as e:
        return str(e)

def center_context(origin: list, max_length: int):
    if len(origin) <= max_length:
        return origin

    center = len(origin) // 2
    half_length = max_length // 2
    
    start = max(0, center - half_length)
    end = min(len(origin), center + half_length)
    
    if end - start < max_length:
        if start == 0: 
            end = min(len(origin), start + max_length)
        elif end == len(origin):
            start = max(0, end - max_length)
    
    extracted = origin[start:end]
    
    if not extracted:
        return "No results found"
    return extracted

def use_tra(url: str, max_length: int = 1500, context_length: int = 200, keyword: str = "default"):
    try:
        html = fetch_url(url)
        text = extract(html)
        if text is None:
            return "No results found"

        if keyword != "default":
            return keyword_context(text, keyword, context_length)
        else:
            return center_context(text, max_length)
        
    except Exception as e:
        return str(e)
    

if __name__ == "__main__":
    print(use_tra("https://greatjoy.tistory.com/72", keyword="fraction"))