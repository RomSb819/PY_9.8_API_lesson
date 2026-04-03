from flask import Flask, request, render_template
import requests

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    quote_quantity = None
    result = None
    error = None

    if request.method == 'POST':
        quote_quantity = request.form.get('quote_quantity')

        if quote_quantity:
            try:
                result = get_quote(quote_quantity)
            except Exception as e:
                error = str(e)

    return render_template(
        'index.html',
        quote_quantity=quote_quantity,
        result=result,
        error=error
    )


def get_quote(quote_quantity):
    url = "https://quoteslate.vercel.app/api/quotes/random"
    params = {
        "count": quote_quantity
    }

    response = requests.get(url, params=params, timeout=10)

    print("URL запроса:", response.url)
    print("Статус:", response.status_code)
    print("Content-Type:", response.headers.get("Content-Type"))
    print("Текст ответа:", response.text[:500])

    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")
    if "application/json" not in content_type:
        raise ValueError(f"Сервер вернул не JSON, а: {content_type}")

    return response.json()


if __name__ == '__main__':
    app.run()