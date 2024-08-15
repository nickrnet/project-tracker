from django import forms


class NewOrganizationDataForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(max_length=255, required=False)
    responsible_party_email = forms.CharField(max_length=255)
    responsible_party_phone = forms.CharField(max_length=255)
    address_line_1 = forms.CharField(max_length=255)
    address_line_2 = forms.CharField(max_length=255, required=False)
    postal_code = forms.CharField(max_length=255)
    city = forms.CharField(max_length=255)
    state = forms.CharField(max_length=255)
    country = forms.CharField(max_length=255)
    timezone = forms.CharField(max_length=255, required=False)

    is_paid = forms.BooleanField(required=False)
    renewal_date = forms.DateField(required=False, widget=forms.SelectDateWidget())
    number_users_allowed = forms.IntegerField(required=False, initial=5)  # This initial has to match the model default

    members = forms.CharField(max_length=255, required=False)
    repositories = forms.CharField(max_length=255, required=False)
    projects = forms.CharField(max_length=255, required=False)


# class NewOrganizationForm(forms.ModelForm):
#     current = NewOrganizationDataForm()

#     class Meta:
#         model = core_organization_models.Organization
#         fields = [
#             'current',
#         ]

#     def save(self, request):
#         organization = super(NewOrganizationForm, self).save(commit=False)
#         try:
#             logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
#         except core_user_models.CoreUser.DoesNotExist:
#             print("User does not exist.")
#             return None

#         organization.created_by = logged_in_user
#         organization.save()
#         return organization
