from django.shortcuts import render

# Create your views here.
def index(request):
    return render(
        request,
        'frontapp/index.html',
        {}
    )
    
def htmlView01(request):
    return render(
        request,
        'frontapp/html/01_html.html',
        {}
    )
    
def linkView(request):
    return render(
        request,
        'frontapp/html/02_link.html',
        {}
    )

def cssView03(request):
    return render(
        request,
        'frontapp/html/03_css.html',
        {}
    )
def cssView04(request):
    return render(
        request,
        'frontapp/html/04_css.html',
        {}
    )
def cssView05(request):
    return render(
        request,
        'frontapp/html/05_css.html',
        {}
    )
def cssView06(request):
    return render(
        request,
        'frontapp/html/06_css.html',
        {}
    )
def tableView07(request):
    return render(
        request,
        'frontapp/html/07_table.html',
        {}
    )
def tableView08(request):
    
    one_row = {"mem_id":"a001",
         "mem_name" : "이순신",
         "mem_area":"부산 남구 신선로 365번길"}
    return render(
        request,
        'frontapp/html/08_table.html',
        one_row
    )
    
def tableView09(request):
    
    ### 행렬 리스트 만들기
    ### 4행 3열의 행렬 데이터 
    # - 딕셔너리 하나가 행 1개를 의미함
    #   -- 딕셔너리 key가 각 컬럼을 의미한다.
    mem_list = [ {"mem_id":"a001",
                  "mem_name" : "이순신",
                  "mem_area":"부산 남구 신선로 365번길"},
                 {"mem_id":"b001",
                  "mem_name" : "이순신",
                  "mem_area":"부산 남구 신선로 365번길"},
                 {"mem_id":"c001",
                  "mem_name" : "이순신",
                  "mem_area":"부산 남구 신선로 365번길"},
                   {"mem_id":"d001",
                    "mem_name" : "이순신",
                    "mem_area":"부산 남구 신선로 365번길"}]
    
    # contexts = {"mem_id":"a001",
    #      "mem_name" : "이순신",
    #      "mem_area":"부산 남구 신선로 365번길"}
    return render(
        request,
        'frontapp/html/09_table.html',
         {"mem_id":"a001",
         "mem_name" : "이순신",
         "mem_area":"부산 남구 신선로 365번길",
        "mem_list":mem_list}
    )        