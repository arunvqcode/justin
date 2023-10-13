from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import RegistrationSerializer,LoginSerializer
from django.http import JsonResponse

from .pdf_QA import get_pdf_text,get_text_chunks,get_vectorstore,get_conversation_chain



@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()

            token, created = Token.objects.get_or_create(user=account)
            response_data = {
                'status': 'True',
                'message': "Registration Successful!"
            
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'status':"True",
                                'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'status':"False",
                                'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['POST',])
# def logout_view(request):

#     if request.method == 'POST':
#         request.user.auth_token.delete()
#         return Response({'message':"Logout sucessful"},status=status.HTTP_200_OK)       
    
    


@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        token=request.headers.get('Authorization')
        try:
            token = Token.objects.get(key=token)
            token.delete()
            return Response({'status':"True",
                'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'status':"False",
                'error': 'Token not found'}, status=status.HTTP_400_BAD_REQUEST)
            
# ---------------wave journal pdf question answers chatbot------------------    

@api_view(['POST','GET'])
def journal(request):
    pdf_docs = ['uploads/uploaded_pdf.pdf']
    raw_text = get_pdf_text(pdf_docs)
    text_chunks = get_text_chunks(raw_text)
    vectorstore = get_vectorstore(text_chunks)
    conversation_chain = get_conversation_chain(vectorstore)

    user_question = request.POST.get('question')
    print(user_question)
    
    response = conversation_chain({'question': user_question})
    print(response)
    response_text = response['answer']
    print("pdf resposne>>>>>>",response_text)

    return JsonResponse({"response_text":response_text})

    
    