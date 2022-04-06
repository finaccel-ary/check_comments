import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args()

    errors = []
    for filename in args.filenames:
       percentage = check_file(filename, args)
       if (percentage<20):
           errors.append(TypeError(f"{filename} ({percentage}%) comments less than 20%"))
    
    if len(errors) > 0:
        return errors
    
    return 0

def using_quote(filename:str):
    # count lines
    count_lines        = 0
    line_have_comments = 0
    on_comments        = False
    with open(filename, 'rb') as fb:    
        for line in fb:
            count_lines += 1
            
            # check comments
            if '"""' in line.decode() or "'''" in line.decode():
                # check if 1 line have comments
                count_tuple = 0
                for l in line.decode():
                    if l == '"' or l == "'":
                        count_tuple += 1
                
                if count_tuple == 6:
                    line_have_comments +=1
                elif count_tuple == 3:
                    # set on comments
                    if on_comments == False:
                        on_comments = True
                    else:
                        line_have_comments +=1
                        on_comments = False
            
            # check comments on 
            if on_comments == True:
                line_have_comments +=1
    
    return {
        'count_lines'       : count_lines,
        'line_have_comments': line_have_comments
    }

def using_hashtag(filename:str):
    # count lines
    count_lines        = 0
    line_have_comments = 0
    with open(filename, 'rb') as fb:    
        for line in fb:
            count_lines += 1
            
            # check comments
            if "#" in line.decode():
                line_have_comments +=1
    
    return {
        'count_lines'       : count_lines,
        'line_have_comments': line_have_comments
    }

def using_dash(filename:str):
    # count lines
    count_lines        = 0
    line_have_comments = 0
    with open(filename, 'rb') as fb:    
        for line in fb:
            count_lines += 1
            
            # check comments
            if "--" in line.decode():
                line_have_comments +=1
    
    return {
        'count_lines'       : count_lines,
        'line_have_comments': line_have_comments
    }
    
def check_comments_python(filename:str):
    # using_quote = using_quote(filename)
    return using_hashtag(filename)

def check_comments_sql(filename:str):
    return using_dash(filename)

def check_file(filename:str, args) -> float:
    percentage         = 0
    count_lines        = 0
    line_have_comments = 0
    
    if filename == '-':
        contents_bytes = sys.stdin.buffer.read()
    else:
        # open file
        with open(filename, 'rb') as fb:
            contents_bytes = fb.read()
    
    if filename.endswith('.py'):
        counting           = check_comments_python(filename)
        count_lines        = counting['count_lines']
        line_have_comments = counting['line_have_comments']
    elif filename.endswith('.sql'):
        counting           = check_comments_sql(filename)
        count_lines        = counting['count_lines']
        line_have_comments = counting['line_have_comments']
    
    # get contexts files
    try:
        contents_text = contents_bytes.decode()
    except UnicodeDecodeError:
        print(f'{filename} is non-utf-8 (not supported)')
        return percentage
    
    if line_have_comments == percentage:
        return percentage
    
    percentage = round(100 * (float(line_have_comments) / float(count_lines)), 2)
    return percentage

if __name__ == "__main__":
    main()