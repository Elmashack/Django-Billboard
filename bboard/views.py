from django.db.models import Q
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.shortcuts import render, get_object_or_404

from .forms import SearchForm
from .models import SubRubric, Bboard


def detail(request, rubric_pk, pk):
    bb = get_object_or_404(Bboard, pk=pk)
    add_imgs = bb.additionalimg_set.all()
    context = {'bb': bb, 'add_imgs': add_imgs}
    return render(request, 'bboard/detail.html', context)


def by_rubrics(request, pk):
    rubric = get_object_or_404(SubRubric, pk=pk)
    boards = Bboard.objects.filter(is_active=True, rubric=pk)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(description__icontains=keyword)
        boards = boards.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(boards, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'rubric': rubric, 'page': page, 'boards': page.object_list, 'form': form}
    return render(request, 'bboard/by_rubric.html', context)


def main_page(request):
    return render(request, 'bboard/main.html')


def about_page(request, page):
    try:
        template = get_template('bboard/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))
