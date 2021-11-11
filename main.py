import re

debug = 1  # 0关闭调试，1仅显示转换为代码块的部分，2显示所有转换过程


class Conversion:
    def __init__(self):
        self.original = open('original.txt', 'r', encoding='utf-8')
        self.result = open('result.txt', 'w+', encoding='utf-8')
        self.line_num = 0  # 统计行数
        # 记录已出现的东西
        self.backgrounds: list[str] = []
        self.BGMs: list[str] = []
        self.standings: list[str] = []
        self.CGs: list[str] = []

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

        # 立绘部分
        character_change = {'贝拉': 'Bella', '向晚': 'Ava', '珈乐': 'Carol', '嘉然': 'Diana', '乃琳': 'Queen',
                            '阿草': 'Acao', '成年男人的剪影': 'Man', '成年女人的剪影': 'Women', '女人的剪影': 'Women',
                            '小男孩的剪影': 'Boy', '小女孩的剪影': 'Girl'}
        cloth_change = {'常服': 'causal', '舞蹈服': 'dance', '团服': 'team', '画家': 'draw'}
        appearance_change = {'通常': 'causal', '生气': 'angry', '微笑': 'smile', '惊讶': 'surprised',
                             '失望': 'disappointed', '50%灰度': 'halfgray'}
        trans = {'黑屏': 'black', '白场': 'white', '溶解': 'melt'}
        # self.diana_cloth = {'常服': 'causal','画家': 'draw','团服': 'team'}

        for block in blocks:
            if '立绘' in block:
                # todo: 目前只能转换贝拉的代码，其余部分需要改进
                for standing in self.standings:  # 先将不用的立绘隐藏
                    result += "hide(%s)\n" % standing
                    self.standings = []
                text = block[block.index('：') + 1:] + '/'  # 末尾添加符号方便匹配
                # text_t = block[block.index('：') + 1:]
                if text == '无立绘/':  # 无立绘不需要显示
                    print('\033[32mSUCCESS\033[0m | 延迟代码块：%s' % line) if debug > 0 else None
                elif re.match('(.*?)-(.*?)-(.*?)/', text):
                    # if(character_change[text_t])
                    character = re.findall('(.*?)-(.*?)-(.*?)/', text)[0]
                    print(character) if debug > 1 else None
                    print("show(" + character_change[character[0]] + ", '" + cloth_change[character[1]] + '_' +
                          appearance_change[character[2]] + "', pos_c)") if debug > 1 else None
                    result += "show(" + character_change[character[0]] + ", '" + cloth_change[character[1]] + '_' + \
                              appearance_change[character[2]] + "', pos_c)\n"
                    self.standings.append(character_change[character[0]])
                    print('\033[32mSUCCESS\033[0m | 延迟代码块：%s' % line) if debug > 0 else None
                elif re.match('(.*?)/', text):
                    character = re.findall('(.*?)/', text)
                    print(character) if debug > 1 else None
                    print("show(" + character_change[character[0]] + ", '" + 'default' + "', pos_c)") \
                        if debug > 1 else None
                    result += "show(" + character_change[character[0]] + ", '" + 'default' + "', pos_c)\n"
                    self.standings.append(character_change[character[0]])
                    print('\033[32mSUCCESS\033[0m | 延迟代码块：%s' % line) if debug > 0 else None
                else:
                    # print('\033[33mWARNING\033[0m | 未完成自动转换的剧本行：%s | 第%s行' % (line, self.line_num))
                    print(text)
            elif '转场' in block:
                # 转换场景的代码
                if re.findall('(.*?)转场', block):
                    tr = re.findall('(.*?)转场', block)[0]
                    print("anim:trans_fade(bg, " + trans[tr] + ")") if debug > 1 else None
                    result += "anim:trans_fade(bg, " + trans[tr] + ")\n"
                    print('\033[32mSUCCESS\033[0m | 延迟代码块：%s' % line) if debug > 0 else None
                else:
                    print('\033[33mWARNING\033[0m | 未完成自动转换的转场剧本行：%s | 第%s行' % (line, self.line_num))
            elif '过渡' in block:
                # todo: 转换场景的代码
                if re.findall('(.*?)过渡', block):
                    tr = re.findall('(.*?)过渡', block)[0]
                    # print(block)
                    print("anim:trans_fade(bg, " + trans[tr] + ")") if debug > 1 else None
                    result += "anim:trans_fade(bg, " + trans[tr] + ")\n"
                    print('\033[32mSUCCESS\033[0m | 延迟代码块：%s' % line) if debug > 0 else None
                else:
                    print('\033[33mWARNING\033[0m | 未完成自动转换的过渡剧本行：%s | 第%s行' % (line, self.line_num))
            elif '场景' in block:
                # todo: 转换场景的代码
                print('\033[33mWARNING\033[0m | 未完成自动转换的剧本行：%s | 第%s行' % (line, self.line_num))
            elif 'BGM' in block:
                # todo: 转换bgm的代码
                text = block[block.find('：') + 1:]
                if text == '无BGM':
                    for BGM in self.BGMs:
                        result += "stop(%s)\n" % BGM
                        self.BGMs = []
                else:
                    result += "play(bgm, '%s')\n" % text
                    self.BGMs.append(text)
                print('\033[32mSUCCESS\033[0m | 延迟代码块：%s -- %s' % (line, block)) if debug > 0 else None
            elif 'CG' in block:
                # todo: 转换CG的代码
                text = block[block.find('：') + 1:]
                if re.match('(.*?)-(.*?)灰度',text):
                	list = re.findall('(.*?)-(.*?)灰度',text);
                	print(list[0])
                	print('show(bg ,' + list[0][0] + ')');
                else:
                    result += "show(bg, '%s')\n" % text
                    self.CGs.append(text)
                print('\033[32mSUCCESS\033[0m | 延迟代码块：%s -- %s' % (line, block)) if debug > 0 else None
            elif '音效' in block:
                text = block[block.find('：') + 1:]
                if text == '无音效':
                    pass
                else:
                    result += "sound('%s')\n" % text
                print('\033[32mSUCCESS\033[0m | 延迟代码块：%s -- %s' % (line, block)) if debug > 0 else None
            else:
                print('\033[31mERROR  \033[0m | 自动转换出错的剧本行：%s | 第%s行' % (line, self.line_num))
                return None
        result += "|>\n"  # 代码块结尾
        if result != "<|\n|>\n":  # 如果没有代码无需添加
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
                self.lazy_execution_block(line)
                # print('\033[32mSUCCESS\033[0m | 延迟代码块：%s' % line) if debug > 0 and a is not None else None
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
