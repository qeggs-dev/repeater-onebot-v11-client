def split_by_indent(
    text: str,
    indent: int = 2,
    indent_char: str = " "
) -> list[str]:
    lines: list[str] = text.splitlines()
    results: list[str] = []
    lines_iter = iter(lines)
    for line in lines_iter:
        if not line:
            continue
        if line.startswith(indent_char * indent):
            sub_lines: list[str] = []
            last_result: str = ""
            sub_lines.append(line.removeprefix(indent_char * indent))
            for sub_line in lines_iter:
                if sub_line.startswith(indent_char * indent):
                    sub_lines.append(sub_line.removeprefix(indent_char * indent))
                else:
                    last_result = sub_line
                    break
            if lines:
                results[-1] += "\n" + "\n".join(sub_lines)
            else:
                results.append("\n".join(sub_lines))
            results.append(last_result)
        else:
            results.append(line)
    return results