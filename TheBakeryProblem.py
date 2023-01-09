# The Bakery Problem
import threading
from flask import Markup
# Global lock
LOCK = threading.Lock()


def batch_orders(no_of_packers, available_goods_quantity, customer_orders):
    """
    This function takes in the number of packers, available goods quantity and customer orders and returns a sequence of the batches.
    :param no_of_packers: number of packers available
    :param available_goods_quantity: quantities of goods available
    :param customer_orders: customer orders
    :return: flow_of_batches: number a sequence of batches each packer will do
    """

    # constructing order priority queue and remaining_orders
    order_priority_queue, remaining_orders = order_priority(customer_orders)

    # ---------------------------------------------------
    # initializing variables and assigning NO_OF_ORDERS for each packer

    NO_OF_ORDERS = 3
    flow_of_batches = {}
    current_item_orders = {}

    for packer in range(1, no_of_packers+1):
        current_item_orders[packer] = {}
        flow_of_batches[packer] = {'number_of_boxes': 0,
                                   'number_of_orders': 0,
                                   'number_of_items': 0,
                                   'flow': []}

        assign_orders_to_packer(packer, order_priority_queue, NO_OF_ORDERS,
                                remaining_orders, current_item_orders[packer], flow_of_batches[packer])

    # ---------------------------------------------------
    # creating a new thread for each packer to operate their orders concurrently

    threads = []
    for packer in range(1, no_of_packers+1):
        thread = threading.Thread(target=operate_orders, args=[packer, current_item_orders[packer],
                                  remaining_orders, available_goods_quantity, order_priority_queue, flow_of_batches[packer]])
        threads.append(thread)
        thread.start()

    # ---------------------------------------------------
    # waiting for all threads to complete before printing the flow of batches

    for thread in threads:
        thread.join()

    # ---------------------------------------------------

    return flow_of_batches, available_goods_quantity


# =============================================================================


def operate_orders(packer, current_item_orders, remaining_orders, available_goods_quantity, order_priority_queue, flow_of_batches):
    """
    This function recursively operates the assigned orders for the given packer and minimizes the number of requested boxes
    :param packer: packer number
    :param current_item_orders: current item to order mapping
    :param remaining_orders: remaining orders as an order status
    :param available_goods_quantity: items quantity in storage
    :param order_priority_queue: order priority queue
    :param flow_of_batches: flow of batches for that packer (maintained)
    :return: none
    """
    # base case
    if len(current_item_orders) == 0:
        return

    # ---------------------------------------------------

    completed_orders = []
    first_item = next(iter(current_item_orders))
    orders = current_item_orders[first_item]

    # ---------------------------------------------------
    # requesting a box of items

    flow_of_batches['flow'].append(
        f"📤 packer {packer} operating box of {first_item}")
    flow_of_batches['number_of_boxes'] += 1

    # ---------------------------------------------------
    # packing item from one box for the assigned orders

    for order_name in orders:
        flow_of_batches['flow'].append(
            Markup(f"&emsp;&emsp;📦 packing {remaining_orders[order_name][first_item]} of {first_item} for order {order_name}"))
        flow_of_batches['number_of_items'] += remaining_orders[order_name][first_item]

        # The lock ensures non-interference between the threads for the same resource
        LOCK.acquire()

        # updating storage quantities
        available_goods_quantity[first_item] -= remaining_orders[order_name][first_item]
        del remaining_orders[order_name][first_item]

        # traking completed orders
        if (len(remaining_orders[order_name]) == 0):
            del remaining_orders[order_name]
            completed_orders.append(order_name)

        LOCK.release()

    # ---------------------------------------------------
    # updated storage to flow of batches

    flow_of_batches['flow'].append(
        Markup(f"&emsp;&emsp;🛒 storage: {available_goods_quantity}"))

    # ---------------------------------------------------
    # assigning new orders instead of the completed ones

    if len(completed_orders):
        for order_name in completed_orders:
            flow_of_batches['flow'].append(
                Markup(f"&emsp;&emsp;✅ order {order_name} complete"))

        del current_item_orders[first_item]
        assign_orders_to_packer(packer, order_priority_queue,
                                len(completed_orders), remaining_orders, current_item_orders, flow_of_batches)
        flow_of_batches['number_of_orders'] += len(completed_orders)
        completed_orders = []

    # ---------------------------------------------------
    # recursive call with updated parameters

    operate_orders(packer, current_item_orders, remaining_orders,
                   available_goods_quantity, order_priority_queue, flow_of_batches)

# =============================================================================


def assign_orders_to_packer(packer, order_priority_queue, num_of_assigned_orders, customer_orders, current_item_orders, flow_of_batches):
    """
    This function assigns a number of orders to a packer depending on the order priority queue. 
    :param packer: packer number
    :param order_priority_queue: order priority queue (maintained)
    :param num_of_assigned_orders: number of orders to assign
    :param customer_orders: customer orders
    :param current_item_orders: current item to order mapping
    :param flow_of_batches: flow of batches for that packer (maintained)
    :return: none
    """
    # no more orders to assign
    if len(order_priority_queue) == 0:
        return

    counter = 0
    while len(order_priority_queue) > 0 and counter <= num_of_assigned_orders:
        order_name = order_priority_queue.pop(0)
        flow_of_batches['flow'].append(
            f"📎 assigning order {order_name} to packer {packer}")

        for item in customer_orders[order_name]:
            if item in current_item_orders:
                current_item_orders[item].append(order_name)
            else:
                current_item_orders[item] = [order_name]
            counter = counter+1

    # ---------------------------------------------------

    # sorting descendingly according to number of orders
    current_item_orders = dict(
        sorted(current_item_orders.items(), key=lambda k: len(k[1]), reverse=True))

# =============================================================================


def order_priority(customer_orders):
    """
    This function takes in customer orders and returns a priority list of order names and a copy of customer orders 
    to keep track of the remaining orders
    :param customer_orders: customer orders
    :return: 
        - queue : list of orders names  e.g.['order_1','order_3']
        - remaining_orders : a copy of customer_order in one dictionary e.g.{'order_1':{'item_1','item_2'},'order_2s':{'item_1'}}
    """

    # item_orders : mapping item to orders e.g.{"item_1":['order_1','order_3'], "item_2":['order_1'] }
    item_orders = {}
    remaining_orders = {}
    for order in customer_orders:
        for order_name, order_value in order.items():
            remaining_orders[order_name] = order_value
            for item in order_value.keys():
                if item in item_orders:
                    item_orders[item].append(order_name)
                else:
                    item_orders[item] = [order_name]

    # ---------------------------------------------------
    # sorting descendingly according to number of orders

    item_orders = dict(
        sorted(item_orders.items(), key=lambda k: len(k[1]), reverse=True))

    # ---------------------------------------------------
    # construction the order priority queue

    queue = []
    for item, orders in item_orders.items():
        for order_name in orders:
            if order_name not in queue:
                queue.append(order_name)

    return queue, remaining_orders

# =============================================================================
