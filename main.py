import re


class Conversion:
    def __init__(self):
        self.original = open('original.txt', 'r', encoding='utf-8')
        self.result = open('result.txt', 'w+', encoding='utf-8')
        self.background = []  # 记录已经出现的背景，方便调用隐藏图像
        self.bgm = []   # 记录已经出现的bgm，方便隐藏
        self.standing = []   # 记录已经出现的立绘，方便隐藏

    @staticmethod
    def eager_execution_block(line: str, span: tuple[int, int]) -> str:
        """将标题行转换为提前代码块"""
        cn_num = {'一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9'}
        result = "@<|\n" \
                 "label('ch%s', '%s')\n" \
                 "|>\n" \
                 % (cn_num[line[span[0] + 1: span[1] - 1]], line)
        return result

    @staticmethod
    def lazy_execution_block():
        # todo: 延迟代码块的加载，包括立绘、场景、bgm
        pass

    def main(self):
        """主程序"""
        line = self.original.readline()
        while line:
            if line == '\n':  # 删除空行
                line = self.original.readline()
                continue
            line = line.strip('\n')  # 删除末尾的换行符
            if re.match('第(.*?)章', line):  # 匹配文件开头的章节名
                span = re.match('第(.*?)章', line).span()
                self.result.write(self.eager_execution_block(line, span))
                line = self.original.readline()
                continue
            if re.match('【(.*?)】', line):  # 匹配场景配置
                line = self.original.readline()
                continue
            # 以下为对话和旁白
            if re.match('旁白', line):
                span = re.match('旁白', line).span()
                aside = line[:span[0]] + line[span[1] + 1:] + "\n\n"  # 处理旁白
                self.result.write(aside)
                line = self.original.readline()
                continue
            else:
                line = line.replace('：', '：：', 1) + "\n\n"
                self.result.write(line)
                line = self.original.readline()
                continue
        self.original.close()
        self.result.close()
        return 0


if __name__ == '__main__':
    x = Conversion()
    x.main()
