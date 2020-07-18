# encoding=utf-8
import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from random import shuffle
import random
from copy import copy, deepcopy

# shift: shiftten başlayıp sona kadar gider,
# :shift bastan baslayıp shifte kadar 1,2,3,4 shift2 3,4,1,2
from django.views.decorators.http import require_http_methods

from sudoku.enums import DifficultyLevel
from sudoku.models import Sudoku


def list_shift(my_list, shift):
    assert shift < len(my_list)
    return my_list[shift:] + my_list[:shift]


def create_solution_matrix(size, sekilli_mi):
    # size kadar satır sutunu olan matris oluşturuyor değerleri sıfır olan
    matrix = [([0] * size) for i in range(size)]

    # Bu satir size'a gore (4, 6, 9) bir satir olusturur.
    # [1, 2, 3, 4] mesela size 4 ise
    values = [i for i in range(1, size + 1)]
    shuffle(values)  # karıştırıyor

    atlama_miktari = 3  # aşağıya doğru
    base_shift_size = 3  # sağa doğru

    if size == 4 or size == 6:
        atlama_miktari = 2

    if size == 4:
        base_shift_size = 2

    # burda matrisin ilk satirini atadik, Sayilar values icinde duruyor
    matrix[0] = values

    # Ikinci asamada sola shift yapip ikinci satiri setliyoruz
    values = list_shift(values, base_shift_size)
    matrix[1] = values

    if size > 6:
        # Ucuncu asamada sola shift yapip ucuncu satiri setliyoruz
        values = list_shift(values, base_shift_size)
        matrix[2] = values

    for i in range(atlama_miktari, size):
        shift_size = base_shift_size
        if (i % atlama_miktari == 0):
            shift_size = 1
        values = list_shift(values, shift_size)
        matrix[i] = values

    if sekilli_mi:
        mapping = {
            1: '□',
            2: '◇',
            3: '△',
            4: '○',
            5: '✕',
            6: '✔'
        }

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                matrix[i][j] = mapping[matrix[i][j]]

    # if size == 9:
    #     temp = matrix[0]
    #     matrix[0] = matrix[2]
    #     matrix[2] = temp
    #     for i in range(atlama_miktari, size):
    #         if (i % atlama_miktari == 0):
    #             gecici = matrix[i]
    #             matrix[i] = matrix[i + 2]
    #             matrix[i + 2] = gecici
    #     kolay_icin = random.randint(34, 36)
    #     orta_icin = random.randint(28, 31)
    #     zor_icin = random.randint(18, 25)
    #
    # if size == 6:
    #     kly_icin = random.randint(13, 15)
    #     ort_icin = random.randint(11, 13)
    #     zr_icin = random.randint(9, 10)
    #
    # if size == 4:
    #     kly = random.randint(9, 10)
    #     orta = random.randint(6, 8)
    #     zor = random.randint(4, 5)

    return matrix


def create_sudoku(solution, size, doluluk_sayisi):
    sudoku = deepcopy(solution)

    bosluk_sayisi = (size * size - doluluk_sayisi)

    while bosluk_sayisi > 0:
        satir = random.randint(0, size - 1)
        sutun = random.randint(0, size - 1)
        while not sudoku[satir][sutun]:
            satir = random.randint(0, size - 1)
            sutun = random.randint(0, size - 1)
        sudoku[satir][sutun] = ''
        bosluk_sayisi -= 1

    return sudoku


def get_query_params(request, default_size):
    size = request.GET.get("size")
    size = default_size if not size else int(size)
    level = request.GET.get("level")
    level = 'kolay' if not level else level
    if level == 'kolay':
        level = DifficultyLevel.KOLAY
    elif level == 'orta':
        level = DifficultyLevel.ORTA
    elif level == 'zor':
        level = DifficultyLevel.ZOR

    return size, level


@login_required
def dokuz(request):
    size, level = get_query_params(request, 9)
    sekilli_mi = False
    solution = create_solution_matrix(size, sekilli_mi)

    if level == DifficultyLevel.KOLAY:
        doluluk_sayisi = random.randint(34, 36)
    elif level == DifficultyLevel.ORTA:
        doluluk_sayisi = random.randint(28, 31)
    else:
        doluluk_sayisi = random.randint(18, 25)

    sudoku = create_sudoku(solution, size, doluluk_sayisi)
    return render(request, "sudoku/sudoku.html",
                  {'sudoku': sudoku, 'solution': solution, 'size': size,
                   'sekilli_mi': sekilli_mi, 'oyunlarim': False})


@login_required
def alti(request):
    size, level = get_query_params(request, 6)
    solution = create_solution_matrix(size, False)

    if level == DifficultyLevel.KOLAY:
        doluluk_sayisi = random.randint(13, 15)
    elif level == DifficultyLevel.ORTA:
        doluluk_sayisi = random.randint(11, 13)
    else:
        doluluk_sayisi = random.randint(9, 10)

    sudoku = create_sudoku(solution, size, doluluk_sayisi)
    return render(request, "sudoku/sudoku.html",
                  {'sudoku': sudoku, 'solution': solution, 'size': size,
                   'oyunlarim': False})


@login_required
def dort(request):
    size, level = get_query_params(request, 4)
    sekilli_mi = False
    solution = create_solution_matrix(size, sekilli_mi)

    if level == DifficultyLevel.KOLAY:
        doluluk_sayisi = random.randint(9, 10)
    elif level == DifficultyLevel.ORTA:
        doluluk_sayisi = random.randint(6, 8)
    else:
        doluluk_sayisi = random.randint(4, 5)

    sudoku = create_sudoku(solution, size, doluluk_sayisi)
    return render(request, "sudoku/sudoku.html",
                  {'sudoku': sudoku, 'solution': solution, 'size': size,
                   'sekilli_mi': sekilli_mi, 'oyunlarim': False})


@login_required
def sembollu_sudoku(request):
    size, level = get_query_params(request, 4)
    sekilli_mi = True

    solution = create_solution_matrix(size, sekilli_mi)

    if level == DifficultyLevel.KOLAY:
        doluluk_sayisi = random.randint(9, 10)
    elif level == DifficultyLevel.ORTA:
        doluluk_sayisi = random.randint(6, 8)
    else:
        doluluk_sayisi = random.randint(4, 5)

    sudoku = create_sudoku(solution, size, doluluk_sayisi)

    return render(request, "sudoku/sudoku.html",
                  {'sudoku': sudoku, 'solution': solution, 'size': size,
                   'sekilli_mi': sekilli_mi, 'oyunlarim': False})


@require_http_methods(['POST', 'PATCH'])
def save_game(request):
    data = json.loads(request.body)

    if request.method == 'POST':
        size = data.get('size')
        game = data.get('game')
        solution = data.get('solution')

        sudoku = Sudoku()
        sudoku.owner = request.user
        sudoku.size = size
        sudoku.game = game
        sudoku.solution = solution
        sudoku.save()
    else:
        id = data.get('id')
        game = data.get('game')

        sudoku = Sudoku.objects.filter(owner=request.user, id=id).first()
        sudoku.game = game
        sudoku.save(update_fields=['game'])

    return JsonResponse({'success': 'true'})


@login_required()
def my_games(request):
    user = request.user
    games = Sudoku.objects.filter(owner=user)
    return render(request, "sudoku/oyunlarim.html", {'games': games})


def convert_1d_to_2d(string, size):
    sudoku_game = []
    row = []

    string = string[1:-1]
    string = string.replace("'", "")
    items = string.split(', ')

    i = 1
    for item in items:
        temp_item = item
        try:
            item = int(temp_item)
        except Exception:
            pass

        row.append(item)
        if i % size == 0:
            sudoku_game.append(row)
            row = []
        i += 1

    return sudoku_game


@login_required()
def my_game(request, id):
    user = request.user

    sudoku = Sudoku.objects.filter(id=id, owner=user).first()
    if not sudoku:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    size = sudoku.size
    game = convert_1d_to_2d(sudoku.game, size)
    solution = convert_1d_to_2d(sudoku.solution, size)

    return render(request, "sudoku/sudoku.html", {
        'sudoku': game,
        'solution': solution,
        'size': sudoku.size,
        'sekilli_mi': False,
        'oyunlarim': True
    })


@login_required()
def delete_game(request, id):
    user = request.user

    sudoku = Sudoku.objects.filter(id=id, owner=user).first()
    if not sudoku:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    sudoku.delete()
    return redirect('oyunlarim')
