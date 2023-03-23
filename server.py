import datetime

from flask import Flask, render_template, redirect, request, make_response, session, url_for, jsonify
from werkzeug.exceptions import abort

import news_resources
from data.news import News
from forms.login import LoginForm
from data import db_session

from data.users import User
from forms.register import RegisterForm
from flask_login import LoginManager, current_user, login_required, logout_user, login_user

from forms.news import NewsForm

from flask_restful import reqparse, abort, Api, Resource


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    minutes=1
)

app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

login_manager = LoginManager()
login_manager.init_app(app)



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found 404'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request 400'}), 400)



@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/news',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
                           form=form)





@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/car')
def car():

    return render_template('car.html')





@app.route('/form_sample', methods=['POST', 'GET'])
def form_sample():
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                            crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            <title>Отбор космонавтов</title>
                          </head>
                          <body>
                            <h1>Анкета в давинчике</h1>
                            <div>
                                <form class="login_form" method="post">
                                    <input type="text" class="form-control" id="text" aria-describedby="emailHelp" placeholder="Введите имя" name="name">
                                    <input type="text" class="form-control" id="text" placeholder="Введите фамилию" name="firstName">
                                    <input type="email" class="form-control" id="email" placeholder="Введите почту" name="email">
                                    <div class="form-group">
                                        <label for="classSelect">ваш уровень хайпа</label>
                                        <select class="form-control" id="classSelect" name="class">
                                          <option>Нубик</option>
                                          <option>Про</option>
                                          <option>Читер</option>
                                          <option>Бог</option>
                                          <option>Андрей</option>
                                        </select>
                                     </div>
                                    <div class="form-group">
                                        <label for="form-check">Укажите пол</label>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="male" value="male" checked>
                                          <label class="form-check-label" for="male">
                                            Мужской
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="female" value="female">
                                          <label class="form-check-label" for="female">
                                            Женский
                                          </label>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <label for="about">Какие у вас есть профессии</label><br>
                                        <input type="checkbox" class="form-check-input" id="jobs" name="job1">
                                        <label class="form-check-label" for="acceptRules">Уборщик</label><br>
                                        <input type="checkbox" class="form-check-input" id="jobs" name="job2">
                                        <label class="form-check-label" for="acceptRules">Ветеринар</label><br>
                                        <input type="checkbox" class="form-check-input" id="jobs" name="job3">
                                        <label class="form-check-label" for="acceptRules">Специалист по мемам</label><br>
                                    </div>
                                    <div class="form-group">
                                        <label for="about">Почему вы хотите принять повестку?</label>
                                        <textarea class="form-control" id="about" rows="3" name="about"></textarea>
                                    </div>
                                    <div class="form-group form-check">
                                        <input type="checkbox" class="form-check-input" id="acceptRules" name="accept">
                                        <label class="form-check-label" for="acceptRules">Готов быть добровольцем</label>
                                    </div>
                                    <button type="submit" class="btn btn-primary">Записаться</button>
                                </form>
                            </div>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        print(request.form['name'])
        print(request.form['firstName'])
        print(request.form['email'])
        print(request.form['class'])
        print(request.form['about'])
        print(request.form['accept'])
        print(request.form['sex'])
        return "Форма отправлена"



@app.route('/astronaut_selection', methods=['POST', 'GET'])
def astronaut_selection():
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                            crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            <title>Отбор астронавтов</title>
                          </head>
                          <body>
                            <h1>Анкета претендента</h1>
                            <h1>на участие в миссии</h1>
                            <div>
                                <form class="login_form" method="post">
                                    <input type="surname" class="form-control" id="surname" placeholder="Введите фамилию" name="surname">
                                    <input type="name" class="form-control" id="name" placeholder="Введите имя" name="name">
                                    <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                                    <div class="form-group">
                                        <label for="classSelect">Какое у Вас образование?</label>
                                        <select class="form-control" id="classSelect" name="class">
                                          <option>Начальное</option>
                                          <option>Среднее</option>
                                          <option>Высшее</option>
                                        </select>
                                     </div>
                                    <div class="form-group">
                                        <label for="form-check">Какие у Вас есть профессии?</label>
                                        <div class="form-check">
                                          <input class="form-check-input" type="checkbox" name="prof" id="eng-exp" value="eng-exp">
                                          <label class="form-check-label" for="eng-exp">
                                            Инженер-исследователь
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="checkbox" name="prof" id="eng-bld" value="eng-bld">
                                          <label class="form-check-label" for="eng-bld">
                                            Инженер-строитель
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="checkbox" name="prof" id="pilot" value="pilot">
                                          <label class="form-check-label" for="pilot">
                                            Пилот
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="checkbox" name="prof" id="bld" value="bld">
                                          <label class="form-check-label" for="bld">
                                            Cтроитель
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="checkbox" name="prof" id="doc" value="doc">
                                          <label class="form-check-label" for="doc">
                                            Доктор
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="checkbox" name="prof" id="clm" value="clm">
                                          <label class="form-check-label" for="clm">
                                            Климатолог
                                          </label>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <label for="form-check">Укажите пол</label>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="male" value="male">
                                          <label class="form-check-label" for="male">
                                            Мужской
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="female" value="female">
                                          <label class="form-check-label" for="female">
                                            Женский
                                          </label>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <label for="about">Почему вы хотите принять участие в миссии?</label>
                                        <textarea class="form-control" id="about" rows="3" name="about"></textarea>
                                    </div>
                                    <div class="form-group">
                                        <label for="photo">Приложите фотографию</label>
                                        <input type="file" class="form-control-file" id="photo" name="file">
                                    </div>
                                    <div class="form-group form-check">
                                        <input type="checkbox" class="form-check-input" id="acceptRules" name="accept">
                                        <label class="form-check-label" for="acceptRules">Готовы остаться на Марсе?</label>
                                    </div>
                                    <button type="submit" class="btn btn-primary">Записаться</button>
                                </form>
                            </div>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        return "Форма отправлена"





@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)






@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/success')
def success():
    return 'ok'


def create_user():

    user2 = User()
    user2.name = "Пользователь 2"
    user2.about = "биография пользователя 2"
    user2.email = "email2@email.ru"
    db_sess = db_session.create_session()
    db_sess.add(user2)
    db_sess.commit()

    '''user = User()
    user.name = "Пользователь 1"
    user.about = "биография пользователя 1"
    user.email = "email1@email.ru"
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()
     
    user3 = User()
    user3.name = "Пользователь 3"
    user3.about = "биография пользователя 3"
    user3.email = "email3@email.ru"
    db_sess = db_session.create_session()
    db_sess.add(user3)
    db_sess.commit()'''


def first_query():
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        print(user)

    print()
    for user in db_sess.query(User).filter(User.id > 1, User.email.notilike("%1%")):
        print(user)

    print()
    for user in db_sess.query(User).filter((User.id > 2) | (User.email.notilike("%1%"))):
        print(user)


def edit():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == 1).first()
    print(user)
    user.name = "Измененное имя пользователя"
    user.created_date = datetime.now()
    db_sess.commit()

def del_users():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == 2).first()
    db_sess.delete(user)
    db_sess.commit()



def create_news():
    db_sess = db_session.create_session()
    news1 = News(title="Первая новость",
                content="Привет блог!",
                user_id=4,
                is_private=False)
    db_sess.add(news1)
    db_sess.commit()

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == 3).first()
    news2 = News(title="Вторая новость", content="Уже вторая запись!",
                user=user, is_private=False)
    db_sess.add(news2)
    db_sess.commit()

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == 1).first()
    news3 = News(title="Личная запись", content="Эта запись личная",
                is_private=True)
    user.news.append(news3)
    db_sess.commit()


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res








if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    api.add_resource(news_resources.NewsListResource, '/api/v2/news')
    api.add_resource(news_resources.NewsResource, '/api/v2/news/<int:news_id>')

    #create_user()
    #first_query()
    #edit()
    #del_users()
    #create_news()

    app.run(port=8089, host='127.0.0.1')