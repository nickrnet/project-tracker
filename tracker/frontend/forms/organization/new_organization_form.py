from django import forms

from core.models import user as core_user_models
from core.models import organization as core_organization_models


class NewOrganizationDataForm(forms.ModelForm):
    class Meta:
        model = core_organization_models.OrganizationData
        fields = [
            'name',
            'description',
            'responsible_party_email',
            'responsible_party_phone',
            'address_line_1',
            'address_line_2',
            'postal_code',
            'city',
            'state',
            'country',
            'timezone',
        ]

    def save(self, request):
        try:
            logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
        except core_user_models.CoreUser.DoesNotExist:
            return None

        organization_data = super(NewOrganizationDataForm, self).save(commit=False)

        organization_data.created_by = logged_in_user
        organization_data.save()
        organization = core_organization_models.Organization(created_by=logged_in_user, organization_data=organization_data)
        organization.save()
        organization.members.add(logged_in_user)
        organization.save()

        return organization_data


class NewOrganizationForm(forms.ModelForm):
    organization_data = NewOrganizationDataForm()

    class Meta:
        model = core_organization_models.Organization
        fields = [
            'organization_data',
        ]

    def save(self, request):
        organization = super(NewOrganizationForm, self).save(commit=False)
        try:
            logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
        except core_user_models.CoreUser.DoesNotExist:
            print("User does not exist.")
            return None

        organization.created_by = logged_in_user
        organization.save()
        return organization
