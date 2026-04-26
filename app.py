from flask import Flask, request, render_template_string, redirect
from datetime import date

app = Flask(__name__)

habits = []

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Habit Tracker</title>
    <style>
        body {
            font-family: Arial;
            background: linear-gradient(to right, #141e30, #243b55);
            color: white;
            text-align: center;
        }
        .container {
            margin-top: 50px;
        }
        input {
            padding: 10px;
            border-radius: 10px;
            border: none;
        }
        button {
            padding: 10px 20px;
            border-radius: 10px;
            border: none;
            background: #00c6ff;
            color: white;
            cursor: pointer;
        }
        .habit {
            background: rgba(255,255,255,0.1);
            margin: 10px auto;
            padding: 15px;
            width: 300px;
            border-radius: 15px;
        }
        .done {
            text-decoration: line-through;
            color: lightgreen;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>🔥 Daily Habit Tracker</h1>

    <form method="POST" action="/add">
        <input type="text" name="habit" placeholder="Enter habit" required>
        <button>Add</button>
    </form>

    <h2>Your Habits</h2>

    {% for h in habits %}
        <div class="habit">
            <p class="{{ 'done' if h.done_today else '' }}">
                {{ h.name }}
            </p>
            <p>🔥 Streak: {{ h.streak }}</p>

            <form method="POST" action="/done/{{ loop.index0 }}">
                <button>Mark Done</button>
            </form>
        </div>
    {% endfor %}

</div>

</body>
</html>
"""

class Habit:
    def __init__(self, name):
        self.name = name
        self.streak = 0
        self.last_done = None
        self.done_today = False

@app.route("/")
def home():
    return render_template_string(HTML, habits=habits)

@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("habit")
    habits.append(Habit(name))
    return redirect("/")

@app.route("/done/<int:index>", methods=["POST"])
def done(index):
    habit = habits[index]
    today = str(date.today())

    if habit.last_done != today:
        habit.streak += 1
        habit.last_done = today
        habit.done_today = True

    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)