import re

debug = 1  # 0关闭调试，1仅显示转换为代码块的部分，2显示所有转换过程


class Conversion:
    def __init__(self):
        self.original = open('original.txt', 'r', encoding='utf-8')
        self.result = open('result.txt', 'w+', encoding='utf-8')
        self.line_num = 0  # 统计行数

    @staticmethod
    def eager_execution_block(line: str, span: tuple[int, int]) -> str:
        """将标题行转换为提前代码块"""
        cn_num = {'一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9'}
        result = "@<|\n" \
                 "label('ch%s', '%s')\n" \
                 "|>\n" \
                 % (cn_num[line[span[0] + 1: span[1] - 1]], line)
        return result

    def lazy_execution_block(self, line: str) -> str | None:
        # todo: 延迟代码块的加载，包括立绘、场景、bgm
        # 首先进行分割
        result = "<|\n"  # 代码块开头
        blocks = re.findall('【(.*?)】', line)  # blocks为待处理的场景，类型为list

        # 记录已出现的东西
        backgrounds: list[str] = []
        bgms: list[str] = []
        standings: list[str] = []

        # 立绘部分
        character_change = {'贝拉': 'Bella', '向晚': 'Ava', '珈乐': 'Carol', '嘉然': 'Diana', '乃琳': 'Queen',
                            '阿草': 'Acao', '男人': 'Man', '女人': 'Women', '男孩': 'Boy', '女孩': 'Girl'}
        cloth_change = {'常服': 'causal', '舞蹈服': 'dance', '团服': 'team', '画家': 'draw'}
        appearance_change = {'通常': 'causal', '生气': 'angry', '微笑': 'smile', '惊讶': 'surprised',
                             '失望': 'disappointed'}
        # self.diana_cloth = {'常服': 'causal','画家': 'draw','团服': 'team'}

        for block in blocks:
            if '立绘' in block:
                # todo: 目前只能转换贝拉的代码，其余部分需要改进
                for standing in standings:  # 先将不用的立绘隐藏
                    result += "hide(%s)\n" % standing
                text = block[block.index('：') + 1:] + '/'
                if text == '无立绘/':  # 无立绘不需要显示
                    print('\033[32mSUCCESS\033[0m | 延迟代码块：%s' % line) if debug > 0 else None
                elif '贝拉' in text:
                    character = re.findall('(.*?)-(.*?)-(.*?)/', text)[0]
                    print(character) if debug > 1 else None
                    print("show(" + character_change[character[0]] + ", '" + cloth_change[character[1]] + '_' +
                          appearance_change[character[2]] + "', pos_c)") if debug > 1 else None
                    result += "show(" + character_change[character[0]] + ", '" + cloth_change[character[1]] + '_' + \
                              appearance_change[character[2]] + "', pos_c)\n"
                    print('\033[32mSUCCESS\033[0m | 延迟代码块：%s' % line) if debug > 0 else None
                else:
                    print('\033[33mWARNING\033[0m | 未完成自动转换的剧本行：%s | 第%s行' % (line, self.line_num))
            elif '场景' in block:
                # todo: 转换场景的代码
                print('\033[33mWARNING\033[0m | 未完成自动转换的剧本行：%s | 第%s行' % (line, self.line_num))
            elif 'bgm' in block:
                # todo: 转换bgm的代码
                print('\033[33mWARNING\033[0m | 未完成自动转换的剧本行：%s | 第%s行' % (line, self.line_num))
            elif '音效' in block:
                # todo: 转换音效的代码
                print('\033[33mWARNING\033[0m | 未完成自动转换的剧本行：%s | 第%s行' % (line, self.line_num))
            else:
                print('\033[33mWARNING\033[0m | 未完成自动转换的剧本行：%s | 第%s行' % (line, self.line_num))
                return None
        result += "|>\n"  # 代码块结尾
        if result != "<|\n|>\n":
            self.result.write(result)
        return result

    def main(self):
        """主程序"""
        line = self.original.readline()
        while line:
            self.line_num += 1
            if line == '\n':  # 删除空行
                line = self.original.readline()
                continue
            line = line.strip('\n')  # 删除末尾的换行符
            if re.match('第(.*?)章', line):  # 匹配文件开头的章节名
                span = re.match('第(.*?)章', line).span()
                self.result.write(self.eager_execution_block(line, span))
                print('\033[32mSUCCESS\033[0m | 提前代码块：%s' % line) if debug > 0 else None
                line = self.original.readline()
                continue
            if re.match('【(.*?)】', line):  # 匹配场景配置
                a = self.lazy_execution_block(line)
                print('\033[32mSUCCESS\033[0m | 延迟代码块：%s' % line) if debug > 0 and a is not None else None
                line = self.original.readline()
                continue
            # 以下为对话和旁白
            if re.match('旁白', line):
                span = re.match('旁白', line).span()
                aside = line[:span[0]] + line[span[1] + 1:] + "\n\n"  # 处理旁白
                self.result.write(aside)
                print('\033[32mSUCCESS\033[0m | 旁白：%s' % line) if debug > 1 else None
                line = self.original.readline()
                continue
            else:
                line = line.replace('：', '：：', 1) + "\n\n"
                self.result.write(line)
                print('\033[32mSUCCESS\033[0m | 台词：%s' % line) if debug > 1 else None
                line = self.original.readline()
                continue
        self.original.close()
        self.result.close()
        return 0


if __name__ == '__main__':
    x = Conversion()
    x.main()
