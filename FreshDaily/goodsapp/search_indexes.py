#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Uson

from haystack import indexes
from goodsapp.models import GoodsInfo


class GoodsInfoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return GoodsInfo

    def index_queryset(self, using=None):
        return self.get_model().objects.all()