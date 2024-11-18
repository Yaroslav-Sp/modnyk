from django import forms

from reviews.models import Review


class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get("instance", None)
        super(ReviewForm, self).__init__(*args, **kwargs)

        self.fields["rating"].required = True
        self.fields["comment"].required = True

        self.fields["comment"].widget.attrs.update(
            {
                "class": "form-control custom-textarea",
            }
        )

    def save(self, commit=True, customer=None):
        instance = super().save(commit=False)
        if customer:
            instance.user = customer
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Review
        fields = ["rating", "comment"]
