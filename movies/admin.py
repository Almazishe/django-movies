from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Review


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(), label='Описание')

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url",)
    list_display_links = ("id", "name",)


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    readonly_fields = ("email", "name",)


class MovieShotsInline(admin.TabularInline):
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100"')

    get_image.short_description = "Изображение"
    model = MovieShots
    extra = 1


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url", "draft",)
    list_filter = ("draft", "category", "year",)
    search_fields = ("title", "category__name",)
    inlines = (MovieShotsInline, ReviewInline,)
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    readonly_fields = ("get_poster",)
    form = MovieAdminForm
    actions = ("publish", "unpublish",)
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", ("poster", "get_poster",),),
        }),
        (None, {
            "fields": (("year", "world_premiere", "country",),)
        }),
        ("Actors", {
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres", "category",),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fees_in_world",),)
        }),
        ("Options", {
            "fields": (("url", "draft",),)
        }),
    )

    def get_poster(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="400"')

    def unpublish(self, request, queryset):
        """ Снять с публикации """

        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись оформлена"
        else:
            message_bit = f'{row_update} записей обновлены'

        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        """ Опубликовать """

        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись оформлена"
        else:
            message_bit = f'{row_update} записей обновлены'

        self.message_user(request, f'{message_bit}')

    get_poster.short_description = "Постер"
    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change',)

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change',)



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "parent", "movie",)
    readonly_fields = ("name", "email",)
    list_display_links = ("id", "name",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "url",)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100"')

    get_image.short_description = "Изображение"


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """ Кадры из фильма """
    list_display = ("title", "movie", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100"')

    get_image.short_description = "Изображение"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """ Рейтинг """
    list_display = ("movie", "star", "ip",)


admin.site.register(RatingStar)
admin.site.site_title = 'Django movies'
admin.site.site_header = 'Django movies'
