def render_progress(count: int):
    complete = '✅'
    empty = '◻'
    progress_bar = complete*count
    for i in range(1+count, 22):
        progress_bar += empty
        if i % 7 == 0:
            progress_bar += '\n'
    return progress_bar.strip()
