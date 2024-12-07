# 간단한 메일 보내기
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP 서버 설정
smtp_server = 'smtp.gmail.com'
smtp_port = 587  # Gmail의 경우 TLS(보안 연결)을 사용하는 포트는 587입니다.

# 보내는 사람 정보
sender_email = 'your_email@gmail.com'
sender_password = 'your_password'  # 보안을 위해 코드에 직접 비밀번호를 작성하는 것은 권장되지 않습니다.

# 받는 사람 정보
receiver_email = 'recipient_email@example.com'

# 이메일 내용 설정
subject = 'Test Email'
body = 'This is a test email sent using Python.'

# 이메일 구성
msg = MIMEMultipart()
msg['From'] = 'fkdlxmsld561@gmail.com'
msg['To'] = 'gkthd2162@gmail.com'
msg['Subject'] = 'alstlr583'

# 이메일 본문 추가
msg.attach(MIMEText(body, 'plain'))

try:
    # SMTP 서버 연결
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # TLS 보안 연결 시작
    server.login(sender_email, sender_password)  # SMTP 서버에 로그인

    # 이메일 보내기
    server.sendmail(sender_email, receiver_email, msg.as_string())
    print('Email sent successfully!')
except Exception as e:
    print(f'Failed to send email. Error: {str(e)}')
finally:
    # SMTP 서버 연결 종료
    server.quit()
