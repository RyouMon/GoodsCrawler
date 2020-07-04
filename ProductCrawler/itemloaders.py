import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import *


class ProductLoader(ItemLoader):
    # use SelectorList.get() default
    default_output_processor = TakeFirst()


def supreme_week_processor(value):
    match = re.findall(r"\((.*?)\)", value)
    return match[0]


class SupremeLoader(ProductLoader):
    title_out = Compose(
        TakeFirst(),
        lambda x: x.strip(),
        lambda x: x.replace("*", "-"),
        lambda x: x.replace("/", "-"),
    )
    images_out = MapCompose(lambda x: x.replace("thumb", "sqr"))  # 把缩略图的链接替换为源图的链接
    week_out = Compose(TakeFirst(), supreme_week_processor)


class KapitalLoader(ProductLoader):
    art_no_out = Compose(
        TakeFirst(),
        lambda x: x.strip(),
    )
    images_out = Identity()
    category_out = Compose(
        TakeFirst(),
        lambda x: re.findall(r'category/(.*?)/', x),
        lambda x: x[0]
    )


class GallianolandorLoader(ProductLoader):
    price_out = Compose(
        TakeFirst(),
        lambda x: x.strip(),
    )
    images_out = MapCompose(
        lambda x: x.split('?')[0]  # 去除image_url的query部分
    )
    season_out = Compose(
        TakeFirst(),
        lambda x: x.replace('/', '')
    )


class NikeLoader(ProductLoader):
    images_out = Compose(
        Identity(),
        lambda urls: [url for url in urls if 'LOADING' not in url]
    )
    art_no_out = Compose(
        TakeFirst(),
        lambda x: re.search(r'.{6}-.{3}', x).group()
    )


class BearBrickLoader(ProductLoader):
    # images output:
    # 1 original values
    images_out = Identity()

    # title output:
    # 1 take first value.
    # 2 strip text.
    title_out = Compose(
        TakeFirst(),
        lambda x: x.strip()
    )

    # category input:
    # 1 take first value
    # 2 matching size info in this value.
    # 3 if matched then return sub group, else return string "other".
    category_in = Compose(
        TakeFirst(),
        lambda x: re.search(r'(\d{3}[％%] & )?\d{3,4}[％%]', x),
        lambda x: x.group() if x else "other",
    )
