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
       
    return errors

def check_comments(filename:str):
    # count lines
    count_lines        = 0
    line_have_comments = 0
    on_comments        = False
    with open(filename, 'rb') as fb:    
        for line in fb:
            count_lines += 1
            
            # check comments
            if '"""' in line.decode():
                
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

def check_file(filename:str, args) -> float:
    print(filename)
    if filename == '-':
        contents_bytes = sys.stdin.buffer.read()
    else:
        # open file
        with open(filename, 'rb') as fb:
            contents_bytes = fb.read()
        
    counting           = check_comments(filename)
    count_lines        = counting['count_lines']
    line_have_comments = counting['line_have_comments']
    
    # get contexts files
    try:
        contents_text = contents_bytes.decode()
    except UnicodeDecodeError:
        print(f'{filename} is non-utf-8 (not supported)')
        return 0
    
    if line_have_comments == 0:
        return 0
    
    return round(100 * (float(line_have_comments) / float(count_lines)), 2)

if __name__ == "__main__":
    main()