import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import pandas as pd


def get_token(date):
    df = pd.read_csv('./logs/' + date + '.txt', delimiter='\t')
    df['question_token_count'] = df['question'].apply(lambda x:len(x))
    df['answer_token_count'] = df['answer'].apply(lambda x:len(x))
    # 计算总token数
    q_tokens = df['question_token_count'].sum()
    a_tokens = df['answer_token_count'].sum()
    return q_tokens, a_tokens, len(df)
if __name__ == '__main__':
    # 发件人邮箱
    username = "2464367707@qq.com"
    # QQ邮箱授权码
    password = "nqtdpthnjnbeecfe"
    # 可设置多个收件人邮箱
    receivers = ['3408853453@qq.com']
    # 设置抄送人信息，可多个，逗号分隔
    cc = ['2464367707@qq.com']

    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d')
    q_tokens, a_tokens,times = get_token(timestamp)
    # 设置标题
    subject = timestamp + " chatgpt网页端：{}Token({}次)({}元)".format(q_tokens+a_tokens, times, round((q_tokens+a_tokens)/1000*0.002*6,4))
    print(subject)
    # 设置内容
    
    content = "chat gpt 网页端{}统计情况\n问题请求tokens：{}\n回答请求tokens：{}".format(timestamp,q_tokens,a_tokens)
    print(content)
    # 创建MIMEMultipart对象，并封装相应的数据
    message = MIMEMultipart()
    # 封装标题
    message['Subject'] = Header(subject, 'gbk')
    # 封装发件人标识
    message['From'] = "chatgpt网页端Token统计"
    # 封装收件人和抄送人
    message['to'] = Header(",".join(receivers))
    message['Cc'] = Header(",".join(cc))
    # 生成邮件正文
    send_text = MIMEText(content, "plain", "utf-8")
    # 封装邮件正文
    message.attach(send_text)

    # 读取csv文件作为附件
    send_file_path = './logs/' + timestamp + '.txt'
    # 发送附件
    add_file = MIMEText(open(send_file_path, 'rb').read(), 'base64', 'gbk')
    add_file['Content-Type'] = 'application/octet-stream'
    # 设置文件名称
    add_file.add_header('Content-Disposition', 'attachment', filename="{}".format(send_file_path.split("\\")[-1]))
    message.attach(add_file)

    try:
        # 设置smtp的相关参数
        smtp_server = 'smtp.qq.com'
        smtp_port = 25
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        # 登录
        smtp.login(username, password)
        # 发送
        smtp.sendmail(username, receivers + cc, message.as_string())
        smtp.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件" + e.strerror)