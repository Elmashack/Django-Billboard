from django.contrib import admin

from .models import SuperRubric, SubRubric, Bboard, AdditionalImg
from .forms import SubRubricForm


class SubRubricInline(admin.TabularInline):
    model = SubRubric


class SuperRubricAdmin(admin.ModelAdmin):
    exclude = ('super_rubric',)
    inlines = (SubRubricInline, )


class SubRubricAdmin(admin.ModelAdmin):
    form = SubRubricForm


class AdditionalImgInline(admin.TabularInline):
    model = AdditionalImg


class BboardAdmin(admin.ModelAdmin):
    list_display = ('rubric', 'title', 'description', 'author', 'created_at')
    fields = (('rubric', 'author'), 'title', 'description', 'price', 'contacts', 'image', 'is_active')
    inlines = (AdditionalImgInline,)


admin.site.register(SuperRubric, SuperRubricAdmin)
admin.site.register(SubRubric, SubRubricAdmin)
admin.site.register(Bboard, BboardAdmin)
