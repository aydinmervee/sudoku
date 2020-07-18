from django.urls import path
from . import views

urlpatterns = [
    path('dokuz/', views.dokuz, name="dokuz"),
    path('alti/', views.alti, name="alti"),
    path('dort/', views.dort, name="dort"),
    path('sembollu_sudoku/', views.sembollu_sudoku, name="sembollu_sudoku"),
    path('save_game/', views.save_game, name="save_game"),
    path('oyunlarim/', views.my_games, name="oyunlarim"),
    path('oyunlarim/<int:id>', views.my_game, name="oyunum"),
    path('oyunlarim/sil/<int:id>', views.delete_game, name="oyunu_sil"),
]
