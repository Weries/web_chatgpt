from flask import Flask, render_template, request
import openai
import os
from datetime import datetime

openai.api_key = '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' # 输入自己的api_key
proxies = {'http': "http://127.0.0.1:7890",
'https': "http://127.0.0.1:7890"}
openai.proxy = proxies
assert(openai.api_key)

app = Flask(__name__)
messages = []
@app.route('/')

# git push测试1
# 进一步的测试
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])

def get_bot_response():
    message = request.form['message']
    message  = message.rstrip('\n')
    messages.append({'role': 'user', 'content': message})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    response = completion.choices[0].message['content']
    print(response)
    today = datetime.now()
    csv_file_name = today.strftime('%Y-%m-%d') + '.txt'
    # 判断是否存在该文件，如果不存在就创建
    if not os.path.exists('./logs/' + csv_file_name):
        with open('./logs/' + csv_file_name, 'w', newline='') as outfile:
            outfile.write(f"time\tquestion\tanswer\n") # 写入表头

    # 获取当前时间并格式化，将用户输入的文本内容和时间写入csv文件
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    message = message.replace('\n', '|')
    responses = response.replace('\n', '|')
    with open('./logs/' + csv_file_name, mode='a', encoding='utf-8', newline='') as outfile:
        outfile.write(f"{timestamp}\t{message}\t{responses}\n")
    return response

if __name__ == '__main__':
    import webbrowser
    webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=True)
    