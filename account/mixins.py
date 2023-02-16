class FormValidMixins():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:       
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            self.obj.status = 2
        return super().form_valid(form)


class FieldsMixins():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = [
                'title',
                'status',
                'image',
                'author',
                'description',
                'category'
            ]
        else:
            self.fields = [
                'title',
                'image',
                'description',
                'category'
            ]
        return super().dispatch(request, *args, **kwargs)
        