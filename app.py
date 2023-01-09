from flask import Flask, render_template, request
from TheBakeryProblem import batch_orders
import json
app = Flask(__name__)

# =====================================


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            no_of_packers = int(request.form['no_of_packers'])
            available_goods_quantity = json.loads(
                request.form['available_goods_quantity'])
            print(available_goods_quantity)
            customer_orders = json.loads((request.form['customer_orders']))
            flow_of_batches = batch_orders(
                no_of_packers, available_goods_quantity, customer_orders)
            return render_template("index.html", flow_of_batches=flow_of_batches)
        except:
            return 'invalid input'
    else:
        return render_template("index.html", flow_of_batches={})

# =====================================


if __name__ == "__main__":
    app.run(debug=True)
