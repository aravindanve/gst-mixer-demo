def parse_rtp_bin_pad_info_from_name(pad_name):
    pad_name_parts = pad_name.split('_')
    info = {}

    if len(pad_name_parts) >= 4:
        info['direction'] = pad_name_parts[0]
        info['protocol'] = pad_name_parts[1]
        info['type'] = pad_name_parts[2]
        info['session'] = int(pad_name_parts[3])

    if len(pad_name_parts) >= 6:
        info['ssrc'] = pad_name_parts[4]
        info['payload'] = int(pad_name_parts[5])

    return info
