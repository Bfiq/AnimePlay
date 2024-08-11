from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Genre, Series, Episodes
from .serializers import GenderSerializer, SeriesSerializer, EpisodesSerializer
from apps.utils.azure_storage import AzureBlobService
from rest_framework.response import Response
from rest_framework import status

class GenreView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Genre.objects.all()
    serializer_class = GenderSerializer

class SeriesView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer

    def post(self, request, *args, **kwargs): #Se permiten parametros adicionales sin generar error
        try:
            serializer = SeriesSerializer(data=request.data)
            if serializer.is_valid():
                image = request.FILES.get('image')
                print(image)
                if image:
                    azure_blob_service = AzureBlobService()
                    image_url = azure_blob_service.upload_image(image)

                    print("ANTES DE...")

                    serializer.save(image_url=image_url)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class EpisodesView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Episodes.objects.all()
    serializer_class = EpisodesSerializer