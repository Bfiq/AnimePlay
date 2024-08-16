from datetime import datetime
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Genre, Series, Episodes
from .serializers import GenderSerializer, SeriesSerializer, EpisodesSerializer
from apps.utils.azure_storage import AzureBlobService
from rest_framework.response import Response
from rest_framework import status
from apps.utils.mongodb import get_database

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
            serializer = SeriesSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                image = request.FILES.get('image')
                print(image)
                if image:
                    azure_blob_service = AzureBlobService()
                    image_url = azure_blob_service.upload_file(image)

                    print("ANTES DE...")

                    serializer.save(image_url=image_url)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"detail":"Falta el campo image"}, status=status.HTTP_400_BAD_REQUEST)
                
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"detail":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class EpisodesView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Episodes.objects.all()
    serializer_class = EpisodesSerializer

    def post(self, request, *args, **kwargs): 
        try:
            serializer = EpisodesSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                video = request.FILES.get('video')
                print(video)
                if video:
                    azure_blob_service = AzureBlobService()
                    video_url = azure_blob_service.upload_file(video)

                    serializer.save(video_url=video_url)

                    #Crear sección de comentarios
                    comments_collection = get_database()['comments']
                    comments_collection.insert_one({"episode_id": serializer.data['id'], "comments": []})

                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"detail":"Falta el campo video"}, status=status.HTTP_400_BAD_REQUEST)
                
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class CommentsView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            episode_id = request.query_params.get('episode_id')
            print(episode_id)

            if not episode_id:
                return Response({"detail": "El 'episode_id' es necesario"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                episode_id = int(episode_id)
            except ValueError:
                return Response({"detail": "'episode_id' debe ser un número entero"}, status=status.HTTP_400_BAD_REQUEST)

            comments_collection = get_database()['comments']
            print(comments_collection)
            episode_comments = comments_collection.find_one({"episode_id": episode_id})

            print(episode_comments)

            if episode_comments:
                return Response(episode_comments['comments'], status=status.HTTP_200_OK)
            else:
                return Response({"detail": "No se encontró el episodio"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            episode_id = request.data.get('episode_id')
            comment_text = request.data.get('comment_text')

            if not episode_id or not comment_text:
                return Response({"detail": "Faltan campos necesarios"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                episode_id = int(episode_id)
            except ValueError:
                return Response({"detail": "'episode_id' debe ser un número entero"}, status=status.HTTP_400_BAD_REQUEST)

            comments_collection = get_database()['comments']
            result = comments_collection.update_one(
                {"episode_id": episode_id},
                {"$push": {"comments": {"user_id": request.user.id, "comment_text": comment_text, "timestamp": datetime.now() }}}
            )
            
            if result.modified_count > 0:
                return Response({"detail": "Comentario añadido exitosamente"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "No se encontró el episodio"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail":str(e)}, status=status.HTTP_404_NOT_FOUND)