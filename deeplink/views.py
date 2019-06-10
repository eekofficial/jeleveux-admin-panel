from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .admitad_scripts import get_admitad_link, get_campaign_list, AdmitadCampaignError, AdmitadLinkError
from .viglink_scripts import get_viglink_link, VigLinkError
from .vk_scripts import send_vk_post, save_photo, clean_html, VKPhotoError, VKPostError
from .tg_scripts import send_tg_post, upload_tg_photo, TGPhotoError, TGPostError
from .jlvx import get_short_link, JLVXLinkError
from .models import Good

@method_decorator(csrf_exempt, name='dispatch')
class DeeplinkAdmitad(LoginRequiredMixin, CreateView):
    def get(self, request):
        website = '867417'
        try:
            campaigns = get_campaign_list(website)
        except AdmitadCampaignError:
            return HttpResponse('Ошибка в получении списка партнерских программ Admitad')
        return render(request, 'deeplink/index.html', {'cpa': 'admitad', 'campaigns': campaigns})

    def post(self, request):
        link_list = list()
        cpa = 'admitad'
        for i in range(1, 6):
            link_list.append(request.POST.get('link{}'.format(i)))
        message = request.POST.get('message')
        photo = request.FILES['photo']
        tg = request.POST.get('tg')
        vk = request.POST.get('vk')
        campaign = request.POST.get('campaign')
        website = '867417'
        post_item = Good(cpa=cpa, vk=vk, tg=tg)
        if vk:
            short_vk_link_list = list()
            subid = 'vk'
            try:
                post_item.vk_photo = save_photo(photo)
            except VKPhotoError:
                return HttpResponse('Ошибка в сохранении фотографии на сервере Вконтакте')
            for i in range(1, 6):
                if link_list[i-1] != '':
                    try:
                        short_vk_link_list.append(get_short_link(get_admitad_link(website, campaign, link_list[i-1], subid)))
                    except AdmitadLinkError:
                        return HttpResponse('Ошибка в генерации партнерской ссылки Admitad')
                    except JLVXLinkError:
                        return HttpResponse('Ошибка в сокращении url')
                else:
                    short_vk_link_list.append('')
            post_item.vk_message = clean_html(message.format(link1=short_vk_link_list[0], link2=short_vk_link_list[1], link3=short_vk_link_list[2], link4=short_vk_link_list[3], link5=short_vk_link_list[4]))
        #фото на серверах телеграма сохраняем даже если оно не используется в постах (нужно для превью)
        try:
            post_item.tg_photo = upload_tg_photo(photo.open())
        except TGPhotoError:
            return HttpResponse('Ошибка в сохранении фото на сервере Telegram')
        if tg:
            short_tg_link_list = list()
            subid = 'tg'
            for i in range(1, 6):
                if link_list[i-1] != '':
                    try:
                        short_tg_link_list.append(get_short_link(get_admitad_link(website, campaign, link_list[i-1], subid)))
                    except AdmitadLinkError:
                        return HttpResponse('Ошибка в генерации партнерской ссылки Admitad')
                    except JLVXLinkError:
                        return HttpResponse('Ошибка в сокращении url')
                else:
                    short_tg_link_list.append('')
            post_item.tg_message = message.format(link1=short_tg_link_list[0], link2=short_tg_link_list[1], link3=short_tg_link_list[2], link4=short_tg_link_list[3], link5=short_tg_link_list[4])
        post_item.save()
        return render(request, 'deeplink/preview.html', {'cpa': cpa, 'vk': vk, 'tg': tg, 'vk_message': post_item.vk_message, 'tg_message': post_item.tg_message, 'vk_photo': post_item.vk_photo, 'tg_photo': post_item.tg_photo})

class DeeplinkVigLink(LoginRequiredMixin, CreateView):
    def get(self, request):
        return render(request, 'deeplink/index.html', {'cpa': 'viglink'})

    def post(self, request):
        link_list = list()
        cpa = 'viglink'
        for i in range(1, 6):
            link_list.append(request.POST.get('link{}'.format(i)))
        message = request.POST.get('message')
        photo = request.FILES['photo']
        tg = request.POST.get('tg')
        vk = request.POST.get('vk')
        post_item = Good(cpa=cpa, vk=vk, tg=tg)
        if vk:
            short_vk_link_list = list()
            subid = 'vk'
            try:
                post_item.vk_photo = save_photo(photo)
            except VKPhotoError:
                return HttpResponse('Ошибка в сохранении фотографии на сервере Вконтакте')
            for i in range(1, 6):
                if link_list[i-1] != '':
                    try:
                        short_vk_link_list.append(get_short_link(get_viglink_link(link_list[i-1], subid)))
                    except VigLinkError:
                        return HttpResponse('Данная партнерская программа не поддерживается')
                    except JLVXLinkError:
                        return HttpResponse('Ошибка в сокращении url')
                else:
                    short_vk_link_list.append('')
            post_item.vk_message = clean_html(message.format(link1=short_vk_link_list[0], link2=short_vk_link_list[1], link3=short_vk_link_list[2], link4=short_vk_link_list[3], link5=short_vk_link_list[4]))
        #фото на серверах телеграма сохраняем даже если оно не используется в постах (нужно для превью)
        try:
            post_item.tg_photo = upload_tg_photo(photo.open())
        except TGPhotoError:
            return HttpResponse('Ошибка в сохранении фото на сервере Telegram')
        if tg:
            short_tg_link_list = list()
            subid = 'tg'
            for i in range(1, 6):
                if link_list[i-1] != '':
                    try:
                        short_tg_link_list.append(get_short_link(get_viglink_link(link_list[i-1], subid)))
                    except VigLinkError:
                        return HttpResponse('Данная партнерская программа не поддерживается')
                    except JLVXLinkError:
                        return HttpResponse('Ошибка в сокращении url')
                else:
                    short_tg_link_list.append('')
            post_item.tg_message = message.format(link1=short_tg_link_list[0], link2=short_tg_link_list[1], link3=short_tg_link_list[2], link4=short_tg_link_list[3], link5=short_tg_link_list[4])
        post_item.save()
        return render(request, 'deeplink/preview.html', {'cpa': cpa, 'vk': vk, 'tg': tg, 'vk_message': post_item.vk_message, 'tg_message': post_item.tg_message, 'vk_photo': post_item.vk_photo, 'tg_photo': post_item.tg_photo})

class SendPost(LoginRequiredMixin, CreateView):
    def post(self, request):
        cpa = request.POST.get('cpa')
        last_good = Good.objects.last()
        if last_good.vk:
            try:
                send_vk_post(last_good.vk_message, last_good.vk_photo)
            except VKPostError:
                return HttpResponse('Ошибка в отправлении поста Вконтакте')
        if last_good.tg:
            try:
                send_tg_post(last_good.tg_message, last_good.tg_photo)
            except TGPostError:
                return HttpResponse('Ошибка в отправлении поста Telegram')
        last_good.delete()
        if cpa == 'admitad':
            return HttpResponseRedirect('/addpost/admitad')
        elif cpa == 'viglink':
            return HttpResponseRedirect('/addpost/viglink')


# Create your views here.
