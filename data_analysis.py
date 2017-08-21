# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from my_classes import *
import re

__author__ = 'Wang Cong'


def get_all_subjects(html_src):
    """获取所有课程信息及成绩\n
       return：课程Subject组成的list"""
    soup = BeautifulSoup(html_src, 'lxml')
    tds = soup.find_all('td', align="center")
    # print(tds[-1].contents)
    tds_list = []
    for item in tds:
        # if item.string is None:
        #     continue
        if len(item.contents) > 1:
            # for i in item.contents:
            # if i.name == 'p':
            # print(item.contents[1])
            tds_list.append(item.p.string.strip())
            # break
        elif len(item.contents) == 1:
            tds_list.append(item.string.strip())
    # print(tds_list)
    # print(len(tds_list))
    all_subjects = []
    index = 0
    while index < len(tds_list):
        id = tds_list[index]
        index += 1
        num = tds_list[index]
        index += 1
        name = tds_list[index]
        index += 1
        en_name = tds_list[index]
        index += 1
        credit = tds_list[index]
        index += 1
        properties = tds_list[index]
        index += 1
        score = tds_list[index]
        index += 1
        all_subjects.append(Subject(id, num, name, en_name, credit, properties, score))
    # print(len(all_subjects))
    # for i in all_subjects:
    #     i.print_subject_info()
    return all_subjects


def get_all_semesters(html_src):
    """获取所有学期的总体信息\n
       return：学期Semester组成的list"""
    soup = BeautifulSoup(html_src, 'lxml')
    td_names = soup.find_all('td', valign='middle')
    se_names = [x.b.string.strip() for x in td_names]
    # print(td_names[0].b.string)
    # print(se_names)
    td_infos = soup.find_all('td', height="21")
    # print(td_infos)
    se_infos = [x.string.strip() for x in td_infos]
    all_semesters = []
    index = 0
    re_match = re.compile(
        r'[\u4e00-\u9fa5]+[：|:]\xa0*(\d+\.\d+)\xa0*[\u4e00-\u9fa5]+[：|:]\xa0*(\d+\.\d+)\xa0*[\u4e00-\u9fa5]+[：|:]\xa0*(\d+)\xa0*[\u4e00-\u9fa5]+[：|:]\xa0*(\d+)')
    while index < len(se_infos):
        name = se_names[index]
        least_credits, studied_credits, studied_subjects, passed_subjects = re_match.match(se_infos[index]).groups()
        all_semesters.append(Semester(name, least_credits, studied_credits, studied_subjects, passed_subjects))
        index += 1
    # for i in all_semesters:
    #     i.print_semester_info()
    return all_semesters
    # print(re.match(,se_infos[0]).groups())


def get_every_semester_subjects(all_subjects_list, all_semesters_list):
    """获取每个学期的所有课程的信息\n
       all_subjects_list：所有课程\n
       all_semesters_list：所有学期\n
       return：list的list，每个元素的都一个list，包含该学期的课程信息"""
    se_num = len(all_semesters_list)
    all_every_semester_subjects = []
    first_index = 0
    for i in range(se_num):
        all_every_semester_subjects.append(
            all_subjects_list[first_index:first_index + int(all_semesters_list[i].studied_subjects)])
        first_index += int(all_semesters_list[i].studied_subjects)
    # print(all_every_semester_subjects)
    # for i in all_every_semester_subjects[1]:
    #     i.print_subject_info()
    return all_every_semester_subjects


def get_GPA(subjects_list):
    """计算加权平均绩点\n
       subjects_list：课程list\n
       return：加权平均绩点"""
    all_sum, div_sum = 0, 0
    for sub in subjects_list:
        if sub.properties == '必修':
            now_credit = float(sub.credit)
            now_sc = sub.score
            if now_sc == '优秀':
                all_sum += 5.0 * now_credit
            elif now_sc == '良好':
                all_sum += 4.0 * now_credit
            elif now_sc == '及格':
                all_sum += 3.0 * now_credit
            elif now_sc == '不及格' or now_sc == '缺考':
                all_sum += 0.0 * now_credit
            else:
                sc = float(now_sc)
                if sc >= 90:
                    all_sum += 5.0 * now_credit
                elif sc >= 85:
                    all_sum += 4.5 * now_credit
                elif sc >= 80:
                    all_sum += 4.0 * now_credit
                elif sc >= 75:
                    all_sum += 3.5 * now_credit
                elif sc >= 70:
                    all_sum += 3.0 * now_credit
                elif sc >= 65:
                    all_sum += 2.5 * now_credit
                elif sc >= 60:
                    all_sum += 2.0 * now_credit
                else:
                    all_sum += 0.0 * now_credit
            div_sum += now_credit
    # print(all_sum, div_sum)
    return all_sum / div_sum


def get_not_passed_subjects(subjects_list):
    """获取未通过的课程信息\n
       subjects_list：课程list\n
       return：挂科的科目dict"""
    not_passed_subs = {'必修': [], '选修': []}
    for sub in subjects_list:
        not_passed = False
        sc = sub.score
        if sc == '不及格' or sc == '缺考':
            not_passed = True
        elif sc == '优秀' or sc == '良好' or sc == '及格':
            continue
        else:
            sc = float(sc)
            if sc < 60:
                not_passed = True
            else:
                continue
        if not_passed:
            if sub.properties == '必修':
                not_passed_subs['必修'].append(sub)
            else:
                not_passed_subs['选修'].append(sub)
    return not_passed_subs


def get_required_elective_subjects(subjects_list):
    """获取必修和选修的课程信息\n
       subjects_list：课程list\n
       return：必修和选修的课程dict"""
    required_elective_subs = {'必修': [], '选修': []}
    required_elective_subs['必修'] = [sub for sub in subjects_list if sub.properties == '必修']
    required_elective_subs['选修'] = [sub for sub in subjects_list if sub.properties == '选修']
    return required_elective_subs


if __name__ == '__main__':
    with open('E:\\table.html', 'r') as fp:
        html_src = fp.read()
    all_subs = get_all_subjects(html_src)
    all_ses = get_all_semesters(html_src)
    all_ev_se_subs = get_every_semester_subjects(all_subs, all_ses)
    # print(get_GPA(all_ev_se_subs[0]))
    for i in all_ev_se_subs:
        print(get_GPA(i))
    print(get_GPA(all_subs))
    for i in all_ev_se_subs:
        print(get_not_passed_subjects(i))
