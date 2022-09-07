import pymongo
from flask import *


with open("mongo_db.txt","r") as f:
    mongodb_login = f.read()
client = pymongo.MongoClient(mongodb_login)

db = client.member_system
print("建立成功")

#初始化Flask伺服器
app = Flask (
    __name__,
    static_folder= "public",
    static_url_path= "/"
)
app.secret_key = "password"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/collections")
def collections():
    return render_template("collections.html")

@app.route("/products")
def products():
    if "nickname" in session:
        return render_template("member.html")   
    else:
        return render_template("products.html")    

@app.route("/reservation")
def reservation():
    return render_template("reservation.html")

@app.route("/traffic")
def traffic():
    return render_template("traffic.html")

@app.route("/member")
def member():
    if "nickname" in session:
        return render_template("member.html")   
    else:
        return redirect("/")
@app.route("/error")
def error():
    message = request.args.get("msg", "發生錯誤，請聯繫客服")
    return render_template("error.html", message=message)

@app.route("/signup_button")
def sign_button():
    return render_template("signup.html")

@app.route("/signup", methods = ["POST"])

#會員註冊頁面
def signup():
    #從前端接收資料
    nickname = request.form["nickname"]
    email = request.form["email"]
    password = request.form["password"]
    
    #根據接收到的資料，和資料庫互動
    collection = db.user

    if nickname and email and password:
        #檢查會員集合中是否有相同email的文件資料
        result = collection.find_one({
            "email":email
        })
        if result != None:
            return redirect("/error?msg=信箱已經被註冊")
        
        # 把資料放進資料庫，完成註冊
        collection.insert_one({
            "nickname":nickname,
            "email":email,
            "password":password
        })
        session["nickname"] = nickname
        return redirect("/signup_ok")
    else:
        return "請輸入註冊資料"

@app.route("/signup_ok")
def signup_ok():
    return render_template("signup_ok.html")

# 會員登入
@app.route("/signin", methods = ["POST"])
def singin():
    # 從前端取得使用者輸入
    email = request.form["email"]
    password = request.form["password"]
    collection = db.user
    result_email = collection.find_one({
        "email":email,     
    })
    result_password = collection.find_one({
            "password":password
    })
    # 登入失敗，導向錯誤頁面
    if result_email and result_password:
        session ["nickname"] = result_password ["nickname"]
        return redirect("/member")
    
    elif result_email and result_password == None:
        return redirect ("/error?msg=您的密碼輸入錯誤")
    
    elif result_email == None and result_password:
        return redirect ("/error?msg=您的帳號輸入錯誤")
    
    else:
        return redirect("/error?msg=您尚未註冊會員，請註冊成為會員。")

    
# 會員登出
@app.route("/signout")
def singout():
    # 移除session中的會員資料
    del session["nickname"]
    return redirect("/")


app.run(debug=True, port=3000)