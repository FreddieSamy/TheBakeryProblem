from flask import Flask, render_template, request
from TheBakeryProblem import batch_orders
import json
import os

# =====================================

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
            flow_of_batches, final_available_quantities = batch_orders(
                no_of_packers, available_goods_quantity, customer_orders)
            return render_template("index.html", flow_of_batches=flow_of_batches, final_available_quantities=final_available_quantities)
        except:
            return render_template("index.html", invalid=True)
    else:
        return render_template("index.html", flow_of_batches={}, final_available_quantities={})

# =====================================


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
