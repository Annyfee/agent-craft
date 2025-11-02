# tests/test_basic.py
import unittest
import sys
import os


class TestBasicImports(unittest.TestCase):

    def test_core_imports(self):
        """测试核心依赖是否可以导入"""
        # 测试必须的依赖
        import requests
        import dotenv

    def test_basic_syntax(self):
        """测试基本语法"""
        self.assertTrue(1 + 1 == 2)


if __name__ == '__main__':
    unittest.main()