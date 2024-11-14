from datetime import datetime

from django import forms

from reviews.models import Review


class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get("instance", None)
        super(ReviewForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields["product"].initial = self.instance.pk

    def save(self, commit=True, customer=None):
        instance = super().save(commit=False)
        if customer:
            instance.user = customer
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Review
        fields = ["product", "rating", "comment"]

        widgets = {
            "product": forms.HiddenInput(),
        }
