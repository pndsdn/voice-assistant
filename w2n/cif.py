def combine(text):
    str_nums = []
    nums = []
    str_nums.append(text[:text.find(" на ")])
    str_nums.append(text[text.find(" на ")+4::])

    for str_num in str_nums:
        if " целых " in str_num:
            _int = int(str_num[:text.find(" целых ")])
            _frac = float(str_num[text.find(" целых ")+7:])
            nums.append(_int + _frac)

        else:
            nums.append(int(str_num))

    return nums
