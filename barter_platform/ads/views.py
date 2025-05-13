from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Ad, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm
from django.core.paginator import Paginator
from django.db.models import Q

def list_ads(request):
    ads = Ad.objects.all().order_by('-created_at')
    q = request.GET.get('q')
    category = request.GET.get('category')
    condition = request.GET.get('condition')

    if q:
        ads = ads.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if category:
        ads = ads.filter(category__icontains=category)
    if condition:
        ads = ads.filter(condition=condition)

    paginator = Paginator(ads, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Ad.objects.values_list('category', flat=True).distinct()

    return render(request, 'ads/list_ads.html', {
        'ads': page_obj,
        'categories': categories
    })

def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    form = ExchangeProposalForm()
    return render(request, 'ads/ad_detail.html', {'ad': ad, 'form': form})

@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ads:ad_detail', pk=ad.pk)
    else:
        form = AdForm()
    return render(request, 'ads/ad_form.html', {'form': form, 'form_title': 'Создать объявление'})

@login_required
def edit_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user != request.user:
        return render(request, '403.html')

    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ads:ad_detail', pk=ad.pk)
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/ad_form.html', {'form': form, 'form_title': 'Редактировать объявление'})

@login_required
def delete_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user != request.user:
        return render(request, '403.html')

    if request.method == 'POST':
        ad.delete()
        return redirect('ads:list_ads')
    return render(request, 'ads/delete_confirm.html', {'ad': ad})

@login_required
def create_proposal(request, pk):
    ad_receiver = get_object_or_404(Ad, pk=pk)
    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            # Выбор объявления отправителя должен быть реализацией выбора пользователя из своих объявлений
            sender_ads = Ad.objects.filter(user=request.user)
            if not sender_ads.exists():
                return render(request, 'ads/ad_detail.html', {
                    'ad': ad_receiver,
                    'form': form,
                    'error': 'У вас нет объявлений для обмена.'
                })
            proposal.ad_sender = sender_ads.first()  # Упростим: берется первое объявление
            proposal.ad_receiver = ad_receiver
            proposal.save()
            return redirect('ads:list_ads')
    return redirect('ads:ad_detail', pk=pk)

@login_required
def proposals_list(request):
    proposals = ExchangeProposal.objects.filter(ad_sender__user=request.user) | ExchangeProposal.objects.filter(ad_receiver__user=request.user)
    return render(request, 'ads/proposals_list.html', {'proposals': proposals})