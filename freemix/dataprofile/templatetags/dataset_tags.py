from django import template


register = template.Library()

@register.inclusion_tag("dataset/dataset_detail.html", takes_context=True)
def dataset_detail(context, dataset):
    return {"dataset": dataset, "request": context['request']}


@register.inclusion_tag("dataset/list/dataset_list.html", takes_context=True)
def dataset_list(context, datasets, max_count=10, pageable=True):
    return {"queryset": datasets, "max_count": max_count, "pageable": pageable,
            "request": context['request']}
