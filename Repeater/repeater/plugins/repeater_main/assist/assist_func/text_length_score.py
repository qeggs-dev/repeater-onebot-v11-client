from ...client_configs import storage_configs

def text_length_score(text: str) -> float:
    if not text:
        return 0.0
    
    config = storage_configs.text_length_score_configs
    
    # 单次遍历统计
    max_line_length: int = 0
    total_chars_in_lines: int = 0  # 所有行中非换行符字符总数
    line_count: int = 0
    current_line_length: int = 0
    
    for char in text:
        if char == "\n":
            # 当前行结束
            if current_line_length > max_line_length:
                max_line_length = current_line_length
            total_chars_in_lines += current_line_length
            line_count += 1
            current_line_length = 0
        else:
            current_line_length += 1
    
    # 处理最后一行（如果文本不以换行符结尾）
    if current_line_length > 0 or (text and text[-1] == '\n'):
        # 两种情况：
        # 1. current_line_length > 0: 最后有内容
        # 2. text[-1] == '\n': 最后是空行（current_line_length=0但算一行）
        if current_line_length > max_line_length:
            max_line_length = current_line_length
        total_chars_in_lines += current_line_length
        line_count += 1
    
    # 如果line_count为0（理论上不会发生，因为text不为空）
    if line_count == 0:
        return 0.0
    
    # 计算统计值
    mean_line_length: float = total_chars_in_lines / line_count
    total_length: int = len(text)  # 直接使用len，避免重复计算
    
    # 计算各项得分
    lines_score: float = line_count / config.max_lines
    max_single_line_score: float = max_line_length / config.single_line_max
    mean_line_score: float = mean_line_length / config.mean_line_max
    total_length_score: float = total_length / config.total_length
    
    # 综合得分（加权平均）
    return (
        lines_score +
        (
            max_single_line_score
            +
            mean_line_score
        ) / 2.0 +
        total_length_score
    ) / 3.0