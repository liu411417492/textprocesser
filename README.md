# textprocesser

Dream of zhijiang 的剧本翻译器  
最近更新：2021.11.11

### 已实现的功能：
- 转换提前代码块（未完善！）
- 转换立绘、过渡、场景、BGM、音效等延迟代码块（未完善！）
- 转换台词、旁白（未完善！）

### 剧本规范：
1. 剧本文件完成后必须以.txt格式保存
2. 多个条件请写于同一行中，用【】包裹  
   ❌不建议的写法：
   ```
   【黑屏转场】
   【场景：地铁站】【音效：地铁站实录】【无BGM】
   【立绘：无立绘】
   旁白：市郊的地铁站，在下班的点人流攒动
   ```
   ✅建议的写法：
   ```
   【黑屏转场】【场景：地铁站】【音效：地铁站实录】【无BGM】【立绘：无立绘】
   旁白：市郊的地铁站，在下班的点人流攒动
   ```
3. 每一个条件要写明类型  
   ❌不建议的写法：
   ```
   【装修声】
   ```
   ✅建议的写法：
   ```
   【音效：装修声】
   ```
4. 尽量避免出现不必要的空格  
   ❌不建议的写法：
   ```
   而地铁站的人群，就在失去梦想的麻木中入站，出站。
         贝拉尽力避开人群，独自埋头快走
   ```
   ✅建议的写法：
   ```
   而地铁站的人群，就在失去梦想的麻木中入站，出站。
   贝拉尽力避开人群，独自埋头快走
   ```
5. 旁白可写可不写，对话中一定要注明角色，否则会被视为旁白  
   ✅建议的写法：
   ```
   旁白：“一、二、三、四，二、二、三、四…”
   旁白：年轻的舞蹈老师有节奏地用手打着拍子，而她面前，是一群稚气未脱的小舞蹈演员们
   ```
   ✅建议的写法：
   ```
   “一、二、三、四，二、二、三、四…”
   年轻的舞蹈老师有节奏地用手打着拍子，而她面前，是一群稚气未脱的小舞蹈演员们
   ```
   ✅建议的写法：
   ```
   旁白：“一、二、三、四，二、二、三、四…”
   年轻的舞蹈老师有节奏地用手打着拍子，而她面前，是一群稚气未脱的小舞蹈演员们
   ```
   ❌不建议的写法：
   ```
   贝拉：有位小朋友又慢了哦
   哎呀，你看，这里应该是这样转
   （以上两句都是贝拉的对话）
   ```
   ✅建议的写法：
   ```
   贝拉：有位小朋友又慢了哦
   贝拉：哎呀，你看，这里应该是这样转
   （以上两句都是贝拉的对话）
   ```


### 目前任务：
- [ ] 实际测试
- [ ] 对于“屏幕背景语”的转换
- [ ] 规范剧本格式
- [ ] 规范文件命名
- [ ] 更细节的转换
- [ ] ……

