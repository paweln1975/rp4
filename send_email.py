import yagmail


with open(".gmail_password") as f:
    password = f.read()


yag = yagmail.SMTP('pawel.niedziela@gmail.com', password=password)
yag.send(to='pawel.niedziela@gmail.com', subject='Movement detected', contents="Hello from Raspberry PI")
