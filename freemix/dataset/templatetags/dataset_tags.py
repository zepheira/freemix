from django import template


register = template.Library()

@register.inclusion_tag("dataset/dataset_summary.html", takes_context=True)
def dataset_summary(context, dataset):
    return {"dataset": dataset, "request": context['request']}


@register.inclusion_tag("dataset/dataset_list.html", takes_context=True)
def dataset_list(context, datasets, max_count=10, pageable=True):
    return {"object_list": datasets, "max_count": max_count, "pageable": pageable,
            "request": context['request']}
