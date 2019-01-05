from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from random import randint
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
import json

from orders.models import Order, OrderItem
from pizzas.models import Pizzas, PizzaSizes
from customers.models import Customers
from orders.serializers import OrderSerializer, OrderItemCreateSerializer


order_url = reverse('orders:orders-list')
item_url = reverse('orders:items-list')


def order_to_dict(obj):
    """
    Creates dict for the model Order instance
    :param obj: Order instance
    :type obj: Order
    :return: dict
    :rtype: dict
    """
    result_dict = {}
    for key, value in obj.__dict__.items():
        if key == '_prefetched_objects_cache':
            for elem_name, elems in obj.__dict__[key].items():
                result_dict[elem_name] = [x.id for x in elems]
            continue
        elif key.startswith('_'):
            continue
        if key.endswith('_id'):
            result_dict[key.split('_')[0]] = value
        else:
            result_dict[key] = value
    return result_dict


def order_detail_url(order_id):
    """
    Order detail URL builder
    :param order_id: order id
    :type order_id: int
    :rtype: str
    """
    return reverse('orders:orders-detail', args=[order_id])


def order_items_url(order_id):
    """
    Order items URL builder
    :param order_id:
    :rtype: str
    """
    return reverse('orders:orderitems-list', args=[order_id])


def order_items_detail_url(order_id):
    """
    Order detail URL builder
    :param order_id: order id
    :type order_id: int
    :rtype: str
    """
    return reverse('orders:orderitems-detail', args=[order_id])


def item_detail_url(item_id):
    """
    Item detail URL builder
    :param item_id: order id
    :type item_id: int
    :rtype: str
    """
    return reverse('orders:items-detail', args=[item_id])


def create_sample_order(customer_id):
    """
    Creates sample order and ties it to the customer_id passed as argument
    :param customer_id: customer id
    :type customer_id: int
    :return: order object
    :rtype: Order
    """
    return Order.objects.create(customer_id=customer_id)


def create_sample_item(order_id, pizza_name, pizza_size, number_of_pizzas):
    """
    Creates new order item and sets it up to the order
    :param order_id: order id
    :return: OrderItem
    """
    return OrderItem.objects.create(
        order_id=order_id,
        pizza_name_id=pizza_name,
        pizza_size_id=pizza_size,
        number_of_pizzas=number_of_pizzas
    )


def generate_test_customers():
    """
    Generates test customers
    :return: list of generated customer objects
    :rtype: list
    """
    all_customers = []
    genders = (Customers.MALE, Customers.FEMALE)
    for name in range(10):
        customer = Customers.objects.create(
            name='test_{}'.format(name),
            phone='342324{}'.format(name),
            email='test_{}@mail.com'.format(name),
            age=30+name,
            gender=genders[name%2]
        )
        all_customers.append(customer)
    return all_customers


def generate_test_pizzas():
    """
    Generates test pizzas
    :return: list of pizzas objects
    :rtype: list
    """
    all_pizzas = []
    for name in range(4):
        pizza = Pizzas.objects.create(
            name='pizza_{}'.format(name)
        )
        all_pizzas.append(pizza)
    return all_pizzas


def generate_pizza_sizes():
    """
    Generates pizza sizes
    :return: List of generated pizza sizes
    :rtype: list
    """
    all_sizes = []
    for name in (PizzaSizes.SMALL, PizzaSizes.MEDIUM, PizzaSizes.LARGE, PizzaSizes.X_LARGE):
        size = PizzaSizes.objects.create(sizename=name)
        all_sizes.append(size)
    return all_sizes


def generate_customers_orders():
    """
    Generates customer's orders
    """
    for customer in Customers.objects.all():
        Order.objects.create(
            customer=customer
        )


def generate_items_for_customer_orders():
    """
    Generates items for customer's orders
    """
    pizzas = Pizzas.objects.all()
    sizes = PizzaSizes.objects.all()

    for order in Order.objects.all():
        for _ in range(2):
            pizza = pizzas[randint(0, len(pizzas)-1)]
            size = sizes[randint(0, len(sizes)-1)]
            number_of_pizzas = randint(1, 10)
            OrderItem.objects.create(
                order=order,
                pizza_name=pizza,
                pizza_size=size,
                number_of_pizzas=number_of_pizzas
            )


def change_order_state(order_id, state):
    """
    Changes order's state
    :param order_id: order id
    :type order_id: int
    :param state: order state
    :type state: str
    """
    Order.objects.get(id=order_id).update(order_state=state)


class OrderTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.customer, _ = Customers.objects.get_or_create(
            name='test',
            age=30,
            email='test@test.com',
            gender='F',
            phone='12321232'
        )
        cls.test_pizza = Pizzas.objects.create(name='test_pizza')
        cls.test_customers = generate_test_customers()
        cls.test_pizzas = generate_test_pizzas()
        cls.test_sizes = generate_pizza_sizes()
        generate_customers_orders()
        generate_items_for_customer_orders()

        cls.locked_order = Order.objects.first()
        cls.order_url = order_detail_url(cls.locked_order.id)
        cls.order_item_url = order_items_url(cls.locked_order.id)

    def test_create_sample_order(self):
        """
        Tests creation or sample order
        """
        sample_order = create_sample_order(OrderTest.customer.id)

        serializer = OrderSerializer(sample_order)
        url = order_detail_url(sample_order.id)
        res = OrderTest.client.get(url)

        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_order_item(self):
        """
        Tests order item creation
        """
        sample_order = create_sample_order(OrderTest.customer.id)

        sample_item = create_sample_item(
            sample_order.id,
            OrderTest.test_pizzas[0].id,
            OrderTest.test_sizes[0].id,
            4
        )

        serializer = OrderItemCreateSerializer(sample_item)
        url = item_detail_url(sample_item.id)
        res = OrderTest.client.get(url)

        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_fail_create_order_with_wrong_data_type(self):
        """
        Tests order creation failure due to the wrong parameters formatting
        """
        sample_data = {
            'customer': OrderTest.customer.id
        }
        res = OrderTest.client.post(order_url, sample_data, content_type='application/json')
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)

    def test_fail_create_order_wrong_param(self):
        """
        Tests order creation failure due to the incorrect parameter
        """
        sample_data = {
            'customer_id': OrderTest.customer.id
        }
        res = OrderTest.client.post(order_url, json.dumps(sample_data), content_type='application/json')
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)

    def test_fail_create_order_empty_params(self):
        """
        Tests order creation failure due to missing parameters
        """
        res = OrderTest.client.post(order_url, json.dumps({}), content_type='application/json')
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)

    def test_create_order_via_post(self):
        """
        Tests creation data via post request
        """
        sample_data = {
            'customer': OrderTest.customer.id
        }
        res = OrderTest.client.post(order_url, json.dumps(sample_data), content_type='application/json')
        self.assertEqual(res.status_code, HTTP_201_CREATED)

    def test_list_orders_for_customer_vs_orm_request(self):
        """
        Lists orders for specified customer
        """
        res = OrderTest.client.get(order_url, data={'customer': OrderTest.customer.id})
        orm_result = []
        orm_request = Order.objects\
            .filter(customer_id=OrderTest.customer.id)\
            .prefetch_related('items')

        for obj in orm_request:
            orm_result.append(order_to_dict(obj))
        for rec in orm_result:
            rec['created'] = rec['created'].isoformat().replace('+00:00', 'Z')
            rec['updated'] = rec['updated'].isoformat().replace('+00:00', 'Z')

        req_data = [dict(x) for x in res.data]
        self.assertListEqual(orm_result, req_data)

    def test_list_orders_total_count_vs_orm(self):
        """
        Check result's amount of orders received via GET request against ORM request
        """
        res = OrderTest.client.get(order_url)
        orm_order_count = Order.objects.count()
        self.assertEqual(orm_order_count, len(res.data))

    def test_create_new_item_for_order(self):
        """
        Creating an item for an order
        """
        item_data = {
            'pizza_name': OrderTest.test_pizzas[0].id,
            'pizza_size': OrderTest.test_sizes[0].id,
            'number_of_pizzas': 3
        }
        res = OrderTest.client.post(OrderTest.order_item_url, json.dumps(item_data), content_type='application/json')
        self.assertEqual(res.status_code, HTTP_201_CREATED)

        item_data['order'] = self.locked_order.id
        result_data = dict(res.data)
        result_data.pop('id')

        self.assertDictEqual(item_data, result_data)

    def test_order_status_changed(self):
        """
        Tests order's status change
        """
        order_data = {
            'order_state': Order.SENT
        }
        res = OrderTest.client.patch(OrderTest.order_url, json.dumps(order_data), content_type='application/json')
        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(res.data.get('order_state'), Order.SENT)

    def test_order_item_create_in_forbidden_status(self):
        """
        Tests creation new item to the order in state SENT or DELIVERED
        :return:
        """
        OrderTest.locked_order.order_state = Order.SENT
        OrderTest.locked_order.save()
        item_data = {
            'pizza_name': OrderTest.test_pizzas[0].id,
            'pizza_size': OrderTest.test_sizes[0].id,
            'number_of_pizzas': 3
        }
        res = OrderTest.client.post(OrderTest.order_item_url, json.dumps(item_data), content_type='application/json')
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)

    def test_order_item_update_number_of_pizza_in_forbidden_status(self):
        """
        Tests if we can change number of pizzas in the order that has been already sent
        """
        OrderTest.locked_order.order_state = Order.SENT
        OrderTest.locked_order.save()
        first_order_state = OrderTest.client.get(OrderTest.order_item_url)
        item_data = {
            'number_of_pizzas': 5
        }
        res = OrderTest.client.post(OrderTest.order_item_url, json.dumps(item_data), content_type='application/json')
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)

        last_order_state = OrderTest.client.get(OrderTest.order_item_url)
        self.assertListEqual(first_order_state.data, last_order_state.data)

    def test_order_item_update_pizza_size_in_forbidden_status(self):
        """
        Tests if we can change pizza size in the order that has been already sent
        """
        OrderTest.locked_order.order_state = Order.SENT
        OrderTest.locked_order.save()
        first_order_state = OrderTest.client.get(OrderTest.order_item_url)
        item_data = {
            'pizza_size': OrderTest.test_sizes[1].id,
        }
        res = OrderTest.client.post(OrderTest.order_item_url, json.dumps(item_data), content_type='application/json')
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)

        last_order_state = OrderTest.client.get(OrderTest.order_item_url)
        self.assertListEqual(first_order_state.data, last_order_state.data)

    def test_order_item_update_pizza_name_in_forbidden_status(self):
        """
        Tests if we can change pizza name in the order that has been already sent
        """
        OrderTest.locked_order.order_state = Order.SENT
        OrderTest.locked_order.save()
        first_order_state = OrderTest.client.get(OrderTest.order_item_url)
        item_data = {
            'pizza_name': OrderTest.test_pizzas[1].id,
        }
        res = OrderTest.client.post(OrderTest.order_item_url, json.dumps(item_data), content_type='application/json')
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)

        last_order_state = OrderTest.client.get(OrderTest.order_item_url)
        self.assertListEqual(first_order_state.data, last_order_state.data)

    def test_change_order_information_in_forbidden_status(self):
        """
        Tests if we can or not change the order details with order status changed
        """
        OrderTest.locked_order.order_state = Order.SENT
        OrderTest.locked_order.save()
        first_order_state = OrderTest.client.get(OrderTest.order_url)

        new_customer = Customers.objects.create(
            name='test_100',
            age=25,
            email='test_100@test.com',
            gender='M',
            phone='12331232'
        )
        order_data = {
            'customer': new_customer.id
        }
        res = OrderTest.client.patch(OrderTest.order_url, json.dumps(order_data), content_type='application/json')
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)

        last_order_state = OrderTest.client.get(OrderTest.order_url)
        self.assertDictEqual(first_order_state.data, last_order_state.data)

    def test_drop_order_state_from_forbidden_to_allowed(self):
        """
        Tests if we can change the state from Sent or Delivered back to the Canceled, Accepted or Processing.
        Request should contain only order_state filed.
        """
        OrderTest.locked_order.order_state = Order.SENT
        OrderTest.locked_order.save()

        order_data = {
            'order_state': Order.CANCELED
        }
        res = OrderTest.client.patch(OrderTest.order_url, json.dumps(order_data), content_type='application/json')

        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(res.data.get('order_state'), 'C')

    def test_fail_drop_order_state_from_forbidden_to_allowed(self):
        """
        Tests if we can change the state from Sent or Delivered back to the Canceled, Accepted or Processing sending
        other parameters in the request.
        Request should contain only order_state filed (but it doesn't in our case).
        """
        OrderTest.locked_order.order_state = Order.SENT
        OrderTest.locked_order.save()

        new_customer = Customers.objects.create(
            name='test_101',
            age=25,
            email='test_101@test.com',
            gender='M',
            phone='12331232'
        )

        order_data = {
            'order_state': Order.CANCELED,
            'customer': new_customer.id
        }
        res = OrderTest.client.patch(OrderTest.order_url, json.dumps(order_data), content_type='application/json')

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)

    def test_drop_order_state_from_forbidden_to_allowed_with_later_update(self):
        """
        Tests if we can change the state from Sent or Delivered back to the Canceled, Accepted or Processing. When an
        order is in allowed state we tests if we can update order details.
        """
        OrderTest.locked_order.order_state = Order.SENT
        OrderTest.locked_order.save()

        new_customer = Customers.objects.create(
            name='test_101',
            age=25,
            email='test_101@test.com',
            gender='M',
            phone='12331232'
        )

        order_custom_data = {
            'customer': new_customer.id
        }
        res = OrderTest.client.patch(
            OrderTest.order_url,
            json.dumps(order_custom_data),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)

        order_state_data = {
            'order_state': Order.PROCESSING
        }
        res = OrderTest.client.patch(
            OrderTest.order_url,
            json.dumps(order_state_data),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(res.data.get('order_state'), 'P')

        res = OrderTest.client.patch(
            OrderTest.order_url,
            json.dumps(order_custom_data),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(res.data.get('customer'), new_customer.id)
