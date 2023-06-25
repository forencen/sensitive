#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：script 
@File    ：sensitive.py
@Author  ：Forencen
@Date    ：2023/6/21 17:17 
@version ：1
敏感词和谐
"""
import re


def format_text(text):
    text = text.replace(' ', '').lower()
    # text re [^\u4e00-\u9fa5a-zA-Z0-9]
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9,.，。]', '', text)
    return text


class SensitiveV1:

    def __init__(self, sensitive_words: list, replace_char: str = '*'):
        self.sensitive_words = list(set(sensitive_words))
        self.replace_char = replace_char

    def match(self, text: str) -> bool:
        for word in self.sensitive_words:
            if word in text:
                return True
        return False

    def add_sensitive_words(self, words: list):
        self.sensitive_words.extend(words)
        self.sensitive_words = list(set(self.sensitive_words))

    def replace(self, text: str) -> str:
        for word in self.sensitive_words:
            text = text.replace(word, self.replace_char * len(word))
        return text


class SensitiveV2:

    def __init__(self, sensitive_words: list, replace_char: str = '*'):
        self.sensitive_words = list(set(sensitive_words))
        self.replace_char = replace_char

    def add_sensitive_words(self, words: list):
        self.sensitive_words.extend(words)
        self.sensitive_words = list(set(self.sensitive_words))

    def match(self, text: str) -> bool:
        regx_str = re.compile('|'.join(self.sensitive_words))
        _sensitive = regx_str.findall(text)
        return True if _sensitive else False

    def replace(self, text: str) -> str:
        regx_str = re.compile('|'.join(self.sensitive_words))
        _sensitive = regx_str.findall(text)
        for word in _sensitive:
            text = text.replace(word, self.replace_char * len(word))
        return text


class TrieNode:
    def __init__(self, value=None):
        self.value = value
        self.children = {}
        self.is_end = False


class SensitiveTrie:

    def __init__(self, sensitive_words: list):
        self.root = TrieNode()
        self.add_sensitive_words(sensitive_words)

    def insert_word(self, word):
        temp = self.root
        for _char in word:
            if _char in temp.children:
                temp = temp.children[_char]
            else:
                node = TrieNode(_char)
                temp.children[_char] = node
                temp = node
        temp.is_end = True

    def delete_word(self, word) -> bool:
        temp = self.root
        for _char in word:
            if _char in temp.children:
                temp = temp.children[_char]
            else:
                return False
        temp.is_end = False
        return True

    def add_sensitive_words(self, words: list):
        words = set(words)
        for word in words:
            self.insert_word(word)

    def match(self, text: str) -> tuple[bool, str]:
        temp = self.root
        match_word_count = 0
        for index, _char in enumerate(text):
            if _char in temp.children:
                match_word_count += 1
                temp = temp.children[_char]
                if temp.is_end:
                    return True, text[index + 1 - match_word_count:index + 1]
            else:
                match_word_count = 0
                temp = self.root
        return False, ''


class SensitiveV3:

    def __init__(self, sensitive_words: list, replace_char: str = '*'):
        self.sensitive_trie = SensitiveTrie(sensitive_words)
        self.replace_char = replace_char

    def add_sensitive_words(self, words: list):
        self.sensitive_trie.add_sensitive_words(words)

    def match(self, text: str) -> bool:
        for index in range(len(text)):
            is_sensitive, word = self.sensitive_trie.match(text[index:])
            if is_sensitive:
                return True
        return False

    def replace(self, text: str) -> str:
        res = text
        index = 0
        while index < len(text):
            is_sensitive, word = self.sensitive_trie.match(text[index:])
            if is_sensitive:
                res = res.replace(word, self.replace_char * len(word))
                index += len(word)
            else:
                index += 1
        return res


if __name__ == '__main__':
    source_sensitive_words = ["傻逼", "垃圾", "laji"]
    sensitive_v1 = SensitiveV1(source_sensitive_words)
    print(sensitive_v1.replace(format_text("傻 逼N次元,laji是个垃圾")))
    sensitive_v2 = SensitiveV2(source_sensitive_words)
    print(sensitive_v2.replace(format_text("傻 逼N次元,laji是个垃圾")))
    sensitive_v3 = SensitiveV3(source_sensitive_words)
    print(sensitive_v3.replace(format_text("傻 逼N次元,laji是个垃圾")))
