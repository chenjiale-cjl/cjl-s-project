from flask import Flask, jsonify, request, render_template, session
import random

# 创建Flask应用
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 用于session加密
# 扩展后的词库：英文单词为键，中文翻译为值
word_bank = {
    # 动物类
    "dog": "狗",
    "cat": "猫",
    "elephant": "大象",
    "lion": "狮子",
    "tiger": "老虎",
    "monkey": "猴子",
    "panda": "熊猫",
    "rabbit": "兔子",
    "fox": "狐狸",
    "wolf": "狼",
    
    # 水果类
    "apple": "苹果",
    "banana": "香蕉",
    "orange": "橙子",
    "grape": "葡萄",
    "watermelon": "西瓜",
    "strawberry": "草莓",
    "peach": "桃子",
    "pear": "梨",
    "pineapple": "菠萝",
    "mango": "芒果",
    
    # 食物类
    "rice": "米饭",
    "noodle": "面条",
    "bread": "面包",
    "egg": "鸡蛋",
    "milk": "牛奶",
    "cheese": "奶酪",
    "chocolate": "巧克力",
    "ice cream": "冰淇淋",
    "hamburger": "汉堡",
    "pizza": "披萨",
    
    # 日常用品
    "book": "书",
    "pen": "钢笔",
    "pencil": "铅笔",
    "bag": "包",
    "chair": "椅子",
    "table": "桌子",
    "computer": "电脑",
    "phone": "手机",
    "clock": "时钟",
    "lamp": "台灯",
    
    # 自然类
    "sun": "太阳",
    "moon": "月亮",
    "star": "星星",
    "sky": "天空",
    "cloud": "云",
    "rain": "雨",
    "snow": "雪",
    "river": "河流",
    "mountain": "山",
    "flower": "花",
    
    # 人物类
    "teacher": "老师",
    "student": "学生",
    "doctor": "医生",
    "nurse": "护士",
    "police": "警察",
    "farmer": "农民",
    "cook": "厨师",
    "driver": "司机",
    "king": "国王",
    "queen": "女王",
    
    # 颜色类
    "red": "红色",
    "blue": "蓝色",
    "green": "绿色",
    "yellow": "黄色",
    "black": "黑色",
    "white": "白色",
    "pink": "粉色",
    "purple": "紫色",
    "orange": "橙色",
    "brown": "棕色",
    
    # 动作类
    "run": "跑",
    "jump": "跳",
    "swim": "游泳",
    "eat": "吃",
    "drink": "喝",
    "sleep": "睡觉",
    "read": "阅读",
    "write": "写",
    "sing": "唱歌",
    "dance": "跳舞"
}

# 获取随机题目
@app.route('/get_question')
def get_question():
    # 初始化错题本
    if 'wrong_answers' not in session:
        session['wrong_answers'] = []
    
    # 从词库中随机选择一个单词
    word = random.choice(list(word_bank.keys()))
    # 获取该单词的正确翻译
    correct_translation = word_bank[word]
    # 从词库中随机选择3个错误翻译
    wrong_translations = random.sample(
        [v for k, v in word_bank.items() if v != correct_translation], 3)
    # 将正确翻译和错误翻译合并，并打乱顺序
    options = wrong_translations + [correct_translation]
    random.shuffle(options)
    # 返回JSON格式的题目数据
    return jsonify({
        "word": word,  # 当前单词
        "options": options,  # 4个选项
        "correct_answer": correct_translation  # 正确答案
    })

# 检查答案
@app.route('/check_answer', methods=['POST'])
def check_answer():
    # 获取前端发送的JSON数据
    data = request.json
    # 提取用户选择的答案和正确答案
    user_answer = data.get("answer")
    correct_answer = data.get("correct_answer")
    word = data.get("word")
    # 判断用户答案是否正确
    is_correct = (user_answer == correct_answer)
    
    # 记录错题
    if not is_correct:
        wrong_answer = {
            "word": word,
            "user_answer": user_answer,
            "correct_answer": correct_answer
        }
        if 'wrong_answers' not in session:
            session['wrong_answers'] = []
        session['wrong_answers'].append(wrong_answer)
        session.modified = True
    
    # 返回JSON格式的结果
    return jsonify({"is_correct": is_correct})

# 获取错题本
@app.route('/get_wrong_answers')
def get_wrong_answers():
    return jsonify(session.get('wrong_answers', []))
# 首页
@app.route('/')
def index():
    # 渲染前端页面
    return render_template('index.html')

# 启动Flask应用
if __name__ == '__main__':
    app.run(debug=True)