from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Review


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

    get_poster.short_description = "Постер"


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
    list_display = ("movie", "ip",)


admin.site.register(RatingStar)
admin.site.site_title = 'Django movies'
admin.site.site_header = 'Django movies'
