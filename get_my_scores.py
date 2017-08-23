# -*- coding:utf-8 -*-
import requests, random
# from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from pytesseract import *
from data_analysis import *

"""This is a program for getting my scores
   of all subjects from my university's
   academic teaching affair management system."""

__author__ = 'Wang Cong'

account = ""  # 学号
password = ""  # 密码
try_ver_times = 10  # 每次登录时验证码尝试次数
try_login_times = 5  # 登录尝试次数
session = requests.Session()  # 全局session会话


def get_verification_code():
    """获取登录验证码\n
       return：识别好的验证码"""
    headers = {"Host": "202.119.113.136",
               "Connection": "keep-alive",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
               }
    times = try_ver_times
    while times:
        # time.sleep(1)
        times -= 1
        session.headers.update(headers)  # 更新请求头
        r = session.get("http://202.119.113.136/validateCodeAction.do?random=" + str(random.random()))
        if r.status_code != 200:
            continue
        else:
            img = Image.open(BytesIO(r.content)).convert("L")  # 将验证码图片转成灰度图，提高识别率
            # img.show()
            ve = image_to_string(img)  # 利用pytesseract识别验证码图片
            # 验证码为4位大小写字母或数字组成，以下判断识别的验证码是否符合要求
            if len(ve) < 4:
                continue
            ve_ok = re.subn('[^0-9a-zA-Z]{1}', '', ve)[0]
            if len(ve_ok) != 4:
                continue
            else:
                # print("Try validation:", ve_ok)
                return ve_ok
    return False


def login(account, password, ver_code):
    """登录模块\n
       account：学号\n
       password：密码\n
       ver_code：验证码\n
       return：False表示登录失败，Response对象表示成功"""
    # va=input("请输入验证码：")
    session.headers.update({
        "Host": "202.119.113.136",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer": "http://202.119.113.136/logout.do",
        "Accept-Encoding": "gzip, deflate",
        "Upgrade-Insecure-Requests": "1"
    })
    form = {"zjh": account, "mm": password, "v_yzm": ver_code}
    r = session.post("http://202.119.113.136/loginAction.do", data=form)
    if r.status_code != 200:
        return False
    else:
        soup = BeautifulSoup(r.text, "lxml")
        if soup.title.string != "学分制综合教务":  # 根据返回的HTML页面的title判断是否登录成功
            return False
        else:
            return r


def get_score_tables():
    """获取所有成绩的HTML表格\n
       return：所有成绩的HTML表格"""
    session.headers.update({
        "Host": "202.119.113.136",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer": "http://202.119.113.136/gradeLnAllAction.do?type=ln&oper=qb",
        "Accept-Encoding": "gzip, deflate",
        "Upgrade-Insecure-Requests": "1"
    })
    params = {'type': 'ln', 'oper': 'qbinfo'}
    r = session.post("http://202.119.113.136/gradeLnAllAction.do", data=params)
    if r.status_code != 200:
        return False
    else:
        return r.text


def logout():
    """退出登录"""
    session.headers.update({
        "Host": "202.119.113.136",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer": "http://202.119.113.136/menu/top.jsp",
        "Accept-Encoding": "gzip, deflate",
        "Upgrade-Insecure-Requests": "1"
    })
    r = session.get('http://202.119.113.136/logout.do')
    if r.status_code != 200:
        return False
    else:
        session.close()
        return True


if __name__ == '__main__':
    print('学号：%s\n登录中...' % account)
    times = try_login_times
    while times:
        times -= 1
        ver_code = get_verification_code()
        if ver_code is False:
            print('尝试解析验证码%d次失败，程序退出！' % try_ver_times)
            exit()
        print("尝试验证码:", ver_code)
        r = login(account, password, ver_code)
        if r is False:
            print("登陆失败！")
            continue
        else:
            print("登陆成功！")
            times = 1
            break
    if times == 0:
        print('尝试登录%d次失败，程序退出！' % try_login_times)
        exit()

    print('获取成绩数据...')
    html_src = get_score_tables()
    if html_src is False:
        print('获取成绩数据失败，程序退出！')
        exit()
    print('获取数据成功！')
    if logout():
        print('退出登录成功！')
    else:
        session.close()
        print('退出登录失败，强制关闭会话！')

    print('分析数据...')
    all_subs = get_all_subjects(html_src)
    all_ses = get_all_semesters(html_src)
    all_ev_se_subs = get_every_semester_subjects(all_subs, all_ses)
    print('-' * 80)
    print('%d个学期的总体情况：\n' % len(all_ses))
    print("加权平均绩点：%.2f" % get_GPA(all_subs))
    required_elective = get_required_elective_subjects(all_subs)
    # print('必修课程总数：%d\t选修课程总数：%d' % (len(required_elective['必修']), len(required_elective['选修'])))
    not_passed = get_not_passed_subjects(all_subs)
    # print('必修课程未通过总数：%d\t选修课程未通过总数：%d\n' % (len(not_passed['必修']), len(not_passed['选修'])))
    for key in required_elective.keys():
        # print(len(not_passed[key]))
        print('%s课程总数：%-4d\t%s课程未通过数：%-4d' % (
            key, len(required_elective[key]), key, len(not_passed[key]) if key in not_passed.keys() else 0))
    t1 = sum(list(map(float, [se.least_credits for se in all_ses])))
    t2 = sum(list(map(float, [se.studied_credits for se in all_ses])))
    t3 = sum(list(map(int, [se.studied_subjects for se in all_ses])))
    t4 = sum(list(map(int, [se.passed_subjects for se in all_ses])))
    print('最低修读学分：%.1f\t已修读课程总学分：%.1f\t已修读课程门数：%d\t通过课程门数：%d' % (t1, t2, t3, t4))

    print('-' * 80)
    print('每个学期的具体情况：\n')
    for i in range(len(all_ses)):
        print(all_ses[i].name)
        print("加权平均绩点：%.2f" % get_GPA(all_ev_se_subs[i]))
        required_elective = get_required_elective_subjects(all_ev_se_subs[i])
        # print('必修课程总数：%d\t选修课程总数：%d' % (len(required_elective['必修']), len(required_elective['选修'])))
        not_passed = get_not_passed_subjects(all_ev_se_subs[i])
        # print('必修课程未通过总数：%d\t选修课程未通过总数：%d' % (len(not_passed['必修']), len(not_passed['选修'])))
        for key in required_elective.keys():
            print('%s课程总数：%-4d\t%s课程未通过数：%-4d' % (
                key, len(required_elective[key]), key, len(not_passed[key]) if key in not_passed.keys() else 0))
        print('最低修读学分：%s\t已修读课程总学分：%s\t已修读课程门数：%s\t通过课程门数：%s' % (
            all_ses[i].least_credits, all_ses[i].studied_credits, all_ses[i].studied_subjects,
            all_ses[i].passed_subjects))
        for key in not_passed.keys():
            print('未通过%s课程详细信息：' % key)
            if len(not_passed[key]) == 0:
                print('无')
            else:
                print('课程号\t课序号\t课程名\t英文课程名\t学分\t课程属性\t成绩')
                for sub in not_passed[key]:
                    sub.print_subject_info()
        print()
        # print('未通过必修课程详细信息：')
        # if len(not_passed['必修']) == 0:
        #     print('无')
        # else:
        #     print('课程号\t课序号\t课程名\t英文课程名\t学分\t课程属性\t成绩')
        #     for sub in not_passed['必修']:
        #         sub.print_subject_info()
        # print('未通过选修课程详细信息：')
        # if len(not_passed['选修']) == 0:
        #     print('无')
        # else:
        #     print('课程号\t课序号\t课程名\t英文课程名\t学分\t课程属性\t成绩')
        #     for sub in not_passed['选修']:
        #         sub.print_subject_info()
    print('-' * 80)
