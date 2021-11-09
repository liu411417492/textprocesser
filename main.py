import re


class Conversion:
    def __init__(self):
        self.original = open('original.txt', 'r', encoding='utf-8')
        self.result = open('result.txt', 'w+', encoding='utf-8')
        self.background = []
        self.bgm = []
        self.standing = []
        self.ch_change = {'贝拉': 'Bella', '向晚': 'Ava', '珈乐': 'Carol', '嘉然': 'Diana', '乃琳': 'Queen', '阿草': 'Acao', '男人': 'Man', '女人': 'Women', '男孩': 'Boy', '女孩': 'Girl'}
        self.cloth_change = {'常服':'causal','舞蹈服':'dance','团服':'team','画家':'draw'};
        self.apperence_change = {'通常':'causal','生气':'angry','微笑':'smile','惊讶':'surprised','失望':'disappointed'}
        #self.diana_cloth = {'常服':'causal','画家':'draw','团服':'team'}；

    @staticmethod
    def character(line: str, span: tuple[int, int]) -> str:
        """将标题行转换为提前代码块"""
        ch_change = {'贝拉': 'Bella', '向晚': 'Ava', '珈乐': 'Carol', '嘉然': 'Diana', '乃琳': 'Queen', '阿草': 'Acao', '男人': 'Man', '女人': 'Women', '男孩': 'Boy', '女孩': 'Girl'}
        result = "@<|\n" \
                 "label('ch%s', '%s')\n" \
                 "is_default_start()\n" \
                 "|>\n" \
                 % (cn_num[line[span[0] + 1: span[1] - 1]], line)
        return result

    @staticmethod
    def head(line: str, span: tuple[int, int]) -> str:
        """将标题行转换为提前代码块"""
        cn_num = {'一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9'}
        result = "@<|\n" \
                 "label('ch%s', '%s')\n" \
                 "is_default_start()\n" \
                 "|>\n" \
                 % (cn_num[line[span[0] + 1: span[1] - 1]], line)
        return result


    def main(self):
        """主程序"""
        line = self.original.readline()
        while line:
            if line == '\n':  # 删除空行
                line = self.original.readline()
                self.result.write(line)
                continue
            line = line.strip('\n')  # 删除末尾的换行符
            if re.match('第(.*?)章', line):  # 匹配文件开头的章节名
                span = re.match('第(.*?)章', line).span()
                self.result.write(self.head(line, span))
                line = self.original.readline()
                continue
            if re.match('【立绘：无立绘】', line):  # 匹配场景配置
                line = self.original.readline()
                continue
            else : 
            	if re.match('【立绘：(.*?)-(.*?)-(.*?)】', line):  # 匹配场景配置
            		listofcharac = re.findall('【立绘：(.*?)-(.*?)-(.*?)】', line);
            		#print(self.ch_change['贝拉']);
            		#print(self.ch_change[listofcharac[0][0]],self.cloth_change[listofcharac[0][1]] + '_' + self.apperence_change[listofcharac[0][2]]);
            		print('show(' + self.ch_change[listofcharac[0][0]] + ',' +'"' +  self.cloth_change[listofcharac[0][1]] + '_' + self.apperence_change[listofcharac[0][2]] + '"' + ','+ 'pos_c' + ')');
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
