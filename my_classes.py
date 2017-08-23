# -*- coding:utf-8 -*-

__author__ = 'Wang Cong'


class Subject(object):
    def __init__(self, id, num, name, en_name, credit, properties, score):
        """课程类\n
           id：课程号\n
           num：课序号\n
           name：课程名\n
           en_name：课程英文名\n
           credit：学分数\n
           properties：课程属性\n
           score：课程分数"""
        self._id = id
        self._num = num
        self._name = name
        self._en_name = en_name
        self._credit = credit
        self._properties = properties
        self._score = score

    def print_subject_info(self):
        print('%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
            self._id, self._num, self._name, self._en_name, self._credit, self._properties, self._score))

    @property
    def id(self):
        return self._id

    @property
    def num(self):
        return self._num

    @property
    def name(self):
        return self._name

    @property
    def en_name(self):
        return self._en_name

    @property
    def credit(self):
        return self._credit

    @property
    def properties(self):
        return self._properties

    @property
    def score(self):
        return self._score

        # @score.setter
        # def score(self, sc):
        #     self._score = sc


class Semester(object):
    def __init__(self, name, least_credits, studied_credits, studied_subjects, passed_subjects):
        """学期类\n
           name：学期名\n
           least_credits：最低修读学分\n
           studied_credits：已修读课程总学分\n
           studied_subjects：已修读课程门数\n
           passed_subjects：通过课程门数"""
        self._name = name
        self._least_credits = least_credits
        self._studied_credits = studied_credits
        self._studied_subjects = studied_subjects
        self._passed_subjects = passed_subjects

    def print_semester_info(self):
        print(self._name, self._least_credits, self._studied_credits, self._studied_subjects, self._passed_subjects)

    @property
    def name(self):
        return self._name

    @property
    def least_credits(self):
        return self._least_credits

    @property
    def studied_credits(self):
        return self._studied_credits

    @property
    def studied_subjects(self):
        return self._studied_subjects

    @property
    def passed_subjects(self):
        return self._passed_subjects
