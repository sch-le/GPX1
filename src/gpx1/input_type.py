def input_type(input_str: str, type: str):
    
    input_str = input()
    
    if type == int:
        try:
            int(input_str, 10)
        except Exception:
            input_str()        
    
    elif type == float:
        try:
            float(input_str, 10)    
        except Exception:
            input_str()