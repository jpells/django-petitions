from django.views.generic.list_detail import object_detail
from django.views.generic.create_update import create_object
from petitions.models import Petition, Signature
from petitions import settings
from django.http import Http404
from django import newforms as forms
from django.http import HttpResponseRedirect

def petition_detail(request, queryset, date_field, object_id=None, slug=None, slug_field=None, year=None, month=None, day=None):
    if object_id != None:
        petition = Petition.objects.get(id=object_id)
    elif slug != None:
        petition = Petition.objects.get(**{slug_field: slug})
    if int(petition.state) != settings.STATE_PUBLISHED:
        raise Http404
    signatures = petition.signature_set.filter(state=settings.STATE_PUBLISHED)

    already_signed = False
    if request.user.is_authenticated():
        if petition.signature_set.filter(user=request.user).count() > 0:
            already_signed = True

    SignatureFormClass = forms.models.form_for_model(Signature)
    SignatureFormClass.base_fields['user'].widget = forms.widgets.HiddenInput()
    SignatureFormClass.base_fields['user'].initial = request.user.id
    SignatureFormClass.base_fields['ip_address'].widget = forms.widgets.HiddenInput()
    SignatureFormClass.base_fields['ip_address'].initial = request.META['REMOTE_ADDR'] 
    SignatureFormClass.base_fields['state'].widget = forms.widgets.HiddenInput()
    SignatureFormClass.base_fields['state'].initial = settings.STATE_DEFAULT
    SignatureFormClass.base_fields['petition'].widget = forms.widgets.HiddenInput()
    SignatureFormClass.base_fields['petition'].initial = petition.id
    SignatureFormClass.base_fields['vote'].widget = forms.widgets.Select(choices=settings.PETITION_SIGNATURE_CHOICES)

    form = None
    if not already_signed:
        if request.POST:
            if not request.user.is_authenticated():
                return HttpResponseRedirect('/accounts/login/?next='+petition.get_absolute_url())
            form = SignatureFormClass(request.POST)
            if form.is_valid():
                signature = form.save()
                return HttpResponseRedirect(signature.get_absolute_url())
    if form == None:
        form = SignatureFormClass()
    return object_detail(request, queryset, object_id, slug, slug_field, extra_context={'user_signed': already_signed, 'signatures': signatures, 'form': form})
