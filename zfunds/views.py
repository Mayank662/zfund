from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ZUser, Category, Product, Purchase
from project.settings import BASE_URL

class CreateAdvisor(APIView):
    def post(self, request):
        print('hello world')
        data = request.data
        phone = data.get('phone')
        otp = data.get('otp')
        if phone and otp:
            try:
                advisor_account = ZUser.objects.create(phone = phone, account_type = 'ADVISOR')
            except:
                return Response(
                    data={
                        'message': 'Something went wrong.'
                    },
                    status=400
                )
            if advisor_account:
                return Response(
                    data={
                        'message':'Advisor Account Created Successfully.',
                        'token': str(advisor_account.key),
                        'id': advisor_account.id
                    },
                    status=201
                )
            else:
                return Response(
                    data={
                        'message':'User not created.'
                    },
                    status=400
                )
        else:
            return Response(
                data={
                    'message':'Unprocessible entity.'
                },
                status=422
            )


class CreateClient(APIView):
    def post(self, request):
        print('hello world')
        data = request.data
        phone = data.get('phone')
        client_name = data.get('client_name')
        advisor_id = data.get('advisor_id')
        otp = data.get('otp')
        if phone and client_name:
            # Case 1: When client is added by the advisor
            if advisor_id:
                try:
                    client_account = ZUser.objects.create(
                        account_type = 'CLIENT',
                        name = client_name,
                        phone = phone,
                        is_self_registered = False,
                        user_created_by = advisor_id
                    )
                except:
                    return Response(
                        data={
                            'message': 'Something went wrong.'
                        },
                        status=400
                    )
                if client_account:
                    return Response(
                        data={
                            'message':'Client Account Created Successfully.',
                            'token': str(client_account.key),
                            'client_id': client_account.id,
                            'advisor_id': advisor_id,
                            'name':client_account.name,
                            'phone': client_account.phone
                        },
                        status=201
                    )
                else:
                    return Response(
                        data={
                            'message':'User not created.'
                        },
                        status=400
                    )

            # Case 2: When client signup on his own
            elif otp:
                try:
                    client_account = ZUser.objects.create(
                        account_type = 'CLIENT',
                        name = client_name,
                        phone = phone
                    )
                except:
                    return Response(
                        data={
                            'message': 'Something went wrong.'
                        },
                        status=400
                    )
                if client_account:
                    return Response(
                        data={
                            'message':'Client Account Created Successfully.',
                            'token': str(client_account.key),
                            'client_id': client_account.id,
                            'name':client_account.name,
                            'phone': client_account.phone
                        },
                        status=201
                    )
                else:
                    return Response(
                        data={
                            'message':'User not created.'
                        },
                        status=400
                    )
        else:
            return Response(
                data={
                    'message':'Unprocessible entity.'
                },
                status=422
            )
        

class AdvisorClientView(APIView):
    def get(self, request):
        print('hello world')
        data = request.data
        advisor_id = data.get('advisor_id')
        if advisor_id:
            try:
                advisor_clients = ZUser.objects.filter(user_created_by = advisor_id)
            except:
                return Response(
                    data={
                        'message': 'Something went wrong.'
                    },
                    status=400
                )
            if advisor_clients:
                response = []
                for each_data in advisor_clients:
                    response.append(
                        {
                            'client_id': each_data.id,
                            'client_name': each_data.name,
                            'client_phone': each_data.phone   
                        }
                    )
                return Response(
                    data=response,
                    status=200
                )
            else:
                return Response(
                    data={
                        'message':'No clients found for this advisor.'
                    },
                    status=404
                )
        else:
            return Response(
                data={
                    'message':'Unprocessible entity.'
                },
                status=422
            )


class AddProducts(APIView):
    def post(self, request):
        print('hello world')
        data = request.data
        admin_id = data.get('admin_id')
        try:
            admin = ZUser.objects.get(id = admin_id, account_type = 'ADMIN')
        except:
            return Response(
                data={
                    'message':'Only Admin can add the products.'
                },
                status=401
            )
        product_name = data.get('product_name')
        desc = data.get('description')
        category_name = (data.get('category_name')).lower()

        if product_name and desc and category_name:
            try:
                cate_obj = Category.objects.get(name = category_name)
            except Exception as e:
                print('----------',e)
                cate_obj = Category.objects.create(name = category_name)
            
            try:
                product_obj = Product.objects.create(
                    name = category_name,
                    description = desc,
                    category = cate_obj
                )
            except Exception as e:
                print('===========',e)
                return Response(
                    data={
                        'message':'Something went wrong.'
                    },
                    status=400
                )
            if product_obj:
                return Response(
                    data={
                        'message':'Product added Successfully.',
                        'product_name': product_name,
                        'category_name': category_name,
                    },
                    status=201
                )
            else:
                return Response(
                    data={
                        'message':'Product not created.'
                    },
                    status=400
                )

        else:
            return Response(
                data={
                    'message':'Unprocessible entity.'
                },
                status=422
            )


class PurchaseProduct(APIView):
    def get(self, request):
        print('hello world')
        data = request.data
        advisor_id = data.get('advisor_id')
        client_id = data.get('client_id')
        product_id = data.get('product_id')
        if advisor_id and client_id and product_id:
            try:
                advisor_obj = ZUser.objects.get(id = advisor_id, account_type='ADVISOR')
                client_obj = ZUser.objects.get(id = client_id, account_type='CLIENT')
                product_obj = Product.objects.get(pid = product_id)
            except Exception as e:
                print('eeeeeeeeee',e)
                return Response(
                    data={
                        'message': 'Unprocessible Entity.'
                    },
                    status=422
                )
            purchase_obj = Purchase.objects.create(
                product_id = product_id,
                client_id = client_id,
                advisor_id = advisor_id
            )
            if purchase_obj:
                Product.objects.get(pid = product_id).delete()
                product_link = f'{BASE_URL}/purchase-product/{product_id}/{client_id}/'
                return Response(
                    data={
                        'message': f'Product purchased by the client {client_id}',
                        'product_link': product_link
                    },
                    status=200
                )
            else:
                return Response(
                    data={
                        'message':'Unable to complete the transaction.'
                    },
                    status=400
                )
        else:
            return Response(
                data={
                    'message':'Unprocessible entity.'
                },
                status=422
            )
