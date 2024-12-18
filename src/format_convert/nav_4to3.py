#-*- coding:utf-8 -*-
# ----------------------------------------------------------------
# *                                                             * |
# * History                                                     * |
# *   -1.0 Liang Qiao  2023-05-05 created                       * |
# *                                                             * |
# * Copyright (c) 2023, East China University of Technology.    * |
# *                     All rights reserved.                    * |
# *                                                             * |
# * Brief    Navigation Data RINEX Conversion                   * |
#            <From 4.00 to 3.00/3.01/3.02/3.03/3.04/3.05>       * |
# *                                                             * |
# * Author   Liang Qiao, East China University of Technology    * |
# * Date     2023-05-05                                         * |
# * Description     python 3.*                                  * |
# *                                                             * |
# ----------------------------------------------------------------


def NAV_rinex4_to_rinex3(input_file_path, target_version):
    with open(input_file_path, 'r') as f:
        raw_rinex_text_list = f.readlines()
    copy_raw_rinex_text_list = raw_rinex_text_list[:]
    raw_header_info = []
    for i in range(len(raw_rinex_text_list)):
        line_text = raw_rinex_text_list[i].strip('\n')
        temp_info_list = [line_text[0:60], line_text[60:80]]
        raw_header_info = raw_header_info + [temp_info_list]
        if 'END OF HEADER' in line_text:
            end_header_rows = i
            break
    converd_list = []
    for i in raw_header_info:
        temp_list = []
        if i[1].strip() == 'RINEX VERSION / TYPE':
            lines_text = ' ' * 5 + target_version + (15 - len(target_version)) * ' ' + i[0][20:60] + i[1]
        else:
            lines_text = i[0] + i[1]
        temp_list.append(lines_text)
        converd_list.append(temp_list)
    iter_copy_raw_rinex_text_list = iter(copy_raw_rinex_text_list[end_header_rows + 1:])
    for row_line in iter_copy_raw_rinex_text_list:
        temp_list = []
        system = row_line.split('\n')[0][6:7].upper()
        if system in ['G', 'E', 'C', 'J', 'I']:
            skip_line_num = 8
        elif system in ['R']:
            skip_line_num = 5
        elif system in ['S']:
            skip_line_num = 4
        while skip_line_num > 0:
            temp_list.append(next(iter_copy_raw_rinex_text_list).split('\n')[0])
            skip_line_num -= 1
        if system == 'R' and target_version != '3.05':
            del(temp_list[-1])
        converd_list.append(temp_list)
    return converd_list

