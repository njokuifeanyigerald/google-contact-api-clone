from genericpath import exists
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, response

from app.models import Contact, CustomUser
from .serializer import UserSerializer

class ContactAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user =request.user 

        contact = list(user.contacts.values())

        return JsonResponse({'contact': contact})

    # def get(self, request):
    #     user =request.user
    #     contact = user.con
    #     return response.Response({'contact': serializer.data})

    def post(self, request, format=None):
        data = request.data
        user= request.user

        try:
            country_code = data['country_code']
            full_name = data['full_name']
            phone_number =data['phone_number']

            custom_id = len(user.contacts.all())+1

            new_contact = Contact.objects.create(
                full_name = full_name,
                country_code = country_code,
                phone_number  = phone_number,
                custom_id = custom_id
            )

            if data.get('is_favourite'):
                new_contact.is_favorite = data['is_favourite']
                new_contact.save()

            user.contacts.add(new_contact)

            context = {
                'full_name': full_name,
                'country_code': country_code,
                'phone_number': phone_number,
                'custom_id': custom_id
            }

            return JsonResponse(context, status=201)

        except KeyError as e:
            error_message = f"{e.args[0]} is a required field"

            return JsonResponse({e.args[0]: [error_message]}, status = 400)



class ContactAPIUpdateDelete(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, format=None, *args, **kwargs):
        data = request.data
        user= request.user

        try:
            contact = user.contacts.filter(custom_id=kwargs['custom_id'])
            if not contact:
                raise Contact.DoesNotExist

            contact = contact[0]
            country_code = data['country_code']
            full_name = data['full_name']
            phone_number = data['phone_number']


            contact.country_code = country_code
            contact.full_name = full_name
            contact.phone_number = phone_number

            if data.get('is_favourite'):
                contact.is_favorite = data['is_favourite']

            contact.save()

            context = {
                'full_name': contact.full_name,
                'country_code': contact.country_code,
                'phone_number': contact.phone_number,
                'custom_id': contact.custom_id

            }

            return JsonResponse(context, status=200)
        except KeyError as e:
            error_message = f"{e.args[0]} is a required field"

            return JsonResponse({e.args[0]: [error_message]}, status = 400)

        except Contact.DoesNotExist:
            return HttpResponseBadRequest({'error: this contact does not exist'})

        except:
            return HttpResponseBadRequest()

    def delete(self, request, *args, **kwargs):
        id  = kwargs['custom_id']

        try:
            user = request.user
            contact = user.contacts.filter(custom_id=id)

            if not contact:
                raise Contact.DoesNotExist
            contact[0].delete()

            return JsonResponse({'detail': 'contact successfully deleted'})

        except Contact.DoesNotExist:
            return HttpResponseBadRequest({'error: this contact does not exist'})

        except:
            return HttpResponseBadRequest()


class ContactSearchAPI(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        full_name = kwargs['full_name']
        contacts = list(user.contacts.filter(full_name__contains=full_name).values())
        if not contacts:
            return HttpResponseBadRequest({'error: this contact does not exist'})

        context = {
            'search_matches':contacts,
            'search_length': len(contacts)
        }

        return JsonResponse(context, status=200)

