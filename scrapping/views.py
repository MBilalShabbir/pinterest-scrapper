from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import scraps
from .selenium.selenium import fetch_data


class ScrappingView(APIView):
    def post(self, request):
        res = scraps(request.data.get('url'))
        return Response(res, status=status.HTTP_200_OK)


class SeleniumScrappingView(APIView):
    def post(self, request):
        res = fetch_data(request.data.get('url'))
        return Response(res, status=status.HTTP_200_OK)
