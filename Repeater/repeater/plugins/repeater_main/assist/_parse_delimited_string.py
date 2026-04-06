def parse_delimited_string(expression: str, delimiters: list[str] | None = None) -> list[str]:
    r"""
    解析以指定分隔符分隔的字符串，返回子串数组
    
    参数:
        expression: 待解析的字符串
        delimiters: 分隔符列表，默认为 ['|', ',', ';', '/', '\n']
    
    规则:
    - 以字符串中第一个出现的分隔符（在 delimiters 中）作为整个字符串的分隔符
    - 其他分隔符被视为普通字符
    - 连续的分隔符会被忽略（不产生空字符串）
    """
    if not expression or not isinstance(expression, str):
        return []
    
    # 默认分隔符
    if delimiters is None:
        delimiters = ["|", ",", ";", "/", "\n"]
    
    if not delimiters:
        return [expression.strip()] if expression.strip() else []
    
    # 查找第一个出现的分隔符
    first_pos = -1
    first_delimiter = None
    
    for delim in delimiters:
        pos = expression.find(delim)
        if pos != -1 and (first_pos == -1 or pos < first_pos):
            first_pos = pos
            first_delimiter = delim
    
    # 没有找到任何分隔符
    if first_delimiter is None:
        return [expression.strip()] if expression.strip() else []
    
    # 使用选定的分隔符分割
    parts = expression.split(first_delimiter)
    
    # 清理并过滤空字符串
    result = []
    for part in parts:
        cleaned = part.strip()
        if cleaned:  # 排除空字符串（连续分隔符产生的）
            result.append(cleaned)
    
    return result