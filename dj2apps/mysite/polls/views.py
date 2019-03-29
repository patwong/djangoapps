from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)
    # return HttpResponse("Hello, world. You're at the polls index.")
    context = {'latest_question_list': latest_question_list, }
    return render(request, 'polls/index.html', context)

# end index()


def detail(request, question_id):
    # 1: basic 404 exception try/except block
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # end try/except

    question = get_object_or_404(Question, pk=question_id)

    #  return statement #1
    # return HttpResponse("You're looking at question %s." % question_id)
    return render(request, 'polls/detail.html', {'question': question})
# end detail()


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)
# end results()


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
# end vote()

