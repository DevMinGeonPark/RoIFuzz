def check(config, msg_list, state_dict, feedback_list):
    errs = list()
    msg = msg_list[0]
    msg_name = type(msg).__name__
    topic_name = f"/idltest_{msg_name}_out"

    if topic_name not in state_dict:
        errs.append(f"Topic {topic_name} is lost")
        return errs

    msg_out_list = state_dict[topic_name]
    if len(msg_out_list) != 1:
        errs.append("Multiple messages replayed by idl target")
        return errs

    (ts, msg_out) = msg_out_list[0]
    
    if not hasattr(msg, 'data') or not hasattr(msg_out, 'data'):
        errs.append("Message does not have 'data' attribute")
        return errs

    # 값 범위 검사 (에러 유발 값 허용)
    if isinstance(msg.data, (int, float)) and "Bool" not in msg_name and "Char" not in msg_name:
        min_val = getattr(msg, 'MIN', float('-inf'))
        max_val = getattr(msg, 'MAX', float('inf'))
        if isinstance(min_val, (int, float)) and isinstance(max_val, (int, float)):
            if not (min_val <= msg.data <= max_val):
                errs.append(f"Value {msg.data} is out of valid range for {msg_name}")
    elif isinstance(msg.data, list):
        for i, val in enumerate(msg.data):
            if isinstance(val, (int, float)) and "Bool" not in msg_name and "Char" not in msg_name:
                min_val = getattr(msg, 'MIN', float('-inf'))
                max_val = getattr(msg, 'MAX', float('inf'))
                if isinstance(min_val, (int, float)) and isinstance(max_val, (int, float)):
                    if not (min_val <= val <= max_val):
                        errs.append(f"Value {val} at index {i} is out of valid range for {msg_name}")

    # 타입 검사 (에러 유발 타입 허용)
    if type(msg.data) != type(msg_out.data):
        errs.append(f"Type mismatch: sent {type(msg.data)}, received {type(msg_out.data)}")

    # 값 일치 검사
    if "Array" not in msg_name:
        if msg.data != msg_out.data:
            errs.append(f"IN:{msg.data}|OUT:{msg_out.data} / Sent and replayed messages do not match")
    else:
        if isinstance(msg.data, list) and isinstance(msg_out.data, list):
            if len(msg.data) != len(msg_out.data):
                errs.append("Sent and replayed array lengths do not match")
            else:
                for i in range(len(msg.data)):
                    if msg.data[i] != msg_out.data[i]:
                        errs.append(f"Sent and replayed messages do not match at index {i}")
                        break
        else:
            errs.append("Array data is not of list type")

    return errs
