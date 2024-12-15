from flask import Flask, render_template, request

app = Flask(__name__)

# Логика расчета потребительского кредита
def calculate_credit(principal, rate, term):
    monthly_rate = rate / 12 / 100  # Месячная процентная ставка
    if monthly_rate == 0:
        monthly_payment = principal / term
    else:
        monthly_payment = principal * monthly_rate / (1 - (1 + monthly_rate) ** -term)

    total_payment = monthly_payment * term  # Общая сумма выплат
    total_interest = total_payment - principal  # Начисленные проценты
    return round(monthly_payment, 2), round(total_payment, 2), round(total_interest, 2)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Получение данных из формы
            principal = float(request.form.get("principal"))
            rate = float(request.form.get("rate"))
            term = int(request.form.get("term"))

            # Расчет
            monthly_payment, total_payment, total_interest = calculate_credit(principal, rate, term)

            return render_template(
                "Calculator.html",
                result={
                    "monthly_payment": monthly_payment,
                    "total_payment": total_payment,
                    "total_interest": total_interest,
                },
                principal=principal,
                rate=rate,
                term=term,
            )
        except ValueError:
            error = "Ошибка ввода данных. Проверьте значения!"
            return render_template("Calculator.html", error=error)

    return render_template("Calculator.html")

if __name__ == "__main__":
    app.run(debug=True)
